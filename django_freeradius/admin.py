from django.contrib import admin

from .models import (Nas, RadiusAccounting, RadiusChecks, RadiusGroup, RadiusGroupUsers, RadiusReplies)


@admin.register(RadiusGroup)
class RadiusGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(RadiusGroupUsers)
class RadiusGroupUsers(admin.ModelAdmin):
    pass


@admin.register(RadiusChecks)
class RadiusChecks(admin.ModelAdmin):
    pass


@admin.register(RadiusReplies)
class RadiusReplies(admin.ModelAdmin):
    pass


@admin.register(RadiusAccounting)
class RadiusAccounting(admin.ModelAdmin):
    pass


@admin.register(Nas)
class Nas(admin.ModelAdmin):
    pass
