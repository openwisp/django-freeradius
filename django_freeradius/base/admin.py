from django.contrib.admin import ModelAdmin


class TimeStampedEditableAdmin(ModelAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """
    def __init__(self, *args, **kwargs):
        self.readonly_fields += ('modified')
        super(TimeStampedEditableAdmin, self).__init__(*args, **kwargs)


class AbstractRadiusGroupAdmin(ModelAdmin):
    pass


class AbstractRadiusGroupUsersAdmin(ModelAdmin):
    pass


class AbstractRadiusCheckAdmin(ModelAdmin):
    pass


class AbstractRadiusReplyAdmin(ModelAdmin):
    pass


class AbstractRadiusAccountingAdmin(ModelAdmin):
    pass


class AbstractNasAdmin(ModelAdmin):
    pass


class AbstractRadiusUserGroupAdmin(ModelAdmin):
    pass


class AbstractRadiusGroupReplyAdmin(ModelAdmin):
    pass


class AbstractRadiusGroupCheckAdmin(ModelAdmin):
    pass


class AbstractRadiusPostAuthenticationAdmin(ModelAdmin):
    pass
