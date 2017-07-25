=============================================
Installation and configuration of Freeradius
=============================================

We will install freeradius 3.x.

For this it will be much easier if you become the root user.

.. code-block:: shell

   sudo su

First, let's add the PPA repository for the Freeradius 3.x stable branch:

.. code-block:: shell

   apt-add-repository ppa:freeradius/stable-3.0

.. code-block:: shell

   apt-get update

Now you can install freeradius with freeradius-postgres and freeradius-mysql modules:

.. code-block:: shell

   apt-get install freeradius freeradius-mysql freeradius-postgresql

Let's go to the file /etc/freeradius/mods-available/sql.

You have to change  driver, dialect, server, port, login, password, radius_db.

Example for configuration with postgresql::

   driver = "rlm_sql_postgresql"

   dialect = "postgresql"

   # Connection info:

	  server = "localhost"
	  #port = 3306
	  login = "<user>"
	  password = "<password>"

   # Database table configuration for everything except Oracle

   radius_db = "freeradius"

Create softlink for modules that you want to add:

.. code-block:: shell

   cd mods-enabled/

   ln -s ../mods-available/sql ./

   ln -s ../mods-available/redis ./

   ln -s ../mods-available/rediswho ./

Launch freeradius in debug mode:

.. code-block:: shell

   freeradius -X

You may also want to take a look at the `Freeradius documentation <http://freeradius.org/doc/>`

==========================================
Configure Freeradius to use a RESTful API.
==========================================

First we need to install the rest module (rml_rest):

.. code-block:: shell

   apt-get install freeradius-rest

To enable the module rlm_rest by symlinking, eg:

.. code-block:: shell

   ln -s /etc/freeradius/mods-available/rest /etc/freeradius/mods-enabled/rest

rml_rest module configuration
-----------------------------

Example::

   #/etc/freeradius/mods-enabled/rest

   connect_uri = "http://127.0.0.1:8000"

   authorize {
    uri = "${..connect_uri}/api/authorize/"
    method = 'post'
    body = 'json'
    data = '{"username": "%{User-Name}", "password": "%{User-Password}"}'
    tls = ${..tls}

   }

   authenticate {
    uri = "${..connect_uri}/api/authorize/"
    method = 'post'
    body = 'json'
    data = '{"username": "%{User-Name}", "password": "%{User-Password}"}'
    tls = ${..tls}

   }

Configure the default site::

   #/etc/freeradius/sites-enabled/default:

   authorize {
       rest
       # ... other configuration
   }

   authenticate {
       rest
       # ... other configuration
   }
