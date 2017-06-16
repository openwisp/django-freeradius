from django.contrib.admin import ModelAdmin


class TimeStampedEditableAdmin(ModelAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """
    def __init__(self, *args, **kwargs):
        self.readonly_fields += ('created', 'modified',)
        super(TimeStampedEditableAdmin, self).__init__(*args, **kwargs)


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
