django-freeradius
=================

.. image:: https://travis-ci.org/openwisp/django-freeradius.svg
   :target: https://travis-ci.org/openwisp/django-freeradius

.. image:: https://coveralls.io/repos/openwisp/django-freeradius/badge.svg
  :target: https://coveralls.io/r/openwisp/django-freeradius

.. image:: https://requires.io/github/openwisp/django-freeradius/requirements.svg?branch=master
   :target: https://requires.io/github/openwisp/django-freeradius/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/django-freeradius.svg
   :target: http://badge.fury.io/py/django-freeradius

------------

TODO:

------------

.. contents:: **Table of Contents**:
   :backlinks: none
   :depth: 3

------------

Current features
----------------

* TODO

Project goals
-------------

* TODO

Install stable version from pypi
--------------------------------

Install from pypi:

.. code-block:: shell

    pip install django-freeradius

Install development version
---------------------------

Install tarball:

.. code-block:: shell

    pip install https://github.com/openwisp/django-freeradius/tarball/master

Alternatively you can install via pip using git:

.. code-block:: shell

    pip install -e git+git://github.com/openwisp/django-freeradius#egg=django-freeradius

If you want to contribute, install your cloned fork:

.. code-block:: shell

    git clone git@github.com:<your_fork>/django-freeradius.git
    cd django-freeradius
    python setup.py develop

Setup (integrate in an existing django project)
-----------------------------------------------

Add ``django_freeradius`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # other apps
        'django_freeradius',
    ]

Add the URLs to your main ``urls.py``:

.. code-block:: python

    urlpatterns = [
        # ... other urls in your project ...

        # django-freeradius urls
        # keep the namespace argument unchanged
        url(r'^', include('django_freeradius.urls', namespace='freeradius')),
    ]

Then run:

.. code-block:: shell

    ./manage.py migrate

Installing for development
--------------------------

Install sqlite:

.. code-block:: shell

    sudo apt-get install sqlite3 libsqlite3-dev

Install your forked repo:

.. code-block:: shell

    git clone git://github.com/<your_fork>/django-freeradius
    cd django-freeradius/
    python setup.py develop

Install test requirements:

.. code-block:: shell

    pip install -r requirements-test.txt

Create database:

.. code-block:: shell

    cd tests/
    ./manage.py migrate
    ./manage.py createsuperuser

Launch development server:

.. code-block:: shell

    ./manage.py runserver

You can access the admin interface at http://127.0.0.1:8000/admin/.

Run tests with:

.. code-block:: shell

    ./runtests.py

Settings
--------

TODO

Extending django-freeradius
---------------------

*django-freeradius* provides a set of models and admin classes which can be imported,
extended and reused by third party apps.

To extend *django-freeradius*, **you MUST NOT** add it to ``settings.INSTALLED_APPS``,
but you must create your own app (which goes into ``settings.INSTALLED_APPS``), import the
base classes from django-freeradius and add your customizations.

Extending models
~~~~~~~~~~~~~~~~

This example provides an example of how to extend the base models of
*django-freeradius* by adding a relation to another django model named `Organization`.

.. code-block:: python

    # TODO

Extending the admin
~~~~~~~~~~~~~~~~~~~

Following the previous `Organization` example, you can avoid duplicating the admin
code by importing the base admin classes and registering your models with.

.. code-block:: python

    # TODO


Contributing
------------

1. Announce your intentions in the `OpenWISP Mailing List <https://groups.google.com/d/forum/openwisp>`_
2. Fork this repo and install it
3. Follow `PEP8, Style Guide for Python Code`_
4. Write code
5. Write tests for your code
6. Ensure all tests pass
7. Ensure test coverage does not decrease
8. Document your changes
9. Send pull request

.. _PEP8, Style Guide for Python Code: http://www.python.org/dev/peps/pep-0008/

Changelog
---------

See `CHANGES <https://github.com/openwisp/django-freeradius/blob/master/CHANGES.rst>`_.

License
-------

See `LICENSE <https://github.com/openwisp/django-freeradius/blob/master/LICENSE>`_.

Support
-------

See `OpenWISP Support Channels <http://openwisp.org/support.html>`_.
