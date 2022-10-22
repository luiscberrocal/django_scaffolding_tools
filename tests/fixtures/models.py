from autoslug import AutoSlugField
from django.conf import settings

from django.db.models import JSONField
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from .exceptions import ClinicException
from ..core.models import Human, Auditable
# Create your models here.
from ..patients.models import Patient


def build_slug(physician):
    return '{} {}'.format(physician.last_name, physician.first_name)


def upload_logo(instance, filename):
    extension = filename.split('.')[-1]
    return f'{instance.folder}/{instance.slug}-logo.{extension}'


def get_default_discount_config():
    json_data = settings.EMR_PRACTICE['DEFAULT_DISCOUNT_CONFIG']
    return json_data


class Clinic(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    short_name = models.CharField(_('Short name'), max_length=20, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    folder = AutoSlugField(populate_from='name', unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('Owner'),
                              related_name='owned_clinics')
    logo = models.FileField(upload_to=upload_logo, verbose_name=_('Clinic logo'), null=True, blank=True)
    default_hospital = models.ForeignKey('CareTakingFacility', verbose_name=_('Default Hospital'), null=True,
                                         blank=True, on_delete=models.SET_NULL)
    discount_config = JSONField(_('Discount configuration'), null=True, blank=True, default=get_default_discount_config)
    settings = JSONField(_('Settings'), null=True, blank=True, default=get_default_discount_config)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def add_member(self, clinic_member):
        try:
            return ClinicMembership.objects.create(clinic_member=clinic_member, clinic=self)
        except IntegrityError:
            msg = _('{} is already a member of {}'.format(clinic_member, self))
            raise ClinicException(msg)

    def balance(self):
        from ..finance.models import Invoice
        return Invoice.objects.outstanding_balance(self)


class Company(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    short_name = models.CharField(_('Short name'), max_length=20, null=True, blank=True)
    national_id = models.CharField(_('National id'), max_length=20, null=True, blank=True)
    verification_digit = models.CharField(_('Verification digit'), max_length=4, null=True, blank=True)
    clinic = models.ForeignKey(Clinic, verbose_name=_('Clinic'), related_name='companies', on_delete=models.PROTECT)
    order = models.IntegerField(_('Order'), default=1)
    settings = JSONField(_('Settings'), null=True, blank=True, default=get_default_discount_config)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    folder = AutoSlugField(populate_from='name', unique=True)
    logo = models.ImageField(upload_to=upload_logo, verbose_name=_('Company logo'), null=True, blank=True)

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return self.name


class ClinicMembership(models.Model):
    clinic_member = models.ForeignKey('clinics.ClinicMember', verbose_name=_('Clinic member'), on_delete=models.PROTECT)
    clinic = models.ForeignKey(Clinic, verbose_name=_('Clinic'), on_delete=models.PROTECT)
    settings = JSONField(_('Settings'), null=True, blank=True, default=get_default_discount_config)

    class Meta:
        unique_together = ('clinic_member', 'clinic')


class CareTakingFacility(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('Name'))
    short_name = models.CharField(max_length=60, verbose_name=_('Short name'), null=True, blank=True)
    address = models.TextField(verbose_name=_('Address'))
    google_map_link = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ClinicMember(Human):
    PHYSICIAN_ROLE = 'PHYSICIAN'
    ASSISTANT_ROLE = 'ASSISTANT'
    ROLES = (
        (PHYSICIAN_ROLE, _('Physician')),
        (ASSISTANT_ROLE, _('Assistant'))
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='clinic_member')
    slug = AutoSlugField(populate_from=build_slug)
    role = models.CharField(_('role'), choices=ROLES, default=PHYSICIAN_ROLE, max_length=10)
    clinics = models.ManyToManyField(Clinic, through=ClinicMembership, related_name='members')

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    class Meta:
        ordering = ('last_name', 'first_name')

    def patients(self):
        clinics = ClinicMembership.objects.filter(clinic_member=self).values_list('clinic__id', flat=True)
        return Patient.objects.filter(clinic__in=clinics)


class UniversalBillingCode(TimeStampedModel):
    """
    Universal code for billing and insurance purposes. Billing codes will have a source CPT
    (https://coder.aapc.com/cpt-codes/)
    or Local which in the begining will only include Other.
    """
    CPT_SOURCE = 'CPT'
    LOCAL_SOURCE = 'LOCAL'
    SOURCES = (
        (CPT_SOURCE, _('CPT')),
        (LOCAL_SOURCE, _('Local'))
    )
    source = models.CharField(_('Source'), max_length=8, choices=SOURCES, default=CPT_SOURCE)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    description = models.CharField(_('Description'), max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)

    class Meta:
        ordering = ('code',)


class Diagnostic(Auditable, TimeStampedModel):
    PRIMARY_TYPE = 'PRIM'
    SECONDARY_TYPE = 'SEC'
    TYPE_CHOICES = (
        (PRIMARY_TYPE, _('Primary')),
        (SECONDARY_TYPE, _('Secondary')),
    )
    type = models.CharField(_('Type'), max_length=10, choices=TYPE_CHOICES, default=PRIMARY_TYPE)
    code = models.CharField(_('Code'), max_length=15, unique=True)
    description = models.CharField(_('Description'), max_length=150)

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)

    class Meta:
        ordering = ('description',)


class Procedure(Auditable, TimeStampedModel):
    code = models.CharField(_('Code'), max_length=15, unique=True)
    description = models.CharField(_('Description'), max_length=150)

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)

    class Meta:
        ordering = ('description',)


class ClinicDiagnostic(Auditable, TimeStampedModel):
    type = models.CharField(_('Type'), max_length=10, null=True, choices=Diagnostic.TYPE_CHOICES)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, verbose_name=_('Clinic'),
                               related_name='clinic_diagnostics')
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.PROTECT, verbose_name=_('Diagnostic'),
                                   related_name='clinic_diagnostics')

    class Meta:
        ordering = ('clinic', 'diagnostic__code')

    def __str__(self):
        if self.type is None:
            return '{} - {}'.format(self.diagnostic.code, self.diagnostic.description)
        else:
            return '{} ({}) - {}'.format(self.type, self.diagnostic.code, self.diagnostic.description)


class ClinicProcedure(Auditable, TimeStampedModel):
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, verbose_name=_('Clinic'),
                               related_name='clinic_procedures')
    procedure = models.ForeignKey(Procedure, on_delete=models.PROTECT, verbose_name=_('Procedure'),
                                  related_name='clinic_procedures')

    class Meta:
        ordering = ('clinic', 'procedure__code')
        unique_together = ('clinic', 'procedure')

    def __str__(self):
        return '{} - {}'.format(self.procedure.code, self.procedure.description)
