import swapper
from django.contrib import messages
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.admin.actions import delete_selected
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from openwisp_utils.admin import TimeReadonlyAdminMixin

from .. import settings as app_settings
from .admin_actions import disable_action, enable_action
from .admin_filters import DuplicateListFilter, ExpiredListFilter
from .forms import ModeSwitcherForm, NasForm, RadiusBatchForm, RadiusCheckForm
from .models import _encode_secret


class TimeStampedEditableAdmin(TimeReadonlyAdminMixin, ModelAdmin):
    pass


class ReadOnlyAdmin(ModelAdmin):
    """
    Disables all editing capabilities
    """
    def __init__(self, *args, **kwargs):
        super(ReadOnlyAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [f.name for f in self.model._meta.fields]

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)
        if 'delete_selected' in actions:  # pragma: no cover
            del actions['delete_selected']
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


class AbstractRadiusCheckAdmin(TimeStampedEditableAdmin):
    list_display = ['username', 'attribute', 'op',
                    'value', 'is_active', 'valid_until',
                    'created', 'modified']
    search_fields = ['username', 'value']
    list_filter = [DuplicateListFilter,
                   ExpiredListFilter,
                   'created',
                   'modified',
                   'valid_until']
    readonly_fields = ['value']
    form = RadiusCheckForm
    fields = ['mode',
              'user',
              'username',
              'op',
              'attribute',
              'value',
              'new_value',
              'is_active',
              'valid_until',
              'notes',
              'created',
              'modified']
    autocomplete_fields = ['user']
    actions = [disable_action, enable_action, delete_selected]

    def save_model(self, request, obj, form, change):
        if form.data.get('new_value'):
            obj.value = _encode_secret(form.data['attribute'],
                                       form.data.get('new_value'))
        obj.save()

    def get_fields(self, request, obj=None):
        """ do not show raw value (readonly) when adding a new item """
        fields = self.fields[:]
        if not obj:
            fields.remove('value')
        return fields


class AbstractRadiusReplyAdmin(TimeStampedEditableAdmin):
    list_display = ['username', 'attribute', 'op',
                    'value', 'created', 'modified']
    autocomplete_fields = ['user']
    form = ModeSwitcherForm
    fields = ['mode',
              'user',
              'username',
              'attribute',
              'op',
              'value',
              'created',
              'modified']


BaseAccounting = ReadOnlyAdmin if not app_settings.EDITABLE_ACCOUNTING else ModelAdmin


class AbstractRadiusAccountingAdmin(BaseAccounting):
    list_display = ['session_id',
                    'username',
                    'session_time',
                    'input_octets',
                    'output_octets',
                    'calling_station_id',
                    'called_station_id',
                    'start_time',
                    'stop_time']
    search_fields = ['unique_id',
                     'username',
                     'calling_station_id',
                     'called_station_id',
                     'nas_ip_address']
    list_filter = ['start_time', 'stop_time']


class AbstractNasAdmin(TimeStampedEditableAdmin):
    form = NasForm
    fieldsets = (
        (None, {
            'fields': (
                'name', 'short_name',
                ('type', 'custom_type'),
                'ports', 'secret', 'server', 'community', 'description'
            )
        }),
    )
    search_fields = ['name', 'short_name', 'server']
    list_display = ['name', 'short_name', 'server', 'secret', 'created', 'modified']

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        obj.type = data.get('custom_type') or data.get('type')
        super(AbstractNasAdmin, self).save_model(request, obj, form, change)

    class Media:
        css = {'all': ('django-freeradius/css/nas.css',)}


class RadiusGroupCheckInline(TimeReadonlyAdminMixin, StackedInline):
    model = swapper.load_model('django_freeradius', 'RadiusGroupCheck')
    exclude = ['groupname']
    extra = 0


class RadiusGroupReplyInline(TimeReadonlyAdminMixin, StackedInline):
    model = swapper.load_model('django_freeradius', 'RadiusGroupReply')
    exclude = ['groupname']
    extra = 0


