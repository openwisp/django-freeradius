from swapper import swappable_setting

from .base.models import (
    AbstractNas, AbstractRadiusAccounting, AbstractRadiusCheck, AbstractRadiusGroup,
    AbstractRadiusGroupCheck, AbstractRadiusGroupReply, AbstractRadiusGroupUsers,
    AbstractRadiusPostAuthentication, AbstractRadiusReply, AbstractRadiusUserGroup,
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


class RadiusPostAuthentication(AbstractRadiusPostAuthentication):

    class Meta(AbstractRadiusPostAuthentication.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusPostAuthentication')


class RadiusUserGroup(AbstractRadiusUserGroup):

    class Meta(AbstractRadiusUserGroup.Meta):
        abstract = False
        swappable = swappable_setting('django_freeradius', 'RadiusUserGroup')
