import swapper
from django.contrib import admin
from django.contrib.auth import get_user_model

from django_freeradius.base.admin import (
    AbstractNasAdmin, AbstractRadiusAccountingAdmin, AbstractRadiusBatchAdmin, AbstractRadiusCheckAdmin,
    AbstractRadiusGroupCheckAdmin, AbstractRadiusGroupReplyAdmin, AbstractRadiusPostAuthAdmin,
    AbstractRadiusProfileAdmin, AbstractRadiusReplyAdmin, AbstractRadiusUserGroupAdmin, AbstractUserAdmin,
)

RadiusGroupReply = swapper.load_model("django_freeradius", "RadiusGroupReply")
RadiusGroupCheck = swapper.load_model("django_freeradius", "RadiusGroupCheck")
RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
RadiusReply = swapper.load_model("django_freeradius", "RadiusReply")
RadiusCheck = swapper.load_model("django_freeradius", "RadiusCheck")
RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
Nas = swapper.load_model("django_freeradius", "Nas")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
RadiusBatch = swapper.load_model("django_freeradius", "RadiusBatch")
RadiusProfile = swapper.load_model("django_freeradius", "RadiusProfile")
RadiusUserProfile = swapper.load_model("django_freeradius", "RadiusUserProfile")


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


@admin.register(RadiusBatch)
class RadiusBatchAdmin(AbstractRadiusBatchAdmin):
    pass


@admin.register(RadiusProfile)
class RadiusProfileAdmin(AbstractRadiusProfileAdmin):
    pass


admin.site.unregister(get_user_model())


@admin.register(get_user_model())
class UserAdmin(AbstractUserAdmin):
    pass
