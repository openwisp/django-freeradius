============
Contributing
============

Thank you for taking the time to contribute to django-freeradius.

Follow these guidelines to speed up the process.

.. contents:: **Table of Contents**:
  :backlinks: none
  :depth: 3

.. note::

    Before continuing with your contributing endeavours, please read the
    OpenWISP contributing guidelines to ensure smooth working of the
    freeradius repository. The guidelines can be found at the following `link here <http://openwisp.io/docs/developer/contributing.html>`_

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
