from decimal import Decimal, ROUND_HALF_UP
import logging
from django.conf import settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models, IntegrityError, transaction
from django.db.models import Sum, Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from model_utils.models import TimeStampedModel

from .exceptions import FinanceException
from .managers import InvoiceManager, EncounterManager, ClinicBillingCodeManager
from ..clinics.models import CareTakingFacility, UniversalBillingCode, Clinic, ClinicMember, Company
from ..core.models import Auditable
from ..patients.models import Patient, InsuranceCompany

logger = logging.getLogger(__name__)


class ClinicBillingCode(Auditable, TimeStampedModel):
    display_order = models.IntegerField(_("Display order"), default=1000)
    universal_code = models.ForeignKey(
        UniversalBillingCode,
        verbose_name=_("universal billing code"),
        on_delete=models.PROTECT,
        related_name="clinic_billing_codes",
    )
    clinic = models.ForeignKey(
        Clinic, verbose_name=_("clinic"), on_delete=models.PROTECT, related_name="clinic_billing_codes"
    )
    price = models.DecimalField(_("price"), max_digits=8, decimal_places=2)
    can_have_discount = models.BooleanField(_("can have discount"), default=True)
    activation_date = models.DateField(_("Activation Date"))
    expiration_date = models.DateField(_("Expiration date"), null=True, blank=True)

    objects = ClinicBillingCodeManager()

    class Meta:
        ordering = ("display_order", "universal_code__description")
        verbose_name = _("clinic billing code")
        verbose_name_plural = _("clinic billing codes")

    def clean_fields(self, exclude=None):
        if self.expiration_date is not None and self.expiration_date < self.activation_date:
            raise ValidationError({"expiration_date": _("Expiration date cannot be before activation date")})

    def validate_unique(self, *args, **kwargs):
        super(ClinicBillingCode, self).validate_unique(*args, **kwargs)
        self._check_for_open()
        self._check_for_date_overlap()

    def _check_for_date_overlap(self):
        ol_filter = Q(expiration_date__gte=self.activation_date, universal_code=self.universal_code, clinic=self.clinic)
        if self.expiration_date is not None:
            ol_filter.add(
                Q(
                    activation_date__lte=self.expiration_date,
                ),
                Q.AND,
            )

        qs = self.__class__._default_manager.filter(ol_filter)

        if not self._state.adding and self.pk is not None:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                {
                    NON_FIELD_ERRORS: [
                        "overlapping date range",
                    ],
                }
            )

    def _check_for_open(self):
        # Issue
        qs = self.__class__._default_manager.filter(
            expiration_date__isnull=True, universal_code=self.universal_code, clinic=self.clinic
        )
        # TODO Verify if there is a better way to exclude
        if not self._state.adding and self.pk is not None:
            qs = qs.exclude(pk=self.pk)
            # logger.debug(f'Excluding {self.pk}')

        if qs.exists():
            count = qs.count()
            pks_list = list()
            # for obj in qs.all():
            #     pks_list.append(f'{obj.pk}')
            #     logger.debug(f'Pk:{obj.pk} code:{obj.universal_code.code} clinic:{obj.clinic}')
            msg = (
                "There is {} existing billing code(s) in this clinic "
                "that are open (expiration date is null). Pks {}".format(count, ",".join(pks_list))
            )
            raise ValidationError(
                {
                    NON_FIELD_ERRORS: [
                        msg,
                    ],
                }
            )

    def __str__(self):
        now = timezone.now().date()
        if self.expiration_date is not None and self.expiration_date > now:
            return _("{} - Standard Charge {} (expired)").format(self.universal_code, self.price)
        else:
            return _("{} - Standard Charge {}").format(self.universal_code, self.price)


