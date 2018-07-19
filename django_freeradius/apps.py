from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured

from .settings import API_TOKEN


class DjangoFreeradiusConfig(AppConfig):
    name = 'django_freeradius'
    verbose_name = 'Freeradius'

    def check_settings(self):
        if API_TOKEN and len(API_TOKEN) < 15 or not API_TOKEN:    # pragma: nocover
            raise ImproperlyConfigured('Security error: DJANGO_FREERADIUS_API_TOKEN '
                                       'is either not set or is less than 15 characters.')

    def ready(self):
        self.check_settings()
