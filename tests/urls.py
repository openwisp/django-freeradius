from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # django_freeradius urls
    # keep the namespace argument unchanged
    url(r'^', include('django_freeradius.urls', namespace='freeradius')),
    url(r'^admin/', admin.site.urls),
    # django-rest-auth is optional
    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