class ChargeType(models.Model):
    """
    Charge types are used by accountants to classify what taxation is used fot the billing items.
    Current values are Emergency, Hospitalization, External Consultation and Home Visit.
    """

    code = models.CharField(_("code"), max_length=10, unique=True)
    name = models.CharField(_("name"), max_length=100)
    requires_hospital_info = models.BooleanField(_("requires hospital info"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = _("charge type")
        verbose_name_plural = _("charge types")


class ClinicChargeType(Auditable, TimeStampedModel):
    display_order = models.IntegerField(_("Display order"), default=1000)
    charge_type = models.ForeignKey(ChargeType, verbose_name=_("charge type"), on_delete=models.PROTECT)
    clinic = models.ForeignKey(Clinic, verbose_name=_("clinic"), on_delete=models.PROTECT)

    class Meta:
        ordering = ("display_order", "charge_type__name")
        verbose_name = _("clinic charge type")
        verbose_name_plural = _("clinic charge types")


class Invoice(TimeStampedModel):
    BILL_TO_PATIENT = "PATIENT"
    BILL_TO_INSURANCE = "INSURANCE"
    BILL_TO_HOSPITAL = "HOSPITAL"
    BILL_TO_OTHER = "OTHER"
    BILL_TO_CHOICES = (
        (BILL_TO_PATIENT, _("Invoice to patient")),
        (BILL_TO_INSURANCE, _("Invoice to insurance company")),
        (BILL_TO_HOSPITAL, _("Invoice to Hospital")),
        (BILL_TO_OTHER, _("Invoice to Other")),
    )
    UNPAID_STATUS = "UNPAID"
    PARTIAL_STATUS = "PARTIAL"
    PAID_STATUS = "PAID"
    OVER_PAID_STATUS = "OVER_PAID"

    PAYMENT_STATUS_CHOICES = (
        (UNPAID_STATUS, _("Unpaid")),
        (PARTIAL_STATUS, _("Partially paid")),
        (PAID_STATUS, _("Paid")),
        (OVER_PAID_STATUS, _("Over paid")),
    )
    date = models.DateField(_("date"))
    bill_to = models.CharField(_("bill to"), max_length=10, choices=BILL_TO_CHOICES, default=BILL_TO_PATIENT)
    clinic = models.ForeignKey(Clinic, verbose_name=_("clinic"), on_delete=models.PROTECT, related_name="invoices")
    company = models.ForeignKey(
        Company, verbose_name=_("Company"), related_name="invoices", null=True, blank=True, on_delete=models.SET_NULL
    )
    patient = models.ForeignKey(
        Patient,
        verbose_name=_("patient"),
        related_name="invoices",
        on_delete=models.PROTECT,
        help_text="Patient. If no hospital or insurance company is" " declared the bill is for the patient",
    )
    hospital = models.ForeignKey(
        CareTakingFacility,
        verbose_name=_("hospital"),
        null=True,
        related_name="invoices",
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Hospital to bill"),
    )
    ticket = models.CharField(_("ticket"), max_length=15, blank=True, null=True)
    insurance_company = models.ForeignKey(
        InsuranceCompany,
        verbose_name=_("insurance company"),
        null=True,
        blank=True,
        related_name="invoices",
        on_delete=models.SET_NULL,
        help_text="Insurance Company to bill",
    )
    insurance_policy = models.CharField(_("Insurance policy"), max_length=30, null=True, blank=True)
    discount = models.DecimalField(
        _("discount"),
        max_digits=13,
        decimal_places=12,
        help_text=_("Percentage of discount in decimal value."),
        default=Decimal("0.00"),
    )
    discountable_subtotal = models.DecimalField(
        _("discountable subtotal"),
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("Sum of all Billing itemas that are subject to discount"),
    )
    non_discountable_subtotal = models.DecimalField(
        _("non discountable subtotal"),
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("Sum of all Billing itemas that are not subject to discount"),
    )
    total = models.DecimalField(_("total"), max_digits=8, decimal_places=2, default=Decimal("0.00"))
    payment_status = models.CharField(
        _("payment status"), max_length=9, choices=PAYMENT_STATUS_CHOICES, default=UNPAID_STATUS
    )
    commission_paid = models.BooleanField(_("Is commission paid?"), default=False)
    commission_tickets = models.CharField(_("Commission tickets"), max_length=60, null=True, blank=True)

    objects = InvoiceManager()

    class Meta:
        ordering = ("-date", "-created")
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def __str__(self):
        return _("Invoice {} for {} - {}").format(self.id, self.patient, self.total)

    def calculate(self):
        cents = Decimal("0.01")
        use_old = True
        if use_old:
            d_subtotal = Decimal("0.00")
            nd_subtotal = Decimal("0.00")
            for billing_item in self.billing_items.all():
                if billing_item.can_have_discount:
                    d_subtotal += billing_item.charge
                else:
                    nd_subtotal += billing_item.charge
            discount = (self.discount * d_subtotal).quantize(cents, ROUND_HALF_UP)
            total = d_subtotal + nd_subtotal - discount
        else:
            annotated = Invoice.objects.get_with_total(self.id)
            total = annotated.grand_total.quantize(cents, ROUND_HALF_UP)
            nd_subtotal = annotated.non_discountable_sum
            d_subtotal = annotated.discountable_sum

        self.total = total
        self.non_discountable_subtotal = nd_subtotal
        self.discountable_subtotal = d_subtotal
        # if self.amount_paid() == Decimal('0.00'):
        #     self.payment_status = self.PAID_STATUS
        self.set_payment_status()

    def amount_paid(self):
        amount_paid = self.invoice_payments.only("amount").all().aggregate(Sum("amount"))
        paid = Decimal(0.0) if amount_paid["amount__sum"] is None else amount_paid["amount__sum"]
        return paid

    def balance(self):
        paid = self.amount_paid()
        return self.total - paid

    def set_payment_status(self, commit=False):
        balance = self.balance()
        if balance == Decimal(0.0):
            self.payment_status = self.PAID_STATUS
        elif balance == self.total:
            self.payment_status = self.UNPAID_STATUS
        elif balance > Decimal(0.0):
            self.payment_status = self.PARTIAL_STATUS
        else:
            self.payment_status = self.OVER_PAID_STATUS

        if commit:
            self.save()

    def remove_encounter(self, encounter):
        if encounter.invoice == self:
            if self.payment_status == self.PAID_STATUS:
                msg = _("Invoice is paid. You cannot remove encounters from it.")
                raise FinanceException(msg)
            encounter.invoice = None
            encounter.save()
            self.calculate()
            self.save()
        else:
            msg = _("Encounter cannot be removed because it is not part of the bill.")
            raise FinanceException(msg)

    def pay(self, receipt_number, payment_type, user, **kwargs):
        if self.payment_status != self.PAID_STATUS:
            payment_data = dict()
            payment_data["date"] = kwargs.get("date", timezone.now().today())
            payment_data["receipt_number"] = receipt_number
            payment_data["clinic"] = self.clinic
            payment_data["amount"] = kwargs.get("amount", self.total)
            payment_data["payment_type"] = payment_type
            payment_data["bank"] = kwargs.get("bank", None)
            payment_data["transaction_num"] = kwargs.get("transaction_num", None)
            payment_data["created_by"] = user
            payment_data["modified_by"] = user
            with transaction.atomic():
                try:
                    payment = Payment.objects.create(**payment_data)

                    invoice_payment_data = dict()
                    invoice_payment_data["invoice"] = self
                    invoice_payment_data["payment"] = payment
                    invoice_payment_data["amount"] = payment.amount
                    invoice_payment_data["created_by"] = user
                    invoice_payment_data["modified_by"] = user

                    InvoicePayment.objects.create(**invoice_payment_data)

                    self.calculate()
                    self.save()
                    return payment
                except IntegrityError as ie:
                    raise FinanceException(str(ie))
        else:
            msg = _("Cannot pay a paid invoice.")
            raise FinanceException(msg)


class BillingItem(TimeStampedModel):
    date = models.DateTimeField(_("date"))
    patient = models.ForeignKey(
        Patient, verbose_name=_("patient"), related_name="billing_items", on_delete=models.PROTECT
    )
    hospital = models.ForeignKey(
        CareTakingFacility, verbose_name=_("hospital"), null=True, blank=True, on_delete=models.SET_NULL
    )
    ticket = models.CharField(_("ticket"), max_length=15, blank=True, null=True)
    billing_code = models.ForeignKey(
        ClinicBillingCode, verbose_name=_("billing code"), related_name="billing_items", on_delete=models.PROTECT
    )
    charge = models.DecimalField(_("charge"), max_digits=8, decimal_places=2)
    description = models.CharField(
        _("description"), max_length=120, blank=True, help_text="Description for when the billing code is OTHER"
    )
    charge_type = models.ForeignKey(
        ChargeType, on_delete=models.PROTECT, verbose_name=_("charge type"), related_name="billing_items"
    )
    physician = models.ForeignKey(ClinicMember, on_delete=models.PROTECT, verbose_name=_("physician"))
    clinic = models.ForeignKey(Clinic, verbose_name=_("clinic"), on_delete=models.PROTECT)
    invoice = models.ForeignKey(
        Invoice,
        verbose_name=_("invoice"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="billing_items",
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    can_have_discount = models.BooleanField(_("can have discount"), default=True)

    objects = EncounterManager()

    class Meta:
        ordering = ("-date", "-created")
        verbose_name = _("encounter")
        verbose_name_plural = _("encounters")

    def __str__(self):
        return "{} {} {}".format(
            self.billing_code.universal_code.code, self.billing_code.universal_code.description, self.charge
        )


class Payment(Auditable, TimeStampedModel):
    CASH_PAYMENT = "CASH"
    CREDIT_CARD_PAYMENT = "CC"
    DEBIT_CARD_PAYMENT = "DEBIT"
    ACH_PAYMENT = "ACH"
    CHECK_PAYMENT = "CHECK"

    PAYMENT_TYPE_CHOICES = (
        (CASH_PAYMENT, _("Cash")),
        (CREDIT_CARD_PAYMENT, _("Credit Card")),
        (DEBIT_CARD_PAYMENT, _("Debit card")),
        (ACH_PAYMENT, _("ACH")),
        (CHECK_PAYMENT, _("Check")),
    )

    date = models.DateField(_("date"))
    receipt_number = models.CharField(_("receipt number"), max_length=15)
    clinic = models.ForeignKey(Clinic, verbose_name=_("clinic"), related_name="payments", on_delete=models.PROTECT)
    amount = models.DecimalField(_("amount"), max_digits=12, decimal_places=2)
    payment_type = models.CharField(
        _("payment type"), max_length=5, choices=PAYMENT_TYPE_CHOICES, default=CREDIT_CARD_PAYMENT
    )
    bank = models.CharField(_("bank"), max_length=30, null=True, blank=True)
    transaction_num = models.CharField(_("transaction num"), max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return "{} {}".format(self.receipt_number, self.amount)


class InvoicePayment(Auditable, TimeStampedModel):
    invoice = models.ForeignKey(
        Invoice, verbose_name=_("Invoice"), related_name="invoice_payments", on_delete=models.CASCADE
    )
    payment = models.ForeignKey(
        Payment, verbose_name=_("Payment"), related_name="invoice_payments", on_delete=models.CASCADE
    )
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = _("invoice payment")
        verbose_name_plural = _("invoice payments")
