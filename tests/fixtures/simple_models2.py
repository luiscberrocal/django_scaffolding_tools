from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.config import settings

# Create your models here.


class Clinic(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Created by'),
                                   help_text=_('User who created the record'), on_delete=models.PROTECT,
                                   related_name='contracts_created')


class Patient(models.Model):
    first_name = models.CharField(_('First name'), max_length=100, help_text="Patient's fist name")
    last_name = models.CharField(_('Last name'), max_length=100)
    owning_clinic = models.ForeignKey(Clinic, verbose_name=_('Clinic'), related_name='companies',
                                      on_delete=models.PROTECT)
