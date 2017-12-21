=====
Setup
=====

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
