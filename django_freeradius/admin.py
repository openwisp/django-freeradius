from django.contrib import admin
from django.contrib.auth import get_user_model

from .base.admin import (
    AbstractNasAdmin, AbstractRadiusAccountingAdmin, AbstractRadiusBatchAdmin, AbstractRadiusCheckAdmin,
    AbstractRadiusGroupAdmin, AbstractRadiusGroupCheckAdmin, AbstractRadiusGroupReplyAdmin,
    AbstractRadiusGroupUsersAdmin, AbstractRadiusPostAuthAdmin, AbstractRadiusProfileAdmin,
    AbstractRadiusReplyAdmin, AbstractRadiusUserGroupAdmin, AbstractUserAdmin,
)
from .models import (
    Nas, RadiusAccounting, RadiusBatch, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply,
    RadiusGroupUsers, RadiusPostAuth, RadiusProfile, RadiusReply, RadiusUserGroup,
)


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


@admin.register(RadiusBatch)
class RadiusBatchAdmin(AbstractRadiusBatchAdmin):
    pass


@admin.register(RadiusProfile)
class RadiusProfileAdmin(AbstractRadiusProfileAdmin):
    pass


user_model = get_user_model()
admin.site.unregister(user_model)


@admin.register(user_model)
class UserAdmin(AbstractUserAdmin):
    pass
