vishnu
======

Sessions for python WSGI applications.

.. image:: https://img.shields.io/pypi/dm/vishnu.svg
    :target: https://pypi.python.org/pypi/vishnu
    :alt: Downloads

.. image:: https://badge.fury.io/py/vishnu.svg
    :target: https://pypi.python.org/pypi/vishnu
    :alt: Latest Version

.. image:: https://travis-ci.org/anomaly/vishnu.svg?branch=master&maxAge=2592000
   :target: https://travis-ci.org/anomaly/vishnu/
   :alt: build status

Features
--------

- Cookie based session for python WSGI applications
- Configurable for the following cookie settings
    - Domain
    - Path
    - Secure
    - HttpOnly
    - Expires (timeout)
- Support for multiple backends
    - `Google App Engine Memcache <https://cloud.google.com/appengine/docs/standard/python/memcache/>`__
    - `Google App Engine NDB <https://cloud.google.com/appengine/docs/standard/python/ndb/>`__
    - `Python Memcached <https://pypi.python.org/pypi/python-memcached>`__
    - `PyMemcache <https://pypi.python.org/pypi/pymemcache>`__
    - `Redis <https://pypi.python.org/pypi/redis>`__
- HMAC signature to verify cookie has not been tampered with
- Autosave option which saves anytime a session value is modified
- Optional Encryption of cookie data using AES
- Custom timeout per session

Installation
------------

Vishnu is available on `PyPi <https://pypi.python.org/pypi/vishnu>`_ and we recommend installation via ``pip``.

.. code:: bash

    pip install vishnu

The following extra installations also exist which include the desired backend library as a requirement.

.. code:: bash

    pip install vishnu[pymemcache]
    pip install vishnu[python-memcached]
    pip install vishnu[redis]

If you are working with Google App Engine we recommend installation via `pip` as a `vendored package <https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27>`__.

.. code:: bash

    pip install -t lib vishnu

Edit the ``appengine_config.py`` file and provide your library directory to the ``vendor.add()`` method.

.. code:: python

    from google.appengine.ext import vendor

    vendor.add('lib')


Alternatively download your `preferred tagged release <https://github.com/anomaly/vishnu/releases>`__ and all you should have to include is the ``vishnu`` folder.

Configuration
-------------

Session Config
~~~~~~~~~~~~~~

The following parameters are available for session configuration.

+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| parameter       | required | default      | type    | description                                                                                           |
+=================+==========+==============+=========+=======================================================================================================+
| ``secret``      | yes      | ``None``     | string  | Secret used for HMAC signature, must be at least 32 characters.                                       |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``cookie_name`` | no       | ``vishnu``   | string  | Name to use for cookie.                                                                               |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``encrypt_key`` | no       | ``None``     | string  | Key used to encrypt cookie data, if omitted then data will not be encrypted.                          |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``secure``      | no       | ``True``     | bool    | Only send this cookie over SSL                                                                        |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``domain``      | no       | N/A          | string  | The domain to set the cookie for, it omitted will use domain cookie was served from.                  |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``path``        | no       | ``/``        | string  | The path to set the cookie for, if omitted it will default to ``/``                                   |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``http_only``   | no       | ``True``     | string  | Only allow cookies access via HTTP/HTTPS                                                              |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``auto_save``   | no       | ``False``    | bool    | Automatically save the session when a value is set.                                                   |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``timeout``     | no       | N/A          | integer | How long until session/cookie expires, it omitted it will last for the length of the browser session. |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+
| ``backend``     | yes      | N/A          | backend | See backends_ configuration                                                                           |
+-----------------+----------+--------------+---------+-------------------------------------------------------------------------------------------------------+

Example of a session configuration.

.. code:: python

    from vishnu.session import Config
    from vishnu.backend import Redis

    config = Config(
        secret="your_secret",
        backend=Redis()
    )

WSGI Middleware
~~~~~~~~~~~~~~~

To use vishnu you must add it as a middleware to your WSGI application.

.. code:: python

    from vishnu.backend import Redis
    from vishnu.middleware import SessionMiddleware
    from vishnu.session import Config


    my_config = Config(
        secret="your_secret",
        backend=Redis()
    )

    app = SessionMiddleware(app=wsgi_app, config=my_config)

Backends
~~~~~~~~

Google App Engine (memcache)
............................

.. code:: python

    from vishnu.backend import GoogleAppEngineMemcache

    config = Config(
        secret="your_secret",
        backend=GoogleAppEngineMemcache()
    )

Google App Engine (NDB)
.......................

.. code:: python

    from vishnu.backend import GoogleAppEngineNDB

    config = Config(
        secret="your_secret",
        backend=GoogleAppEngineNDB()
    )

PyMemcache
..........

+-----------+----------+---------------+---------+
| parameter | required | default       | type    |
+===========+==========+===============+=========+
| ``host``  | no       | ``localhost`` | string  |
+-----------+----------+---------------+---------+
| ``port``  | no       | ``11211``     | integer |
+-----------+----------+---------------+---------+

.. code:: python

    from vishnu.backend import PyMemcache

    config = Config(
        secret="your_secret",
        backend=PyMemcache(host="memcache.host", port=11222)
    )

PythonMemcached
...............

+-----------+----------+---------------+---------+
| parameter | required | default       | type    |
+===========+==========+===============+=========+
| ``host``  | no       | ``localhost`` | string  |
+-----------+----------+---------------+---------+
| ``port``  | no       | ``11211``     | integer |
+-----------+----------+---------------+---------+

.. code:: python

    from vishnu.backend import PythonMemcached

    config = Config(
        secret="your_secret",
        backend=PythonMemcached()
    )

Redis
.....

+-----------+----------+---------------+---------+
| parameter | required | default       | type    |
+===========+==========+===============+=========+
| ``host``  | no       | ``localhost`` | string  |
+-----------+----------+---------------+---------+
| ``port``  | no       | ``6379``      | integer |
+-----------+----------+---------------+---------+
| ``db``    | no       | ``0``         | integer |
+-----------+----------+---------------+---------+

.. code:: python

    from vishnu.backend import Redis

    config = Config(
        secret="your_secret",
        backend=Redis(host="redis.host", port=6421, db=0)
    )

Setting a Custom Timeout
~~~~~~~~~~~~~~~~~~~~~~~~

Each session uses the default timeout specified in your server config but if you want to have particular sessions differ to this you can do the following.

.. code:: python

    session = vishnu.get_session()
    session.timeout = 3600
    session.save()

The timeout is in seconds. To set the timeout to expire at the end of this session you can use the ``vishnu.session.TIMEOUT_SESSION`` constant.

.. code:: python

    session = vishnu.get_session()
    session.timeout = vishnu.session.TIMEOUT_SESSION
    session.save()

Cleaning up Expired Sessions (Google App Engine NDB backend only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following to a cron handler.

.. code:: python

    from vishnu.util import gae_ndb_delete_expired_sessions

    while not gae_ndb_delete_expired_sessions():
        pass

You can alter the period after expired sessions are deleted by passing a value in seconds as ``dormant_for``. You can also alter the amount of sessions to delete per call using the ``limit`` argument.

.. code:: python

    from vishnu.util import gae_ndb_delete_expired_sessions

    while not gae_ndb_delete_expired_sessions(dormant_for=3600, limit=100):
        pass