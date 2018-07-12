========================
Enforcing session limits
========================

This feature lets the system administrator enforce session and
bandwidth limits on the users.

Some of the features added here are:

* put daily and all time session limits
* put daily bandwidth limits
* default profile for the new users being added

Adding from admin inteface
--------------------------

At the url ``/admin/django_freeradius/radiusprofile/`` it is possible to
edit the profiles for different types of users. You can map the profiles to the users
from the user change page i.e., at the url ``/admin/auth/user/<user_id>/change``.

You will find two profiles which are created automatically:

- ``Limited User`` is the deafult profile for new users, the default limits
  are 3 hours and 300 MB daily
- ``Power User`` is a profile you can use to grant unlimited usage

You can customize these profiles or create new ones according to your needs.

**Note on the default profile**: keep in mind that the profile flagged as
default will by automatically assigned to new users.

There are attributes defined in the RadiusProfile model which help us enforce limits on the users.

``Daily session limit``
-----------------------

The daily session time limit (in seconds) to be enforced on the users.

``Daily bandwidth limit``
-------------------------

The daily bandwidth usage limit (in octets) to be enforced on the users.

``Maximum all time session limit``
----------------------------------

The all time session limit (in seconds) to be enforced on the users.

Configuring the FreeRADIUS rlm_sqlcounter modules
-------------------------------------------------

The sqlcounter modules should be configured in order to get this feature working.

The ``/etc/freeradius/mods-available/sqlcounter`` should look like the following:

.. code-block:: ini

    # /etc/freeradius/3.0/mods-available/sqlcounter
    # The dailycounter sqlcounter module which comes by default
    sqlcounter dailycounter {
        sql_module_instance = sql
        dialect = ${modules.sql.dialect}

        counter_name = Daily-Session-Time
        check_name = Max-Daily-Session
        reply_name = Session-Timeout

        key = User-Name
        reset = daily

        $INCLUDE ${modconfdir}/sql/counter/${dialect}/${.:instance}.conf
    }

    # The noresetcounter sqlcounter module which comes by default
    sqlcounter noresetcounter {
        sql_module_instance = sql
        dialect = ${modules.sql.dialect}

        counter_name = Max-All-Session-Time
        check_name = Max-All-Session
        key = User-Name
        reset = never

        $INCLUDE ${modconfdir}/sql/counter/${dialect}/${.:instance}.conf
    }

    # Custom defined dailybandwidthcounter for calculating the data transfer daily
    sqlcounter dailybandwidthcounter {
        counter_name = Max-Daily-Session-Traffic
        check_name = Max-Daily-Session-Traffic
        sql_module_instance = sql
        key = 'User-Name'
        reset = daily
        Reply-Message = "Your daily bandwidth limit has reached"
        query = "SELECT sum(AcctOutputOctets) + sum(AcctInputOctets) FROM radacct WHERE \
                 UserName = '%{${key}}' AND \
                 AcctStartTime::ABSTIME::INT4 + AcctSessionTime > '%%b'"
    }

Create a symbolic link to ``mods-available/sqlcounter`` at
``mods-available/sqlcounter`` for the sqlcounter modules to get enabled.

.. code-block:: ini

    ln -s /etc/freeradius/3.0/mods-available/sqlcounter /etc/freeradius/3.0/mods-enabled/sqlcounter

Add the sqlcounter modules to the authorize section.

.. code-block:: ini

    # /etc/freeradius/3.0/sites-enabled/default
    authorize {
        rest
        sql
        dailycounter
        noresetcounter
        dailybandwidthcounter
    }

Restart freeradius to load new configuration

.. code-block:: ini

    service freeradius restart
    # alternatively if you are using systemd
    systemctl restart freeradius

If you are having errors with the importing the sqlcounter modules,
try doing the following in your ``radiusd.conf``

.. code-block:: ini

    # /etc/freeradius/3.0/radiusd.conf
    modules {
        # ..
        $INCLUDE mods-enabled/sql
        $INCLUDE mods-enabled/sqlcounter
        $INCLUDE mods-enabled
        # ..
    }

This issue has been fixed in the latest patch of FreeRADIUS in the v3.0.x branch.
