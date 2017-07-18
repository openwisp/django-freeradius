from django.conf.urls import include, url

from .api import urls as api

urlpatterns = [
    url(r'^api/', include(api)),
]
