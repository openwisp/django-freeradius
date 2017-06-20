from django.db import models
from django.utils.translation import ugettext_lazy as _
import swapper
from django_freeradius.models import (AbstractNas, AbstractRadiusAccounting,
                                      AbstractRadiusCheck, AbstractRadiusGroup,
                                      AbstractRadiusGroupCheck, AbstractRadiusGroupReply,
                                      AbstractRadiusGroupUsers,
                                      AbstractRadiusPostAuthentication,
                                      AbstractRadiusReply, AbstractRadiusUserGroup)

RadiusGroupReply = swapper.load_model("django_freeradius", "RadiusGroupReply")
RadiusGroupCheck = swapper.load_model("django_freeradius", "RadiusGroupCheck")
RadiusGroupUsers = swapper.load_model("django_freeradius", "RadiusGroupUsers")
RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
RadiusReply = swapper.load_model("django_freeradius", "RadiusReply")
RadiusCheck = swapper.load_model("django_freeradius", "RadiusCheck")
RadiusPostAuthentication = swapper.load_model("django_freeradius", "RadiusPostAuthentication")
Nas = swapper.load_model("django_freeradius", "Nas")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
RadiusGroup = swapper.load_model("django_freeradius", "RadiusGroup")


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
