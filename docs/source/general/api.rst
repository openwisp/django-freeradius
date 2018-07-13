=================
API Documentation
=================

django-freeradius provides an API for performing all the get and post
actions. Only authorized users with a token will able to get and post to
the API. The API token can be configured in the settings which is mandatory.

``DJANGO_FREERADIUS_API_TOKEN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set this variable to the secret API token of your instance.
Users can send this token as a bearer token or also as a query string.
FreeRADIUS must be configured to send a bearer token as mentioned in the
`docs <freeradius.html>`_.

Accessing the API
-----------------

There are two ways in which you can send the token to access the API.

* Bearer token (recommended)::

      curl -X POST http://localhost:8000/api/authorize/ \
           -H "Authorization: Bearer <token>" \
           -d "username=<username>&password=<password>"

* Querystring::

      curl -X POST http://localhost:8000/api/authorize/?token=<token> \
           -d "username=<username>&password=<password>"

Accounting
##########

.. code-block:: text

    /api/accounting

GET
+++
Returns a list of accounting objects

.. code-block:: text

    GET /api/accounting

.. code-block:: json

    [
      {
          "called_station_id": "00-27-22-F3-FA-F1:hostname",
          "nas_port_type": "Async",
          "groupname": null,
          "id": 1,
          "realm": "",
          "terminate_cause": "User_Request",
          "nas_ip_address": "172.16.64.91",
          "authentication": "RADIUS",
          "stop_time": null,
          "nas_port_id": "1",
          "service_type": "Login-User",
          "username": "admin",
          "update_time": null,
          "connection_info_stop": null,
          "start_time": "2018-03-10T14:44:17.234035+01:00",
          "output_octets": 1513075509,
          "calling_station_id": "5c:7d:c1:72:a7:3b",
          "input_octets": 9900909,
          "interval": null,
          "session_time": 261,
          "session_id": "35000006",
          "connection_info_start": null,
          "framed_protocol": "test",
          "framed_ip_address": "127.0.0.1",
          "unique_id": "75058e50"
      }
    ]


POST
++++
Add or update accounting information (start, interim-update, stop);
does not return any JSON response so that freeradius will avoid
processing the response without generating warnings

=====================     ======================
Param                     Description
=====================     ======================
session_id                Session ID
unique_id                 Accounting unique ID
username                  Username
groupname                 Group name
realm                     Realm
nas_ip_address            NAS IP address
nas_port_id               NAS port ID
nas_port_type             NAS port type
start_time                Start time
update_time               Update time
stop_time                 Stop time
interval                  Interval
session_time              Session Time
authentication            Authentication
connection_info_start     Connection Info Start
connection_info_stop      Connection Info Stop
input_octets              Input Octets
output_octets             Output Octets
called_station_id         Called station ID
calling_station_id        Calling station ID
terminate_cause           Termination Cause
service_type              Service Type
framed_protocol           Framed protocol
framed_ip_address         framed IP address
=====================     ======================

Pagination
++++++++++
Pagination is provided using a Link header pagination.
https://developer.github.com/v3/guides/traversing-with-pagination/

.. code-block:: text

    {
      ....
      ....
      link: <http://testserver/api/accounting/?page=2&page_size=1>; rel=\"next\",
            <http://testserver/api/accounting/?page=3&page_size=1>; rel=\"last\"
      ....
      ....
    }

Note: Default page size is 10, which can be overridden using the `page_size` parameter.

Filters
+++++++
The JSON objects returned using the GET endpoint can be filtered/queried using specific parameters.

==================  ====================
Filter Parameters   Description
==================  ====================
username            Username
called_station_id   Called Station ID
calling_station_id  Calling Station ID
start_time          Start time
stop_time           Stop time
is_open             If stop_time is null
==================  ====================

Authorize
#########

.. code-block:: text

    /api/authorize

Responds to only **POST**, used for authorizing a given username and password.

.. code-block:: text

    POST /api/authorize HTTP/1.1 username=testuser&password=testpassword

========    ===========================
Param       Description
========    ===========================
username    Username for the given user
password    Password for the given user
========    ===========================

PostAuth
########

.. code-block:: text

    /api/postauth

Sets the response data to None in order to instruct
FreeRADIUS to avoid processing the response body

Responds only to **POST**
