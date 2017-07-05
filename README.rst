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

Django-freeradius is part of the `OpenWISP project <http://openwrt.org>`_.

.. image:: http://netjsonconfig.openwisp.org/en/latest/_images/openwisp.org.svg
  :target: http://openwisp.org

**django-freeradius** is Django reusable app that provides an admin interface to a `freeradius <http://freeradius.org/>`_ database.

.. contents:: **Table of Contents**:
   :backlinks: none
   :depth: 3

Project goals
-------------

* provide a web interface to manage a freeradius database.
* provide abstract models and admin classes that can be imported, extended and reused in third party apps.

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

`Documentation <https://github.com/openwisp/django-freeradius/tree/master/docs>`_ |
`Change log <https://github.com/openwisp/django-freeradius/blob/master/CHANGES.rst>`_ |
`Support channels <http://openwisp.org/support.html>`_ |
`Issue Tracker <https://github.com/openwisp/django-freeradius/issues>`_ |
`License <https://github.com/openwisp/django-freeradius/blob/master/LICENSE>`_
