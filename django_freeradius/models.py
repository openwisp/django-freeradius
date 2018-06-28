from django.contrib.auth import get_user_model
from django.db.models import signals
from swapper import swappable_setting

from django_freeradius.utils import set_default_limits

from .base.models import (
    AbstractNas, AbstractRadiusAccounting, AbstractRadiusBatch, AbstractRadiusCheck, AbstractRadiusGroup,
    AbstractRadiusGroupCheck, AbstractRadiusGroupReply, AbstractRadiusGroupUsers, AbstractRadiusPostAuth,
    AbstractRadiusProfile, AbstractRadiusReply, AbstractRadiusUserGroup, AbstractRadiusUserProfile,
)


class RadiusGroup(AbstractRadiusGroup):
    class Meta(AbstractRadiusGroup.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusGroup')


class RadiusGroupUsers(AbstractRadiusGroupUsers):
    class Meta(AbstractRadiusGroupUsers.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusGroupUsers')


class RadiusCheck(AbstractRadiusCheck):
    class Meta(AbstractRadiusCheck.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusCheck')


class RadiusAccounting(AbstractRadiusAccounting):
    class Meta(AbstractRadiusAccounting.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusAccounting')


class RadiusReply(AbstractRadiusReply):
    class Meta(AbstractRadiusReply.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusReply')


class Nas(AbstractNas):
    class Meta(AbstractNas.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'Nas')


class RadiusGroupCheck(AbstractRadiusGroupCheck):
    class Meta(AbstractRadiusGroupCheck.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusGroupCheck')


class RadiusGroupReply(AbstractRadiusGroupReply):
    class Meta(AbstractRadiusGroupReply.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusGroupReply')


class RadiusPostAuth(AbstractRadiusPostAuth):
    class Meta(AbstractRadiusPostAuth.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusPostAuth')


class RadiusUserGroup(AbstractRadiusUserGroup):
    class Meta(AbstractRadiusUserGroup.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusUserGroup')


class RadiusBatch(AbstractRadiusBatch):
    class Meta(AbstractRadiusBatch.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusBatch')


class RadiusProfile(AbstractRadiusProfile):
    class Meta(AbstractRadiusProfile.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusProfile')


class RadiusUserProfile(AbstractRadiusUserProfile):
    class Meta(AbstractRadiusUserProfile.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusUserProfile')


signals.post_save.connect(set_default_limits, sender=get_user_model())
