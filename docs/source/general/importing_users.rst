===============
Importing users
===============

This feature can be used for importing users from a csv file. There are many features included in it such as:

* Importing users in batches: all of the users of a particular csv file would be stored in batches and can be retrieved/ deleted easily using the batch functions.
* Set an expiration date: Expiration date can be set for a batch after which the users would not able to authenticate to the RADIUS Server.
* Autogenerate usernames and passwords: The usernames and passwords are automatically generated if they aren't provided in the csv file. Usernames are generated from the email address whereas passwords are generated randomly where the length of passwords can be customized.
* Passwords are accepted in both cleartext and hash formats from the CSV.

We've defined management commands which would help us in acheiving these.

``batch_add_users``
-------------------

This command imports users from a csv file. Usage is as shown below.

.. code-block:: shell

    ./manage.py batch_add_users --file <filepath> --expiration <expiration_date> --password-length <password_length>

Note that the expiration and password-length are optional parameters which default to never and 8 respectively.

It is important to take care of the following when importing users from the CSV.

* The CSV shall be of the format:

    `username,password,email,firstname,lastname`

* cleartext passwords should start with a prefix `cleartext$`. For ex, if the password is 'qwerty' it should be encoded as `cleartext$qwerty`.
* The hashes are directly stored in the database if they are of the django hash format. Check about django's password hashing from `here <https://docs.djangoproject.com/en/2.0/topics/auth/passwords/>`_.
* Email is the only mandatory field of the CSV file. Others important fields like username and passeword will be auto generated.

``delete_old_users``
--------------------

This command deletes users expired before a certain duration of time.

.. code-block:: shell

    ./manage.py delete_old_users --older-than-months <duration_in_months>

Note that the default duration is set to 18 months.
