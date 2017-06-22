from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_freeradius.models import (AbstractNas, AbstractRadiusAccounting,
                                      AbstractRadiusCheck, AbstractRadiusGroup,
                                      AbstractRadiusGroupCheck, AbstractRadiusGroupReply,
                                      AbstractRadiusGroupUsers,
                                      AbstractRadiusPostAuthentication,
                                      AbstractRadiusReply, AbstractRadiusUserGroup)


class RadiusGroup(AbstractRadiusGroup):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusCheck(AbstractRadiusCheck):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusAccounting(AbstractRadiusAccounting):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusReply(AbstractRadiusReply):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusGroupCheck(AbstractRadiusGroupCheck):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusGroupReply(AbstractRadiusGroupReply):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusPostAuthentication(AbstractRadiusPostAuthentication):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusUserGroup(AbstractRadiusUserGroup):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class Nas(AbstractNas):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)


class RadiusGroupUsers(AbstractRadiusGroupUsers):
    details = models.CharField(
            verbose_name=_('details'), max_length=64, blank=True, null=True)
