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

.. note::
    If you use a recent version of Debian like **Stretch** (9) or Ubuntu **Zesty** (17),
    you can skip the following command and use the official repositories if you prefer.

Let's add the PPA repository for the Freeradius 3.x stable branch:

.. code-block:: shell

    apt-add-repository ppa:freeradius/stable-3.0
    apt-get update

Now you can install the packages we need:

.. code-block:: shell

    apt-get install freeradius freeradius-postgresql freeradius-rest
    # if mysql instead of postgresql
    apt-get install freeradius freeradius-mysql freeradius-rest

Configuring Freeradius 3
------------------------

For a complete reference on how to configure freeradius please read the `Freeradius wiki, configuration files <http://wiki.freeradius.org/config/Configuration-files>`_ and their `configuration tutorial <http://wiki.freeradius.org/guide/HOWTO>`_.

.. note::
    The path to freeradius configuration could be different on your system. This article use the `/etc/freeradius/3.0/` directory that ships with Debian Stretch

Refer to the `mods-available documentation <http://networkradius.com/doc/3.0.10/raddb/mods-available/home.html>`_ for the available configuration values.

Configure the SQL module
^^^^^^^^^^^^^^^^^^^^^^^^

Once you have configured properly an SQL server, e.g. PostgreSQL:, and you can connect with a username and password edit the file ``/etc/freeradius/3.0/mods-available/sql`` to configure Freeradius to use the relational database.

Change the configuration for ``driver``, ``dialect``, ``server``, ``port``, ``login``, ``password``, ``radius_db`` as you need to fit your SQL server configuration.

Refer to the `sql module documentation <http://networkradius.com/doc/3.0.10/raddb/mods-available/sql.html>`_ for the available configuration values.

Example configuration using the PostgreSQL database:

.. code-block:: ini

    # /etc/freeradius/3.0/mods-available/sql
    driver = "rlm_sql_postgresql"
    dialect = "postgresql"

    # Connection info:
    server = "localhost"
    port = 5432
    login = "<user>"
    password = "<password>"
    radius_db = "radius"


Configure the REST module
^^^^^^^^^^^^^^^^^^^^^^^^^

Configure the rest module by editing the file ``/etc/freeradius/3.0/mods-enabled/rest``, substituting
``<url>`` with your django project's URL, (for example, if you are testing a development environment, the URL could be ``http://127.0.0.1:8000``, otherwise in production could be something like ``https://openwisp2.mydomain.org``)-

Refer to the `rest module documentation <http://networkradius.com/doc/3.0.10/raddb/mods-available/rest.html>`_ for the available configuration values.

.. code-block:: ini

    # /etc/freeradius/3.0/mods-enabled/rest

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

    post-auth {
        uri = "${..connect_uri}/api/postauth/"
        method = 'post'
        body = 'json'
        data = '{"username": "%{User-Name}", "password": "%{User-Password}", "reply": "%{reply:Packet-Type}", "called_station_id": "%{Called-Station-ID}", "calling_station_id": "%{Calling-Station-ID}"}'
        tls = ${..tls}
    }

    accounting {
        uri = "${..connect_uri}/api/accounting/"
        method = 'post'
        body = 'json'
        data = '{"status_type": "%{Acct-Status-Type}", "session_id": "%{Acct-Session-Id}", "unique_id": "%{Acct-Unique-Session-Id}", "username": "%{User-Name}", "realm": "%{Realm}", "nas_ip_address": "%{NAS-IP-Address}", "nas_port_id": "%{NAS-Port}", "nas_port_type": "%{NAS-Port-Type}", "session_time": "%{Acct-Session-Time}", "authentication": "%{Acct-Authentic}", "input_octets": "%{Acct-Input-Octets}", "output_octets": "%{Acct-Output-Octets}", "called_station_id": "%{Called-Station-Id}", "calling_station_id": "%{Calling-Station-Id}", "terminate_cause": "%{Acct-Terminate-Cause}", "service_type": "%{Service-Type}", "framed_protocol": "%{Framed-Protocol}", "framed_ip_address": "%{Framed-IP-Address}"}'
        tls = ${..tls}
    }

Configure the ``authorize``, ``authenticate`` and ``postauth`` section
as follows

.. code-block:: ini

    # /etc/freeradius/3.0/sites-enabled/default

    authorize {
       rest
    }

    # this section can be left empty
    authenticate {}

    post-auth {
       rest

       Post-Auth-Type REJECT {
            rest
        }
    }

    accounting {
       rest
    }

For accounting configuration you need to verify that in pre-accounting we have:

.. code-block:: ini

    preacct {
        # ...
        acct_unique
        # ...
    }

Enable the configured modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now enable the ``sql`` and ``rest`` modules:

