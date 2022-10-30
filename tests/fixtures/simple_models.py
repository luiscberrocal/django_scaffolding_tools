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
