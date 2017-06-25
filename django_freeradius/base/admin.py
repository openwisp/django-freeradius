from django.contrib.admin import ModelAdmin


class TimeStampedEditableAdmin(ModelAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(TimeStampedEditableAdmin, self).get_readonly_fields(request, obj)
        return readonly_fields + ('created', 'modified')


class AbstractRadiusGroupAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupUsersAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusCheckAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusReplyAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusAccountingAdmin(TimeStampedEditableAdmin):
    pass


class AbstractNasAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusUserGroupAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupReplyAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupCheckAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusPostAuthenticationAdmin(TimeStampedEditableAdmin):
    pass
