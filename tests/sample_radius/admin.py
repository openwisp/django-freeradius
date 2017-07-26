import swapper
from django.contrib import admin

from django_freeradius.admin import (
    AbstractNasAdmin, AbstractRadiusAccountingAdmin, AbstractRadiusCheckAdmin, AbstractRadiusGroupAdmin,
    AbstractRadiusGroupCheckAdmin, AbstractRadiusGroupReplyAdmin, AbstractRadiusGroupUsersAdmin,
    AbstractRadiusPostAuthAdmin, AbstractRadiusReplyAdmin, AbstractRadiusUserGroupAdmin,
)

RadiusGroupReply = swapper.load_model("django_freeradius", "RadiusGroupReply")
RadiusGroupCheck = swapper.load_model("django_freeradius", "RadiusGroupCheck")
RadiusGroupUsers = swapper.load_model("django_freeradius", "RadiusGroupUsers")
RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
RadiusReply = swapper.load_model("django_freeradius", "RadiusReply")
RadiusCheck = swapper.load_model("django_freeradius", "RadiusCheck")
RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
Nas = swapper.load_model("django_freeradius", "Nas")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
RadiusGroup = swapper.load_model("django_freeradius", "RadiusGroup")


@admin.register(RadiusGroup)
class RadiusGroupAdmin(AbstractRadiusGroupAdmin):
    pass


@admin.register(RadiusGroupUsers)
class RadiusGroupUsersAdmin(AbstractRadiusGroupUsersAdmin):
    pass


@admin.register(RadiusCheck)
class RadiusCheckAdmin(AbstractRadiusCheckAdmin):
    pass


@admin.register(RadiusReply)
class RadiusReplyAdmin(AbstractRadiusReplyAdmin):
    pass


@admin.register(RadiusAccounting)
class RadiusAccountingAdmin(AbstractRadiusAccountingAdmin):
    pass


@admin.register(Nas)
class NasAdmin(AbstractNasAdmin):
    pass


@admin.register(RadiusUserGroup)
class RadiusUserGroupAdmin(AbstractRadiusUserGroupAdmin):
    pass


@admin.register(RadiusGroupReply)
class RadiusGroupReplyAdmin(AbstractRadiusGroupReplyAdmin):
    pass


@admin.register(RadiusGroupCheck)
class RadiusGroupCheckAdmin(AbstractRadiusGroupCheckAdmin):
    pass


@admin.register(RadiusPostAuth)
class RadiusPostAuthAdmin(AbstractRadiusPostAuthAdmin):
    pass
