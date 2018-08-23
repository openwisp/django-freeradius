from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals

from django_freeradius.utils import set_default_limits

from .settings import API_TOKEN


class DjangoFreeradiusConfig(AppConfig):
    name = 'django_freeradius'
    verbose_name = 'Freeradius'

    def check_settings(self):
        if API_TOKEN and len(API_TOKEN) < 15 or not API_TOKEN:    # pragma: nocover
            raise ImproperlyConfigured('Security error: DJANGO_FREERADIUS_API_TOKEN '
                                       'is either not set or is less than 15 characters.')

    def connect_signals(self):
        signals.post_save.connect(set_default_limits,
                                  sender=get_user_model())

    def ready(self):
        self.check_settings()
        self.connect_signals()
