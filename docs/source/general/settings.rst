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
