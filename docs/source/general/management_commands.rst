===================
Management commands
===================

Management commands serve many purposes, for example: database cleaning.

Management commands can be used with:

.. code-block:: shell

    cd tests/
    ./manage.py <commad> <args>

In this page we list the management commands currently available in django-freeradius.

``delete_old_radacct``
----------------------

This command deletes RADIUS accounting sessions older than <days>.

.. code-block:: shell

    ./manage.py delete_old_radacct <days>

For example:

.. code-block:: shell

    ./manage.py delete_old_radacct 365