.. code-block:: shell

    ln -s /etc/freeradius/3.0/mods-available/sql /etc/freeradius/3.0/mods-enabled/sql
    ln -s /etc/freeradius/3.0/mods-available/rest /etc/freeradius/3.0/mods-enabled/rest

Restart freeradius to load the new configuration:

.. code-block:: shell

    service freeradius restart
    # alternatively if you are using systemd
    systemctl restart freeradius

You may also want to take a look at the `Freeradius documentation <http://freeradius.org/doc/>`_ for further details on how to configure other modules.

Reconfigure the development environment using PostgreSQL
--------------------------------------------------------

You'll have to reconfigure the development environment as well before being able to use django-radius for managing the freeradius databases. Create a file `tests/local_settings.py` and add the following code to configure the database.

.. code-block:: python

   # django-freeradius/tests/local_settings.py
     DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '<db_name>',
            'USER': '<db_user>',
            'PASSWORD': '<db_password>',
            'HOST': '127.0.0.1',
            'PORT': '5432'
        },
     }

Make sure the database by the name <db_name> is created and also the role <db_user> with <db_password> as password.

Radius Checks: ``is_active`` & ``valid_until``
----------------------------------------------

Django-Freeradius provides the possibility to extend the freeradius
query in order to introduce ``is_active`` and ``valid_until`` checks.

An example using MySQL is:

.. code-block:: ini

    # /etc/freeradius/3.0/mods-config/sql/main/mysql/queries.conf
    authorize_check_query = "SELECT id, username, attribute, value, op \
                             FROM ${authcheck_table} \
                             WHERE username = '%{SQL-User-Name}' \
                             AND is_active = TRUE \
                             AND valid_until >= CURDATE() \
                             ORDER BY id"

Debugging
---------

In this section we will explain how to debug your freeradius instance.

Start freeradius in debug mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When debugging we suggest you to open up a dedicated terminal window to run freeradius in debug mode:

.. code-block:: shell

    # we need to stop the main freeradius process first
    service freeradius stop
    # alternatively if you are using systemd
    systemctl stop freeradius
    # launch freeradius in debug mode
    freeradius -X

Testing authentication and authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Alternatively, you can use ``radclient`` which allows more complex tests; in the following
example we show how to test an authentication request which includes ``Called-Station-ID``
and ``Calling-Station-ID``:

.. code-block:: shell

    user="foo"
    pass="bar"
    called="00-11-22-33-44-55:localhost"
    calling="00:11:22:33:44:55"
    request="User-Name=$user,User-Password=$pass,Called-Station-ID=$called,Calling-Station-ID=$calling"
    echo $request | radclient localhost auth testing123

Testing accounting
^^^^^^^^^^^^^^^^^^

You can do this with ``radclient``, but first of all you will have to create a text file
like the following one::

    # /tmp/accounting.txt

    Acct-Session-Id = "35000006"
    User-Name = "jim"
    NAS-IP-Address = 172.16.64.91
    NAS-Port = 1
    NAS-Port-Type = Async
    Acct-Status-Type = Interim-Update
    Acct-Authentic = RADIUS
    Service-Type = Login-User
    Login-Service = Telnet
    Login-IP-Host = 172.16.64.25
    Acct-Delay-Time = 0
    Acct-Session-Time = 261
    Acct-Input-Octets = 9900909
    Acct-Output-Octets = 10101010101
    Called-Station-Id = 00-27-22-F3-FA-F1:hostname
    Calling-Station-Id = 5c:7d:c1:72:a7:3b

Then you can call ``radclient``:

.. code-block:: shell

    radclient -f /tmp/accounting.txt -x 127.0.0.1 acct testing123

You should get the following output::

    Sent Accounting-Request Id 83 from 0.0.0.0:51698 to 127.0.0.1:1813 length 154
    	Acct-Session-Id = "35000006"
    	User-Name = "jim"
    	NAS-IP-Address = 172.16.64.91
    	NAS-Port = 1
    	NAS-Port-Type = Async
    	Acct-Status-Type = Interim-Update
    	Acct-Authentic = RADIUS
    	Service-Type = Login-User
    	Login-Service = Telnet
    	Login-IP-Host = 172.16.64.25
    	Acct-Delay-Time = 0
    	Acct-Session-Time = 261
    	Acct-Input-Octets = 9900909
    	Acct-Output-Octets = 1511075509
    	Called-Station-Id = "00-27-22-F3-FA-F1:hostname"
    	Calling-Station-Id = "5c:7d:c1:72:a7:3b"
    Received Accounting-Response Id 83 from 127.0.0.1:1813 to 0.0.0.0:0 length 20

Customizing your configuration
------------------------------

You can further customize your freeradius configuration and exploit the many features of freeradius but
you will need to test how your configuration plays with *django-freeradius*.
