vishnu
======

Sessions for the Google App Engine python runtime

Features
--------

-  Cookie based session for Google App Engine using the NDB datastore
-  Configurable for the following cookie settings:
    -  Domain
    -  Path
    -  Secure
    -  HttpOnly
    -  Expires (timeout)
-  HMAC signature to verify cookie has not been tampered with
-  Autosave option which saves anytime a session value is modified
-  Optional Encryption of cookie data using AES
-  Custom timeout per session

Configuration
-------------

app.yaml
~~~~~~~~

Vishnu will automatically look for and use the following variables from your ``app.yaml`` config.

+------+----------+---------+------------+
| name | required | default | descriptio |
|      |          |         | n          |
+======+==========+=========+============+
| ``VI | no       | ``vishn | The name   |
| SHNU |          | u``     | to use for |
| _COO |          |         | the        |
| KIE_ |          |         | cookie. If |
| NAME |          |         | omitted it |
| ``   |          |         | will       |
|      |          |         | default to |
|      |          |         | ``vishnu`` |
|      |          |         | .          |
+------+----------+---------+------------+
| ``VI | yes      | N/A     | Secret     |
| SHNU |          |         | used for   |
| _SEC |          |         | HMAC       |
| RET` |          |         | signature  |
| `    |          |         |            |
+------+----------+---------+------------+
| ``VI | no       | N/A     | Key used   |
| SHNU |          |         | to encrypt |
| _ENC |          |         | cookie     |
| RYPT |          |         | data, it   |
| _KEY |          |         | omitted    |
| ``   |          |         | then value |
|      |          |         | will not   |
|      |          |         | be         |
|      |          |         | encrypted. |
+------+----------+---------+------------+
| ``VI | no       | N/A     | The domain |
| SHNU |          |         | to set the |
| _DOM |          |         | cookie     |
| AIN` |          |         | for. If    |
| `    |          |         | omitted it |
|      |          |         | will       |
|      |          |         | default to |
|      |          |         | the domain |
|      |          |         | the cookie |
|      |          |         | was served |
|      |          |         | from.      |
+------+----------+---------+------------+
| ``VI | no       | ``/``   | The path   |
| SHNU |          |         | to set the |
| _PAT |          |         | cookie     |
| H``  |          |         | for. If    |
|      |          |         | omitted it |
|      |          |         | will       |
|      |          |         | default to |
|      |          |         | ``/``.     |
+------+----------+---------+------------+
| ``VI | no       | true    | Only send  |
| SHNU |          |         | this       |
| _SEC |          |         | cookie     |
| URE` |          |         | over SSL.  |
| `    |          |         |            |
+------+----------+---------+------------+
| ``VI | no       | true    | Only allow |
| SHNU |          |         | cookie     |
| _HTT |          |         | access via |
| P_ON |          |         | HTTP/HTTPS |
| LY`` |          |         | .          |
+------+----------+---------+------------+
| ``VI | no       | false   | Automatica |
| SHNU |          |         | lly        |
| _AUT |          |         | save the   |
| O_SA |          |         | session    |
| VE`` |          |         | when a     |
|      |          |         | value is   |
|      |          |         | set.       |
+------+----------+---------+------------+
| ``VISHNU_TIMEOUT`` | no       | N/A     | How long   |
|  |          |         | until this |
| _TIM |          |         | cookie     |
| EOUT |          |         | expires.   |
| ``   |          |         | If omitted |
|      |          |         | it will    |
|      |          |         | last for   |
|      |          |         | the length |
|      |          |         | of the     |
|      |          |         | browser    |
|      |          |         | session.   |
+------+----------+---------+------------+

Dependencies
~~~~~~~~~~~~

If using encryption you will need to add the following to your ``app.yaml``.

.. code:: yaml

    libraries:
    - name: pycrypto
      version: "2.6"

WSGI Middleware
~~~~~~~~~~~~~~~

To use vishnu you must add it as a middleware to your WSGI application.

.. code:: python

    from vishnu.middleware import SessionMiddleware
    app = SessionMiddleware(app)

Setting a Custom Timeout
~~~~~~~~~~~~~~~~~~~~~~~~

Each session uses the default timeout specified in ``app.yaml`` but if you want to have particular sessions differ to this you can do the following.

.. code:: python

    session = vishnu.get_session()
    session.timeout = 3600
    session.save()

The timeout is in seconds. To set the timeout to expire at the end of this session you can use the ``vishnu.session.TIMEOUT_SESSION`` constant.

.. code:: python

    session = vishnu.get_session()
    session.timeout = vishnu.session.TIMEOUT_SESSION
    session.save()

Cleaning up Expired Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following to a cron handler.

.. code:: python

    import vishnu

    while not vishnu.delete_expired_sessions():
        pass

You can alter the period after expired sessions are deleted by passing a value in seconds as ``dormant_for``.

You can also alter the amount of sessions to delete per call using the ``limit`` argument.