from django.conf.urls import url, include

from .api import urls as api

urlpatterns = [
    url(r'^api/', include(api)),
]
