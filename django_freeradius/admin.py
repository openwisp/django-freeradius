from django.contrib import admin

from .models import (Nas, RadiusAccounting, RadiusCheck, RadiusGroup,
                     RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
                     RadiusPostAuthentication, RadiusReply, RadiusUserGroup)

from .base.admin import (AbstractRadiusGroupAdmin, AbstractRadiusGroupUsersAdmin,
                         AbstractRadiusCheckAdmin, AbstractRadiusAccountingAdmin,
                         AbstractRadiusReplyAdmin, AbstractNasAdmin,
                         AbstractRadiusGroupCheckAdmin, AbstractRadiusGroupReplyAdmin,
                         AbstractRadiusPostAuthenticationAdmin, AbstractRadiusUserGroupAdmin)


class RadiusGroupAdmin(AbstractRadiusGroupAdmin):
    model = RadiusGroup


class RadiusGroupUsersAdmin(AbstractRadiusGroupUsersAdmin):
    model = RadiusGroupUsers


class RadiusCheckAdmin(AbstractRadiusCheckAdmin):
    model = RadiusCheck


class RadiusReplyAdmin(AbstractRadiusReplyAdmin):
    model = RadiusReply


class RadiusAccountingAdmin(AbstractRadiusAccountingAdmin):
    model = RadiusAccounting


class NasAdmin(AbstractNasAdmin):
    model = Nas


class RadiusUserGroupAdmin(AbstractRadiusUserGroupAdmin):
    model = RadiusUserGroup


class RadiusGroupReplyAdmin(AbstractRadiusGroupReplyAdmin):
    model = RadiusGroupReply


class RadiusGroupCheckAdmin(AbstractRadiusGroupCheckAdmin):
    model = RadiusGroupCheck


class RadiusPostAuthenticationAdmin(AbstractRadiusPostAuthenticationAdmin):
    model = RadiusPostAuthentication


admin.site.register(RadiusPostAuthentication, RadiusPostAuthenticationAdmin)
admin.site.register(RadiusGroupCheck, RadiusGroupCheckAdmin)
admin.site.register(RadiusGroupReply, RadiusGroupReplyAdmin)
admin.site.register(RadiusUserGroup, RadiusUserGroupAdmin)
admin.site.register(Nas, NasAdmin)
admin.site.register(RadiusAccounting, RadiusAccountingAdmin)
admin.site.register(RadiusReply, RadiusReplyAdmin)
admin.site.register(RadiusCheck, RadiusCheckAdmin)
admin.site.register(RadiusGroupUsers, RadiusGroupUsersAdmin)
admin.site.register(RadiusGroup, RadiusGroupAdmin)
