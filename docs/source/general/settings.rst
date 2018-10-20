Available settings
------------------

``DJANGO_FREERADIUS_EDITABLE_ACCOUNTING``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``False``

Whether ``radacct`` entries are editable from the django admin or not.

``DJANGO_FREERADIUS_EDITABLE_POSTAUTH``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``False``

Whether ``postauth`` logs are editable from the django admin or not.

``DJANGO_FREERADIUS_GROUPCHECK_ADMIN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``False``

Direct editing of group checks items is disabled by default because
these can be edited through inline items in the Radius Group
admin (Freeradius > Groups).

*This is done with the aim of simplifying the admin interface and avoid
overwhelming users with too many options*.

If for some reason you need to enable direct editing of group checks
you can do so by setting this to ``True``.

``DJANGO_FREERADIUS_GROUPREPLY_ADMIN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``False``

Direct editing of group reply items is disabled by default because
these can be edited through inline items in the Radius Group
admin (Freeradius > Groups).

*This is done with the aim of simplifying the admin interface and avoid
overwhelming users with too many options*.

If for some reason you need to enable direct editing of group replies
you can do so by setting this to ``True``.

``DJANGO_FREERADIUS_USERGROUP_ADMIN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``False``

Direct editing of user group items (``radusergroup``) is disabled by default
because these can be edited through inline items in the User
admin (Users and Organizations > Users).

*This is done with the aim of simplifying the admin interface and avoid
overwhelming users with too many options*.

If for some reason you need to enable direct editing of user group items
you can do so by setting this to ``True``.

``DJANGO_FREERADIUS_DEFAULT_SECRET_FORMAT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``NT-Password``

The default encryption format for storing radius check values.

``DJANGO_FREERADIUS_DISABLED_SECRET_FORMATS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``[]``

A list of disabled encryption formats, by default all formats are
enabled in order to keep backward compatibility with legacy systems.

``DJANGO_FREERADIUS_RADCHECK_SECRET_VALIDATORS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**:

.. code-block:: python

    {'regexp_lowercase': '[a-z]+',
     'regexp_uppercase': '[A-Z]+',
     'regexp_number': '[0-9]+',
     'regexp_special': '[\!\%\-_+=\[\]\
                       {\}\:\,\.\?\<\>\(\)\;]+'}

Regular expressions regulating the password validation;
by default the following character families are required:

- a lowercase character
- an uppercase character
- a number
- a special character

``DJANGO_FREERADIUS_BATCH_DEFAULT_PASSWORD_LENGTH``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``8``

The default password length of the auto generated passwords while
batch addition of users from the csv.

``DJANGO_FREERADIUS_BATCH_DELETE_EXPIRED``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``18``

It is the number of months after which the expired users are deleted.

``DJANGO_FREERADIUS_BATCH_PDF_TEMPLATE``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is the template used to generate the pdf when users are being generated using the batch add users feature using the prefix.

The value should be the absolute path to the template of the pdf.

``DJANGO_FREERADIUS_API_TOKEN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `API Token <api.html#api-token>`_.

``DJANGO_FREERADIUS_API_AUTHORIZE_REJECT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``False``

Indicates wether the `Authorize API view <api.html#Authorize>`_ will return
``{"control:Auth-Type": "Reject"}`` or not.

Rejecting an authorization request explicitly will prevent freeradius from
attempting to perform authorization with other mechanisms (eg: radius checks, LDAP, etc.).

When set to ``False``, if an authorization request fails, the API will respond with
``None``, which will allow freeradius to keep attempting to authorize the request
with other freeradius modules.

Set this to ``True`` if you are performing authorization exclusively through the REST API.

Batch mail settings
~~~~~~~~~~~~~~~~~~~

    * `DJANGO_FREERADIUS_BATCH_MAIL_SUBJECT <importing_users.html#django-freeradius-batch-mail-subject>`_
    * `DJANGO_FREERADIUS_BATCH_MAIL_MESSAGE <importing_users.html#django-freeradius-batch-mail-message>`_
    * `DJANGO_FREERADIUS_BATCH_MAIL_SENDER <importing_users.html#django-freeradius-batch-mail-sender>`_
