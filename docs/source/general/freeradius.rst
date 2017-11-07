==============================================
Installation and configuration of Freeradius 3
==============================================

This guide explains how to install and configure `freeradius 3 <http://freeradius.org/version3.html>`_
in order to make it work with `django-freeradius <https://github.com/openwisp/django-freeradius/>`_.

.. note::
    The guide is written for debian based systems, other linux distributions can work as well but the
    name of packages and files may be different.
    
.. note::
    You will need a recent version of Debian as Freeradius 3 is available from **Jessie**. The related Ubuntu version is **Zesty**

How to install freeradius 3 on older version
---------------------------------------------

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

Configuring Freeradius 3
------------------------

Edit the file ``/etc/freeradius/mods-available/sql``.

Change the configuration for ``driver``, ``dialect``, ``server``, ``port``, ``login``, ``password``, ``radius_db``.

Refer to the `mods-available documentation <http://networkradius.com/doc/3.0.10/raddb/mods-available/home.html>`_ for the available configuration values.

Example configuration  using  postgresql as storage

.. code-block:: ini
    
    # /etc/freeradius/mods-available/sql
    driver = "rlm_sql_postgresql"
    dialect = "postgresql"

    # Connection info:
    server = "localhost"
    port = 5432
    login = "<user>"
    password = "<password>"
    radius_db = "radius"

Now enable the ``sql`` and ``rest`` modules:

.. code-block:: shell

    cd mods-enabled/
    ln -s /etc/freeradius/mods-available/sql /etc/freeradius/mods-enabled/sql
    ln -s /etc/freeradius/mods-available/rest /etc/freeradius/mods-enabled/rest

Restart freeradius to load the new configuration:

.. code-block:: shell

    service freeradius restart
    # alternatively if you are using systemd
    systemctl restart freeradius

You may also want to take a look at the `Freeradius documentation <http://freeradius.org/doc/>`_.

How to configure the REST module
--------------------------------

Configure the rest module by editing the file ``/etc/freeradius/mods-enabled/rest``, substituting
``<url>`` with your django-freeradius's URL, (eg: ``http://127.0.0.1:8000``)

.. code-block:: ini

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

Configure the ``authorize``, ``authenticate`` and ``postauth`` section in the default site
(``/etc/freeradius/sites-enabled/default``) as follows::

    # /etc/freeradius/sites-enabled/default

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

    preacct {
        # ...
        acct_unique
        # ...
    }

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
~~~~~~~~~~~~~~~~~~

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
you will need to test how your configuratoin play with *django-freeradius*.
