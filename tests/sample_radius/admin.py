from django.contrib import admin

from django_freeradius.admin import (AbstractNasAdmin, AbstractRadiusAccountingAdmin,
                                     AbstractRadiusCheckAdmin, AbstractRadiusGroupAdmin,
                                     AbstractRadiusGroupCheckAdmin,
                                     AbstractRadiusGroupReplyAdmin,
                                     AbstractRadiusGroupUsersAdmin,
                                     AbstractRadiusPostAuthenticationAdmin,
                                     AbstractRadiusReplyAdmin,
                                     AbstractRadiusUserGroupAdmin)

from django_freeradius.models import (Nas, RadiusAccounting, RadiusCheck, RadiusGroup,
                                      RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
                                      RadiusPostAuthentication, RadiusReply, RadiusUserGroup)
