from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # django-x509 urls
    # keep the namespace argument unchanged
    url(r'^', include('django_freeardius.urls', namespace='freeardius')),
]

urlpatterns += staticfiles_urlpatterns()
