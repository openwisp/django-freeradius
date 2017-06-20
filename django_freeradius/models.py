import swapper

from .base.models import (AbstractNas, AbstractRadiusAccounting,
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

    class Meta(AbstractRadiusGroup.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroup')


class RadiusGroupUsers(AbstractRadiusGroupUsers):

    class Meta(AbstractRadiusGroupUsers.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroupUsers')


class RadiusCheck(AbstractRadiusCheck):

    class Meta(AbstractRadiusCheck.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusCheck')


class RadiusAccounting(AbstractRadiusAccounting):

    class Meta(AbstractRadiusAccounting.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusAccounting')


class RadiusReply(AbstractRadiusReply):

    class Meta(AbstractRadiusReply.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusReply')


class Nas(AbstractNas):

    class Meta(AbstractNas.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'Nas')


class RadiusGroupCheck(AbstractRadiusGroupCheck):

    class Meta(AbstractRadiusGroupCheck.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroupCheck')


class RadiusGroupReply(AbstractRadiusGroupReply):

    class Meta(AbstractRadiusGroupReply.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusGroupReply')


class RadiusPostAuthentication(AbstractRadiusPostAuthentication):

    class Meta(AbstractRadiusPostAuthentication.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusPostAuthentication')


class RadiusUserGroup(AbstractRadiusUserGroup):

    class Meta(AbstractRadiusUserGroup.Meta):
        abstract = False
        swappable = swapper.swappable_setting('django_freeradius', 'RadiusUserGroup')
