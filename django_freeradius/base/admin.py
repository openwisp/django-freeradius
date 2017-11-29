from django.contrib.admin import ModelAdmin
from passlib.hash import lmhash, nthash

from .. import settings as app_settings
from .admin_filters import DuplicateListFilter
from .forms import AbstractRadiusCheckAdminForm


class TimeStampedEditableAdmin(ModelAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(TimeStampedEditableAdmin, self).get_readonly_fields(request, obj)
        return readonly_fields + ('created', 'modified')


class ReadOnlyAdmin(ModelAdmin):
    """
    Disables all editing capabilities
    """
    def __init__(self, *args, **kwargs):
        super(ReadOnlyAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [f.name for f in self.model._meta.fields]

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)
        del actions["delete_selected"]
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):  # pragma: nocover
        pass

    def delete_model(self, request, obj):  # pragma: nocover
        pass

    def save_related(self, request, form, formsets, change):  # pragma: nocover
        pass

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(ReadOnlyAdmin, self).change_view(request,
                                                      object_id,
                                                      extra_context=extra_context)


class AbstractRadiusGroupAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupUsersAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusCheckAdmin(TimeStampedEditableAdmin):
    list_display = (
                    'username', 'attribute', 'is_active',
                    'created', 'valid_until',
                   )
    search_fields = ('username', 'value')
    list_filter = (DuplicateListFilter, 'created', 'modified', 'valid_until')
    readonly_fields = ('value',)
    form = AbstractRadiusCheckAdminForm
    fields = ('username', 'value', 'op', 'attribute', 'new_value',
              'is_active', 'valid_until', 'note', 'created', 'modified')

    # if new_value is present this will be hashed and stored into value
    def save_model(self, request, obj, form, change):
        password_renewed = form.data['new_value']
        password_format = form.data['attribute']
        if password_renewed:
            if password_format == 'Cleartext-Password':
                obj.value = password_renewed
            elif password_format == 'NT-Password':
                obj.value = nthash.hash(password_renewed)
            elif password_format == 'LM-Password':
                obj.value = lmhash.hash(password_renewed)
        obj.save()


class AbstractRadiusReplyAdmin(TimeStampedEditableAdmin):
    pass


BaseAccounting = ReadOnlyAdmin if not app_settings.EDITABLE_ACCOUNTING else ModelAdmin


class AbstractRadiusAccountingAdmin(BaseAccounting):
    list_display = ('nas_ip_address', 'username', 'session_time',
                    'input_octets', 'output_octets',
                    'start_time', 'stop_time')
    search_fields = ('unique_id', 'username', 'nas_ip_address')
    list_filter = ('start_time', 'stop_time')


class AbstractNasAdmin(TimeStampedEditableAdmin):
    search_fields = ['name', 'short_name', 'server']
    list_display = ['name', 'short_name', 'server', 'secret', 'created', 'modified']


class AbstractRadiusUserGroupAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupReplyAdmin(TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupCheckAdmin(TimeStampedEditableAdmin):
    pass


BasePostAuth = ReadOnlyAdmin if not app_settings.EDITABLE_POSTAUTH else ModelAdmin


class AbstractRadiusPostAuthAdmin(BasePostAuth):
    list_display = ['username', 'reply', 'date']
    list_filter = ['date', 'reply']
    search_fields = ['username', 'reply']
