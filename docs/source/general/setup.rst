=====
Setup
=====

Create a virtual environment
----------------------------

Please use a `python virtual environment <https://docs.python.org/3/library/venv.html>`_.
It keeps everybody on the same page, helps reproducing bugs and resolving problems.

We highly suggest to use **virtualenvwrapper**, please refer to the official `virtualenvwarpper installation page <http://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_ and come back here when ready to proceed.

.. code-block:: shell

    # create virtualenv
    mkvirtualenv radius

.. note::
    If you encounter an error like ``Python could not import the module virtualenvwrapper``
    add ``VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3`` and run ``source virtualenvwrapper.sh`` again :)

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

In the django ``settings.py`` file of your project, do the following:

- add ``django_freeradius`` and ``django_filters`` to ``INSTALLED_APPS``
- set ``DJANGO_FREERADIUS_API_TOKEN`` (see `API Token <api.html#api-token>`_
  for more information):

.. code-block:: python

    INSTALLED_APPS = [
        # other apps
        'django_freeradius',
        'django_filters',
    ]

    DJANGO_FREERADIUS_API_TOKEN = '<a-long-secret-value-of-your-choice>'

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

Migrating an existing freeradius database
-----------------------------------------

If you already have a freeradius 3 database with the default schema, you should
be able to use it with django-freeradius (and openwisp-radius) easily:

1. first of all, back up your existing database;
2. configure django to connect to your existing database;
3. fake the first migration (which only replicates the default freeradius schema)
   and then launch the rest of migrations normally, see the examples below to
   see how to do this.

django-freeradius
~~~~~~~~~~~~~~~~~

.. code-block:: shell

    ./manage.py migrate --fake django_freeradius 0001_initial_freeradius
    ./manage.py migrate


openwisp-radius
~~~~~~~~~~~~~~~

In case you are using `openwisp-radius <https://github.com/openwisp/openwisp-radius>`_:

.. code-block:: shell

    ./manage.py migrate --fake openwisp_radius 0001_initial_freeradius
    ./manage.py migrate

Installing for development
--------------------------

Install sqlite:

.. code-block:: shell

    sudo apt-get install sqlite3 libsqlite3-dev

Install mysqlclient:

.. code-block:: shell

    sudo apt-get install libmysqlclient-dev

Install your forked repo:

.. code-block:: shell

    git clone git://github.com/<your_username>/django-freeradius
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
