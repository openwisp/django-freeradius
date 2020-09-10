.. include:: ../_moved.rst

===============================
How to extend django-freeradius
===============================

``django-freeeadius`` provieds set of models, admin and API classes which can be imported, extended and hence customized by third party apps.

Update Settings
---------------

Update the settings to trigger the swapper:

.. code-block:: python

    # In settings.py of your project

    DJANGO_FREERADIUS_RADIUSREPLY_MODEL = "my_radius_app.RadiusReply"
    DJANGO_FREERADIUS_RADIUSGROUPREPLY_MODEL = "my_radius_app.RadiusGroupReply"
    DJANGO_FREERADIUS_RADIUSCHECK_MODEL = "my_radius_app.RadiusCheck"
    DJANGO_FREERADIUS_RADIUSGROUPCHECK_MODEL = "my_radius_app.RadiusGroupCheck"
    DJANGO_FREERADIUS_RADIUSACCOUNTING_MODEL = "my_radius_app.RadiusAccounting"
    DJANGO_FREERADIUS_NAS_MODEL = "my_radius_app.Nas"
    DJANGO_FREERADIUS_RADIUSUSERGROUP_MODEL = "my_radius_app.RadiusUserGroup"
    DJANGO_FREERADIUS_RADIUSPOSTAUTHENTICATION_MODEL = "my_radius_app.RadiusPostAuth"

    # where my_radius_app is name of your app extending django_freeradius


Extend models
-------------

Apart from extending implemented models, ``django_freeradius`` also provides flexibility to extend abstract class models from `django-freeradius.base.models`.

Example:

.. code-block:: python

    # In my_radius_app/models.py

    from django.db import models
    from django_freeradius.base.models import AbstractRadiusCheck

    class RadiusCheck(AbstractRadiusCheck):
        # modify/extend the default behavour here
        custom_field = models.TextField()

Similary, you can extend other model classes from ``django_freeradius.base.models``.

Extend admin
------------

Similar to models, abstract admin classes from ``django_freeradius.base.admin`` can also be extended to avoid duplicate code.

.. code-block:: python

    # In my_radius_app/admin.py

    from django.contrib import admin
    from .models import RadiusCheck
    from django_freeradius.base.admin import AbstractRadiusAccountingAdmin

    class RadiusCheckAdmin(AbstractRadiusCheckAdmin):
        model = RadiusCheck
        # modify/extend default behaviour here
        fields = AbstractRadiusCheckAdmin.fields + ['custom_field']
        list_display = AbstractRadiusCheckAdmin.list_display + ['custom_field']

    admin.site.register(RadiusCheck, RadiusCheckAdmin)

.. note::
    For a real world implementation of extending ``django-freeradius.base.admin``, refer `openswisp-radius.admin <https://github.com/openwisp/openwisp-radius/blob/master/openwisp_radius/admin.py>`_

Extend AppConfig
----------------

You can also extend AppConfig class from ``django_freeradius.apps.DjangoFreeradiusConfig`` and provide support for your signals and hooks.

.. code-block:: python

    # In my_radius_app/apps.py

    from django.conf import settings
    from django_freeradius.apps import DjangoFreeradiusConfig
    from django.core.exceptions import ImproperlyConfigured

    API_TOKEN = settings.DJANGO_FREERADIUS_API_TOKEN

    class MyRadiusAppConfig(DjangoFreeradiusConfig):
        name = 'my_radius_app'

        # Overiding DjangoFreeradiusConfig.check_settings
        # just for the sake of example, we add a check which ensures the
        # DJANGO_FREERADIUS_API_TOKEN settings is defined and is at
        # least 20 characters long.
        def check_settings(self):
            if API_TOKEN and len(API_TOKEN) < 20 or not API_TOKEN:
                def check_settings(self):
        if API_TOKEN and len(API_TOKEN) < 20 or not API_TOKEN:
            raise ImproperlyConfigured(
                'Security error: DJANGO_FREERADIUS_API_TOKEN is either not set or is less than 20 characters.')


Extend API views
----------------

You can also extend API views from ``django_freeradius.api.views`` to your suit your models.

.. code-block:: python

    # In my_radius_app/api/views.py

    from django_freeradius.api.views import AuthorizeView, AuthorizeView

    class RadiusTokenAuthentication(TokenAuthentication):
        # modify/extend default behaviour here
        pass

    class RadiusAuthorizeView(AuthorizeView):
        # use your modified authentication class
        authentication_classes = (RadiusTokenAuthentication,)

    authorize = RadiusAuthorizeView.as_view()

.. note::
    For a real world implementation of extending ``django-freeradius.api``, refer `openwisp-radius.api <https://github.com/openwisp/openwisp-radius/tree/master/openwisp_radius/api>`_
