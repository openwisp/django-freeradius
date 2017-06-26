from django.contrib import admin

from .base.admin import (
    AbstractNasAdmin, AbstractRadiusAccountingAdmin, AbstractRadiusCheckAdmin, AbstractRadiusGroupAdmin,
    AbstractRadiusGroupCheckAdmin, AbstractRadiusGroupReplyAdmin, AbstractRadiusGroupUsersAdmin,
    AbstractRadiusPostAuthenticationAdmin, AbstractRadiusReplyAdmin, AbstractRadiusUserGroupAdmin,
)
from .models import (
    Nas, RadiusAccounting, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
    RadiusPostAuthentication, RadiusReply, RadiusUserGroup,
)


@admin.register(RadiusGroup)
class RadiusGroupAdmin(AbstractRadiusGroupAdmin):
    model = RadiusGroup


@admin.register(RadiusGroupUsers)
class RadiusGroupUsersAdmin(AbstractRadiusGroupUsersAdmin):
    model = RadiusGroupUsers


@admin.register(RadiusCheck)
class RadiusCheckAdmin(AbstractRadiusCheckAdmin):
    model = RadiusCheck


@admin.register(RadiusReply)
class RadiusReplyAdmin(AbstractRadiusReplyAdmin):
    model = RadiusReply


@admin.register(RadiusAccounting)
class RadiusAccountingAdmin(AbstractRadiusAccountingAdmin):
    model = RadiusAccounting


@admin.register(Nas)
class NasAdmin(AbstractNasAdmin):
    model = Nas


@admin.register(RadiusUserGroup)
class RadiusUserGroupAdmin(AbstractRadiusUserGroupAdmin):
    model = RadiusUserGroup


@admin.register(RadiusGroupReply)
class RadiusGroupReplyAdmin(AbstractRadiusGroupReplyAdmin):
    model = RadiusGroupReply


@admin.register(RadiusGroupCheck)
class RadiusGroupCheckAdmin(AbstractRadiusGroupCheckAdmin):
    model = RadiusGroupCheck


@admin.register(RadiusPostAuthentication)
class RadiusPostAuthenticationAdmin(AbstractRadiusPostAuthenticationAdmin):
    model = RadiusPostAuthentication
