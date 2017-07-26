from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_freeradius.models import (
    AbstractNas, AbstractRadiusAccounting, AbstractRadiusCheck, AbstractRadiusGroup,
    AbstractRadiusGroupCheck, AbstractRadiusGroupReply, AbstractRadiusGroupUsers, AbstractRadiusPostAuth,
    AbstractRadiusReply, AbstractRadiusUserGroup,
)


class DetailsModel(models.Model):
    details = models.CharField(verbose_name=_('details'), max_length=64, blank=True, null=True)

    class Meta:
        abstract = True


class RadiusGroup(DetailsModel, AbstractRadiusGroup):
    pass


class RadiusCheck(DetailsModel, AbstractRadiusCheck):
    pass


class RadiusAccounting(DetailsModel, AbstractRadiusAccounting):
    pass


class RadiusReply(DetailsModel, AbstractRadiusReply):
    pass


class RadiusGroupCheck(DetailsModel, AbstractRadiusGroupCheck):
    pass


class RadiusGroupReply(DetailsModel, AbstractRadiusGroupReply):
    pass


class RadiusPostAuth(DetailsModel, AbstractRadiusPostAuth):
    pass


class RadiusUserGroup(DetailsModel, AbstractRadiusUserGroup):
    pass


class Nas(DetailsModel, AbstractNas):
    pass


class RadiusGroupUsers(DetailsModel, AbstractRadiusGroupUsers):
    pass
