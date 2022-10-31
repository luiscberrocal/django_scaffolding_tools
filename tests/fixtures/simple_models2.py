from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Clinic(models.Model):
    name = models.CharField(_('Name'), max_length=100)


class Patient(models.Model):
    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('Last name'), max_length=100)
    clinic = models.ForeignKey(Clinic, verbose_name=_('Clinic'), related_name='companies', on_delete=models.PROTECT)
