from django.contrib.admin import ModelAdmin

from .. import settings


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
    search_fields = ['name', 'short_name', 'server']
    list_display = ['name', 'short_name', 'server', 'secret', 'created', 'modified']


class AbstractRadiusUserGroupAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupReplyAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupCheckAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusPostAuthAdmin(ModelAdmin):
    list_display = ['username', 'reply', 'date']
    list_filter = ['date']
    search_fields = ['username', 'reply']

    if not settings.EDITABLE_POSTAUTH:
        readonly_fields = ['username', 'password', 'reply', 'date']

        def has_add_permission(self, request):
            return False

        def change_view(self, request, object_id, extra_context=None):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
            return super(AbstractRadiusPostAuthAdmin, self).change_view(request,
                                                                        object_id,
                                                                        extra_context=extra_context)
