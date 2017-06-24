from django.contrib import admin

import swapper
from django_freeradius.admin import (AbstractNasAdmin,
                                     AbstractRadiusAccountingAdmin,
                                     AbstractRadiusCheckAdmin,
                                     AbstractRadiusGroupAdmin,
                                     AbstractRadiusGroupCheckAdmin,
                                     AbstractRadiusGroupReplyAdmin,
                                     AbstractRadiusGroupUsersAdmin,
                                     AbstractRadiusPostAuthenticationAdmin,
                                     AbstractRadiusReplyAdmin,
                                     AbstractRadiusUserGroupAdmin)

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
