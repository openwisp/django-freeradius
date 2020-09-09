django-freeradius
=================

**WARNING**: The development of this project has moved to `openwisp-radius <https://github.com/openwisp/openwisp-radius>`_, we advise all users of *django-freeradius* to follow the tutorial below to migrate their existing database:

1. Take a backup of your database.
2. Create JSON backup of data that's required for migration with the following command:

.. code-block:: shell

    # Go to the django-freeradius repository (or installed app)
    cd tests/
    python manage.py dumpdata auth.user > user.json
    python manage.py dumpdata auth.group > group.json
    python manage.py dumpdata auth.permission > permission.json
    python manage.py dumpdata contenttypes > contenttype.json
    python manage.py dumpdata sites > site.json
    python manage.py dumpdata socialaccount > social.json
    python manage.py dumpdata django_freeradius > freeradius.json
    pwd # copy output of the command

3. `Setup openwisp-radius <https://openwisp-radius.readthedocs.io/en/latest/developer/setup.html#setup-integrate-in-an-existing-django-project>`_

4. `Use the upgrader script <https://openwisp-radius.readthedocs.io/en/latest/user/management_commands.html#upgrade-from-django-freeradius>`_:

.. code-block:: shell

    # In the openwisp-radius repository
    python tests/manage.py upgrade_from_django_freeradius --backup <output-copied-in-step-2>

For any support, please reach out to us on `the chat channel on gitter <https://gitter.im/openwisp/general>`_ or `use the mailing list <https://groups.google.com/forum/#!forum/openwisp>`_.

**The development of django-freeradius is discontinued and this repository is archived.**
