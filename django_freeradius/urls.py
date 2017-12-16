from django.conf.urls import include, url

from .api import urls as api

app_name = 'freeradius'
urlpatterns = [
    url(r'^api/', include(api)),
]
