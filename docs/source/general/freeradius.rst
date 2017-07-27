==============================================
Installation and configuration of Freeradius 3
==============================================

This guide explains how to install and configure `freeradius 3 <http://freeradius.org/version3.html>`_
in order to make it work with `django-freeradius <https://github.com/openwisp/django-freeradius/>`_.

.. note::
    The guide is written for debian based systems, other linux distributions can work as well but the
    name of packages and files may be different.

How to install freeradius 3
---------------------------

First of all, become root:

.. code-block:: shell

    sudo -i

Let's add the PPA repository for the Freeradius 3.x stable branch:

.. code-block:: shell

    apt-add-repository ppa:freeradius/stable-3.0

.. code-block:: shell

    apt-get update

Now you can install the packages we need:

.. code-block:: shell

    apt-get install freeradius freeradius-postgresql freeradius-rest

Open the file ``/etc/freeradius/mods-available/sql``.

You have to change  ``driver``, ``dialect``, ``server``, ``port``, ``login``, ``password``, ``radius_db``.

Example for configuration with postgresql::

    driver = "rlm_sql_postgresql"
    dialect = "postgresql"

    # Connection info:
    server = "localhost"
    port = 5432
    login = "<user>"
    password = "<password>"
    radius_db = "radius"

Enable the ``sql`` and ``rest`` modules:

.. code-block:: shell

    cd mods-enabled/
    ln -s /etc/freeradius/mods-available/sql /etc/freeradius/mods-enabled/sql
    ln -s /etc/freeradius/mods-available/rest /etc/freeradius/mods-enabled/rest

Restart freeradius to load the new configuration:

.. code-block:: shell

    service freeradius restart

You may also want to take a look at the `Freeradius documentation <http://freeradius.org/doc/>`_.

How to configure the REST module
--------------------------------

Configure the rest module by editing the file ``/etc/freeradius/mods-enabled/rest``, substituting
``<url>`` with your project's URL, (eg: ``http://127.0.0.1:8000``) ::

    # /etc/freeradius/mods-enabled/rest

    connect_uri = "<url>"

    authorize {
        uri = "${..connect_uri}/api/authorize/"
        method = 'post'
        body = 'json'
        data = '{"username": "%{User-Name}", "password": "%{User-Password}"}'
        tls = ${..tls}
    }

    # this section can be left empty
    authenticate {}

Configure the ``authorize`` and ``authenticate`` section in the default site
(``/etc/freeradius/sites-enabled/default``) as follows::

    # /etc/freeradius/sites-enabled/default

    authorize {
       rest
    }

    # this section can be left empty
    authenticate {}

Debugging
---------

In this section we will explain how to debug your freeradius instance.

Start freeradius in debug mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When debugging we suggest you to open up a dedicated terminal window to run freeradius in debug mode:

.. code-block:: shell

    # we need to stop the main freeradius process first
    service freeradius stop
    # launch freeradius in debug mode
    freeradius -X

Testing authentication and authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can do this with ``radtest``:

.. code-block:: shell

    # radtest <username> <password> <host> 10 <secret>
    radtest admin admin localhost 10 testing123

A successful authentication will return similar output::

    Sent Access-Request Id 215 from 0.0.0.0:34869 to 127.0.0.1:1812 length 75
    	User-Name = "admin"
    	User-Password = "admin"
    	NAS-IP-Address = 127.0.0.1
    	NAS-Port = 10
    	Message-Authenticator = 0x00
    	Cleartext-Password = "admin"
    Received Access-Accept Id 215 from 127.0.0.1:1812 to 0.0.0.0:0 length 20

While an unsuccessful one will look like the following::

    Sent Access-Request Id 85 from 0.0.0.0:51665 to 127.0.0.1:1812 length 73
    	User-Name = "foo"
    	User-Password = "bar"
    	NAS-IP-Address = 127.0.0.1
    	NAS-Port = 10
    	Message-Authenticator = 0x00
    	Cleartext-Password = "bar"
    Received Access-Reject Id 85 from 127.0.0.1:1812 to 0.0.0.0:0 length 20
    (0) -: Expected Access-Accept got Access-Reject


Customizing your configuration
------------------------------

You can customize your freeradius configuration and exploit the many features of freeradius but
you will need to test how your changes play with *django-freeradius*.
