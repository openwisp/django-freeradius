from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


def disable_accounts(modeladmin, request, queryset):
    queryset.update(is_active=False)
    ct = ContentType.objects.get_for_model(queryset.model)
    for entry in queryset:
        LogEntry.objects.log_action(user_id=request.user.id,
                                    content_type_id=ct.pk,
                                    object_id=entry.pk,
                                    object_repr=entry.username,
                                    action_flag=CHANGE,
                                    change_message=_("Disabled"))
    messages.add_message(request, messages.INFO, '%d modifiche' % queryset.count())


disable_accounts.short_description = _('Disable')


def enable_accounts(modeladmin, request, queryset):
    queryset.update(is_active=True)
    ct = ContentType.objects.get_for_model(queryset.model)
    for entry in queryset:
        LogEntry.objects.log_action(user_id=request.user.id,
                                    content_type_id=ct.pk,
                                    object_id=entry.pk,
                                    object_repr=entry.username,
                                    action_flag=CHANGE,
                                    change_message=_("Enabled"))
    messages.add_message(request, messages.INFO, '%d modifiche' % queryset.count())


enable_accounts.short_description = _('Enable')
