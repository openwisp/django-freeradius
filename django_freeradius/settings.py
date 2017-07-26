from django.conf import settings

EDITABLE_POSTAUTH = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_POSTAUTH', False)
