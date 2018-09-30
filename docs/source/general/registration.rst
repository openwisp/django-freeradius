=========================
Registration of new users
=========================

Django-freeradius does not ship logic related to registration of new users
because there are many good django packages that are aimed at solving that solution.

We recommend using `django-rest-auth <https://github.com/Tivix/django-rest-auth>`_
which provides registration of new users via REST API so you can implement
registration and password reset directly from your captive page.

Setup
-----

Install ``django-rest-auth``::

    pip install django-rest-auth

Add the following to your ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        # ... other apps ..
        # apps needed for registration
        'rest_framework.authtoken',
        'rest_auth',
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'rest_auth.registration',
    ]

    SITE_ID = 1

Add the rest-auth urls to your main ``urls.py``:

.. code-block:: python

    urlpatterns = [
        # ...
        url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
        url(r'^api/v1/registration/', include('rest_auth.registration.urls'))
    ]

API endpoints
-------------

Refer to the `django-rest-auth documentation regarding its API endpoints
<https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html>`_.
