import swapper
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

from django_freeradius.base.admin import (
    AbstractNasAdmin, AbstractRadiusAccountingAdmin, AbstractRadiusBatchAdmin, AbstractRadiusCheckAdmin,
    AbstractRadiusGroupAdmin, AbstractRadiusGroupCheckAdmin, AbstractRadiusGroupReplyAdmin,
    AbstractRadiusPostAuthAdmin, AbstractRadiusReplyAdmin, AbstractRadiusTokenAdmin,
    AbstractRadiusUserGroupAdmin, AbstractUserAdmin,
)

RadiusCheck = swapper.load_model('django_freeradius', 'RadiusCheck')
RadiusReply = swapper.load_model('django_freeradius', 'RadiusReply')
RadiusGroup = swapper.load_model('django_freeradius', 'RadiusGroup')
RadiusGroupCheck = swapper.load_model('django_freeradius', 'RadiusGroupCheck')
RadiusGroupReply = swapper.load_model('django_freeradius', 'RadiusGroupReply')
RadiusUserGroup = swapper.load_model('django_freeradius', 'RadiusUserGroup')
RadiusAccounting = swapper.load_model('django_freeradius', 'RadiusAccounting')
RadiusPostAuth = swapper.load_model('django_freeradius', 'RadiusPostAuth')
Nas = swapper.load_model('django_freeradius', 'Nas')
RadiusBatch = swapper.load_model('django_freeradius', 'RadiusBatch')
RadiusToken = swapper.load_model('django_freeradius', 'RadiusToken')


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


if settings.DEBUG:
    @admin.register(RadiusToken)
    class RadiusTokenAdmin(AbstractRadiusTokenAdmin):
        pass


admin.site.unregister(get_user_model())


@admin.register(get_user_model())
class UserAdmin(AbstractUserAdmin):
    pass
