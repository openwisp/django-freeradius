from django.conf import settings

EDITABLE_ACCOUNTING = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_ACCOUNTING', False)
EDITABLE_POSTAUTH = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_POSTAUTH', False)
