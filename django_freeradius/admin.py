from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

from . import settings as app_settings
from .base.admin import (
    AbstractNasAdmin, AbstractRadiusAccountingAdmin, AbstractRadiusBatchAdmin, AbstractRadiusCheckAdmin,
    AbstractRadiusGroupAdmin, AbstractRadiusGroupCheckAdmin, AbstractRadiusGroupReplyAdmin,
    AbstractRadiusPostAuthAdmin, AbstractRadiusReplyAdmin, AbstractRadiusTokenAdmin,
    AbstractRadiusUserGroupAdmin, AbstractUserAdmin,
)
from .models import (
    Nas, RadiusAccounting, RadiusBatch, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply,
    RadiusPostAuth, RadiusReply, RadiusToken, RadiusUserGroup,
)


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


@admin.register(RadiusGroup)
class RadiusGroupAdmin(AbstractRadiusGroupAdmin):
    pass


if app_settings.USERGROUP_ADMIN:
    @admin.register(RadiusUserGroup)
    class RadiusUserGroupAdmin(AbstractRadiusUserGroupAdmin):
        pass


if app_settings.GROUPREPLY_ADMIN:
    @admin.register(RadiusGroupReply)
    class RadiusGroupReplyAdmin(AbstractRadiusGroupReplyAdmin):
        pass


if app_settings.GROUPCHECK_ADMIN:
    @admin.register(RadiusGroupCheck)
    class RadiusGroupCheckAdmin(AbstractRadiusGroupCheckAdmin):
        pass


@admin.register(RadiusPostAuth)
class RadiusPostAuthAdmin(AbstractRadiusPostAuthAdmin):
    pass


@admin.register(RadiusBatch)
class RadiusBatchAdmin(AbstractRadiusBatchAdmin):
    pass


if settings.DEBUG:
    @admin.register(RadiusToken)
    class RadiusTokenAdmin(AbstractRadiusTokenAdmin):
        pass

user_model = get_user_model()
admin.site.unregister(user_model)


@admin.register(user_model)
class UserAdmin(AbstractUserAdmin):
    pass
