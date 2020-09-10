.. include:: ../_moved.rst

============
Contributing
============

Thank you for taking the time to contribute to django-freeradius.

Follow these guidelines to speed up the process.

.. contents:: **Table of Contents**:
  :backlinks: none
  :depth: 3

.. note::
    **In order to have your contribution accepted faster**, please read the
    `OpenWISP contributing guidelines <http://openwisp.io/docs/developer/contributing.html>`_ and make sure to follow its guidelines.

Setup
-----

Once you have chosen an issue to work on, `setup your machine for development
<https://django-freeradius.readthedocs.io/en/latest/general/setup.html#installing-for-development>`_

Ensure test coverage does not decrease
--------------------------------------

First of all, install the test requirements:

.. code-block:: shell

    workon radius  # activate virtualenv
    pip install --no-cache-dir -U -r requirements-test.txt

When you introduce changes, ensure test coverage is not decreased with:

.. code-block:: shell

    coverage run --source=django_freeradius runtests.py

Follow style conventions (PEP8, isort, JSLint)
----------------------------------------------

First of all, install the test requirements:

.. code-block:: shell

    workon radius  # activate virtualenv
    pip install --no-cache-dir -U -r requirements-test.txt
    npm install -g jslint

Before committing your work check that your changes are not breaking the style conventions with:

.. code-block:: shell

    ./runflake8
    ./runisort
    jslint ./django_freeradius/static/django-freeradius/js/*.js

For more information, please see:

- `PEP8: Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_
- `isort: a python utility / library to sort imports <https://github.com/timothycrosley/isort>`_

Update the documentation
------------------------

If you introduce new features or change existing documented behavior,
please remember to update the documentation!

The documentation is located in the ``/docs`` directory
of the repository.

To do work on the docs, proceed with the following steps:

.. code-block:: shell

    workon radius  # activate virtualenv
    pip install sphinx
    cd docs
    make html

Send pull request
-----------------

Now is time to push your changes to github and open a `pull request
<https://github.com/openwisp/django-freeradius/pulls>`_!