class AbstractRadiusGroupAdmin(TimeStampedEditableAdmin):
    list_display = ['name', 'description', 'default',
                    'created', 'modified']
    search_fields = ['name']
    inlines = [RadiusGroupCheckInline,
               RadiusGroupReplyInline]

    def has_delete_permission(self, request, obj=None):
        if obj and obj.default:
            return False
        return super().has_delete_permission(request, obj)

    def delete_selected(self, request, queryset):
        if self.get_default_queryset(request, queryset).exists():
            msg = _('Cannot proceed with the delete operation because '
                    'the batch of items contains the default group, '
                    'which cannot be deleted')
            self.message_user(request, msg, messages.ERROR)
            return False
        return delete_selected(self, request, queryset)

    actions = [delete_selected]

    def get_default_queryset(self, request, queryset):
        """ overridable """
        return queryset.filter(default=True)


class AbstractRadiusUserGroupAdmin(TimeStampedEditableAdmin):
    list_display = ['username', 'groupname',
                    'priority', 'created', 'modified']
    autocomplete_fields = ['user', 'group']
    form = ModeSwitcherForm
    fields = ['mode',
              'user',
              'username',
              'group',
              'groupname',
              'priority',
              'created',
              'modified']


class RadiusUserGroupInline(StackedInline):
    model = swapper.load_model('django_freeradius', 'RadiusUserGroup')
    exclude = ['username', 'groupname', 'created', 'modified']
    extra = 0
    ordering = ('priority',)


class RadGroupMixin(object):
    list_display = ['groupname', 'attribute', 'op',
                    'value', 'created', 'modified']
    autocomplete_fields = ['group']
    form = ModeSwitcherForm
    fields = ['mode',
              'group',
              'groupname',
              'attribute',
              'op',
              'value',
              'created',
              'modified']


class AbstractRadiusGroupCheckAdmin(RadGroupMixin, TimeStampedEditableAdmin):
    pass


class AbstractRadiusGroupReplyAdmin(RadGroupMixin, TimeStampedEditableAdmin):
    pass


BasePostAuth = ReadOnlyAdmin if not app_settings.EDITABLE_POSTAUTH else ModelAdmin


class AbstractRadiusPostAuthAdmin(BasePostAuth):
    list_display = ['username',
                    'reply',
                    'calling_station_id',
                    'called_station_id',
                    'date']
    list_filter = ['date', 'reply']
    search_fields = ['username',
                     'reply',
                     'calling_station_id',
                     'called_station_id']


class AbstractRadiusBatchAdmin(TimeStampedEditableAdmin):
    form = RadiusBatchForm

    class Media:
        js = [static('django-freeradius/js/strategy-switcher.js')]

    def number_of_users(self, obj):
        return obj.users.count()

    number_of_users.short_description = _('number of users')

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.exclude = ('pdf', 'users')
        return super(AbstractRadiusBatchAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        strategy = data.get('strategy')
        if not change:
            if strategy == "csv":
                if data.get('csvfile', False) and not change:
                    csvfile = data.get('csvfile')
                    obj.csvfile_upload(csvfile)
            elif strategy == "prefix":
                prefix = data.get('prefix')
                n = data.get('number_of_users')
                obj.prefix_add(prefix, n)
        else:
            obj.save()

    def delete_model(self, request, obj):
        obj.users.all().delete()
        super(AbstractRadiusBatchAdmin, self).delete_model(request, obj)

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = _('Delete selected batches')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(AbstractRadiusBatchAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return ('strategy', 'prefix', 'csvfile', 'number_of_users',
                    'users', 'pdf', 'expiration_date') + readonly_fields
        return readonly_fields


AbstractRadiusBatchAdmin.list_display += ('expiration_date', 'created')


class AbstractUserAdmin(BaseUserAdmin):
    search_fields = ['username']
    readonly_fields = ['date_joined', 'last_login']

    def get_inline_instances(self, request, obj=None):
        """
        Adds RadiusGroupInline only for existing objects
        """
        inlines = super().get_inline_instances(request, obj)
        if obj:
            usergroup = RadiusUserGroupInline(self.model,
                                              self.admin_site)
            inlines.append(usergroup)
        return inlines
