from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_freeradius.base.models import (
    AbstractNas, AbstractRadiusAccounting, AbstractRadiusBatch, AbstractRadiusCheck, AbstractRadiusGroup,
    AbstractRadiusGroupCheck, AbstractRadiusGroupReply, AbstractRadiusPostAuth, AbstractRadiusReply,
    AbstractRadiusToken, AbstractRadiusUserGroup,
)


class DetailsModel(models.Model):
    details = models.CharField(verbose_name=_('details'), max_length=64, blank=True, null=True)

    class Meta:
        abstract = True


class RadiusCheck(DetailsModel, AbstractRadiusCheck):
    pass


class RadiusAccounting(DetailsModel, AbstractRadiusAccounting):
    pass


class RadiusReply(DetailsModel, AbstractRadiusReply):
    pass


class RadiusGroup(DetailsModel, AbstractRadiusGroup):
    pass


class RadiusUserGroup(DetailsModel, AbstractRadiusUserGroup):
    pass


class RadiusGroupCheck(DetailsModel, AbstractRadiusGroupCheck):
    pass


class RadiusGroupReply(DetailsModel, AbstractRadiusGroupReply):
    pass


class RadiusPostAuth(DetailsModel, AbstractRadiusPostAuth):
    pass


class Nas(DetailsModel, AbstractNas):
    pass


class RadiusBatch(DetailsModel, AbstractRadiusBatch):
    pass


class RadiusToken(DetailsModel, AbstractRadiusToken):
    pass
