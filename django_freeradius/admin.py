from django.contrib import admin

from .models import (Nas, RadiusAccounting, RadiusCheck, RadiusGroup,
                     RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
                     RadiusPostAuthentication, RadiusReply, RadiusUserGroup)


@admin.register(RadiusGroup)
class RadiusGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(RadiusGroupUsers)
class RadiusGroupUsers(admin.ModelAdmin):
    pass


@admin.register(RadiusCheck)
class RadiusCheck(admin.ModelAdmin):
    pass


@admin.register(RadiusReply)
class RadiusReply(admin.ModelAdmin):
    pass


@admin.register(RadiusAccounting)
class RadiusAccounting(admin.ModelAdmin):
    pass


@admin.register(Nas)
class Nas(admin.ModelAdmin):
    pass


@admin.register(RadiusUserGroup)
class RadiusUserGroup(admin.ModelAdmin):
    pass


@admin.register(RadiusGroupReply)
class RadiusGroupReply(admin.ModelAdmin):
    pass


@admin.register(RadiusGroupCheck)
class RadiusGroupCheck(admin.ModelAdmin):
    pass


@admin.register(RadiusPostAuthentication)
class RadiusPostAuthentication(admin.ModelAdmin):
    pass
