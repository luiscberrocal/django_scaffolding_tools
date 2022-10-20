import uuid

from typing import Any, Dict

from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel
from pj_d_local_sdk.models import PaymentResponse
from pj_d_local_sdk.pay_ins.payments import PaymentManager

from .d_local import send_payment_to_d_local
from .enums import PaymentState

STATE_CHANGES = 'state_changes'


def get_response_default_dict() -> Dict[str, Any]:
    return {'request': '', 'callback': ''}


def get_metadata_default_dict() -> Dict[str, Any]:
    """Default dictionary to keep track of changes in state. Add a dictionary containing the date the state
    changed. For example:
    metadata['state_changes'][PaymentState.SENT_TO_PROVIDER.value].append({'date':'2022-08-08T15:45:00+00:00'})"""
    metadata = dict()
    metadata[STATE_CHANGES] = dict()
    metadata[STATE_CHANGES][PaymentState.SENT_TO_PROVIDER.value] = []
    metadata[STATE_CHANGES][PaymentState.PROVIDER_RESPONDED.value] = []
    metadata[STATE_CHANGES][PaymentState.RESPONDED_TO_CALLER.value] = []
    metadata[STATE_CHANGES][PaymentState.NOTIFICATION_RECEIVED.value] = []
    metadata[STATE_CHANGES][PaymentState.NOTIFICATION_SENT_TO_CALLER.value] = []
    metadata[STATE_CHANGES][PaymentState.CLOSED.value] = []

    return metadata


class Payer(TimeStampedModel):
    """D-Local representation of a Customer. The country attribute was added to avoid future collitions with
    repeated country. This occurred in between Colombia and Peru national ids."""
    name = models.CharField(_('Name'), max_length=100)
    email = models.CharField(_('Email'), max_length=100)
    document = models.CharField(_('Document'), max_length=100,
                                help_text=_('User’s personal identification number. '
                                            'To see the document code list per country, '
                                            'go to the Country Reference page.'))
    country = models.CharField(_('Country'), max_length=2,
                               help_text=_('This will contain the two letter country code'
                                           ' of the country the device was sold in.'))

    def __str__(self):
        return f'{self.name} ({self.document})'

    class Meta:
        unique_together = ('document', 'country')


class Payment(TimeStampedModel):
    """Represents a payment sent from M3 and resolved or rejected by D-Local."""
    payer = models.ForeignKey(Payer, verbose_name=_('Payer'), on_delete=models.PROTECT,
                              related_name='payments')
    credit_line_id = models.CharField(_('Credit line id'), max_length=64,
                                      help_text=_('Unique identifier for a credit line or a finance order.'))
    finance_engine_version = models.CharField(_('Finance engine version'), max_length=5,
                                              help_text=_('Finance engine version FEv1 or FEv2'))
    user_id = models.CharField(_('User id'), max_length=50,
                               help_text=_('This will contain the foreign key to the Users table in '
                                           'M2 or the Persons table in M3'))
    device_id = models.CharField(_('Device id'), max_length=50,
                                 help_text=_('This will contain the foreign key to the Devices table'))
    merchant_id = models.CharField(_('Merchant id'), max_length=64, null=True, blank=True,
                                   help_text=_('Reference to the Merchants table - ONLY '
                                               'FEv2 needs to publish this information'))
    clerk_id = models.CharField(_('Clerk id'), max_length=50, null=True, blank=True,
                                help_text=_('This will contain the foreign key to the clerk who sold the device'))
    finance_provider = models.CharField(_('Finance provider'), max_length=50,
                                        help_text=_('Constants representing the finance provider.'))
    payment_provider = models.CharField(_('Payment provider'), max_length=16)
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    currency = models.CharField(_('Currency'), max_length=3,
                                help_text=_("The three letter currency code abbreviation."))
    country = models.CharField(_('Country'), max_length=2,
                               help_text=_('This will contain the two letter country code'
                                           ' of the country the device was sold in.'))
    payment_method_id = models.CharField(_('Payment method id'), max_length=3,
                                         help_text=_('Payment method defined by D-Local.'))
    payment_method_flow = models.CharField(_('Payment method flow'), max_length=15,
                                           help_text=_('D-Local payment flow usually DIRECT or REDIRECT.'))
    order_id = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
    notification_url = models.URLField(_('Notification url'))
    payment_status = models.CharField(_('Payment status'), max_length=15, null=True, blank=True,
                                      help_text=_('The values should match pj_d_local_sdk.enums.PaymentStatus values.'))

    response = models.JSONField(_('Response'), default=get_response_default_dict,
                                help_text=_("Response from D-Local API. Will contain 2 keys for "
                                            "request response and callback response"))
    state = FSMField(_('State'), protected=True, default=PaymentState.CREATED)
    metadata = models.JSONField(_('Metadata'), default=get_metadata_default_dict,
                                help_text=_('Metadata for the payment. It includes the dates with'
                                            ' the changes of state.'))

    @transition(field=state, source=PaymentState.CREATED, target=PaymentState.SENT_TO_PROVIDER)
    def send_to_provider(self, payment_manager_instance: PaymentManager) -> PaymentResponse:
        """This method will call the D-Local endpoint and return a pj_d_local_sdk.models.PaymentResponse object"""
        payment_response = send_payment_to_d_local(self, payment_manager_instance)
        return payment_response

    @transition(field=state, source=PaymentState.SENT_TO_PROVIDER, target=PaymentState.RESPONDED_TO_CALLER)
    def responded_m3(self):
        pass

    def __str__(self):
        return f'Order id: {self.order_id}'

    class Meta:
        ordering = ('-created',)
