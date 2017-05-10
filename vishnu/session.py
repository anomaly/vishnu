"""
Vishnu session.
"""

from __future__ import absolute_import

from Cookie import SimpleCookie

from datetime import datetime, timedelta
import hashlib
import hmac
import logging
import uuid

from vishnu.cipher import AESCipher
from vishnu.backend import BackendType

# constant used for specifying this cookie should expire at the end of the session
TIMEOUT_SESSION = "timeout_session"

SECRET_MIN_LEN = 32
ENCRYPT_KEY_MIN_LEN = 32

DEFAULT_COOKIE_NAME = "vishnu"
DEFAULT_BACKEND = BackendType.GoogleAppEngineNDB
DEFAULT_MEMCACHE_HOST = "localhost"
DEFAULT_MEMCACHE_PORT = "11211"

SIG_LENGTH = 128
SID_LENGTH = 32
EXPIRES_FORMAT = "%a, %d-%b-%Y %H:%M:%S GMT"


class Session(object):  # pylint: disable=R0902, R0904
    """The vishnu session object."""

    def __init__(self, environ):  # pylint: disable=R0912, R0915

        self._environ = environ
        self._send_cookie = False
        self._expire_cookie = False
        self._started = False

        self._sid = uuid.uuid4().hex
        self._loaded = False

        # try to fetch the default values for this session
        # cookie name
        cookie_name = environ.get("VISHNU_COOKIE_NAME")
        if cookie_name is None:
            self._cookie_name = DEFAULT_COOKIE_NAME
        else:
            self._cookie_name = cookie_name

        # secret
        self._secret = environ.get("VISHNU_SECRET")
        if self._secret is None or len(self._secret) < SECRET_MIN_LEN:
            raise ValueError("Secret should be at least %i characters" % SECRET_MIN_LEN)

        # encrypt key
        self._encrypt_key = environ.get("VISHNU_ENCRYPT_KEY")
        if self._encrypt_key is not None and len(self._encrypt_key) < ENCRYPT_KEY_MIN_LEN:
            raise ValueError("Encrypt key should be at least %i characters" % ENCRYPT_KEY_MIN_LEN)

        # secure
        secure = environ.get("VISHNU_SECURE")
        if secure is None:
            self._secure = True
        else:
            self._secure = secure == "True"

        # domain
        domain = environ.get("VISHNU_DOMAIN")
        if domain is None:
            self._domain = None
        else:
            self._domain = domain

        # path
        path = environ.get("VISHNU_PATH")
        if path is None:
            self._path = "/"
        else:
            self._path = path

        # http only
        http_only = environ.get("VISHNU_HTTP_ONLY")
        if http_only is None:
            self._http_only = True
        else:
            self._http_only = http_only == "True"

        # auto save
        self._needs_save = False
        auto_save = environ.get("VISHNU_AUTO_SAVE")
        if auto_save is None:
            self._auto_save = False
        else:
            self._auto_save = auto_save == "True"

        # timeout
        timeout = environ.get("VISHNU_TIMEOUT")
        if timeout is not None:
            try:
                self._timeout = int(timeout)
            except ValueError:
                raise TypeError("VISHNU_TIMEOUT must be a non-negative integer")

            if self._timeout < 0:
                raise TypeError("VISHNU_TIMEOUT must be a non-negative integer")

            # calculate the expiry date
            self._calculate_expires()
        else:
            self._timeout = None

        # configure the backend
        backend = environ.get("VISHNU_BACKEND")
        if backend is None:
            backend = DEFAULT_BACKEND

        backend_host = environ.get("VISHNU_BACKEND_HOST")
        if backend_host is None and backend == BackendType.PythonMemcached:
            backend_host = DEFAULT_MEMCACHE_HOST
        elif backend_host is None and backend == BackendType.PyMemcache:
            backend_host = DEFAULT_MEMCACHE_HOST

        backend_port = environ.get("VISHNU_BACKEND_PORT")
        if backend_port is None and backend == BackendType.PythonMemcached:
            backend_port = DEFAULT_MEMCACHE_PORT
        elif backend_port is None and backend == BackendType.PyMemcache:
            backend_port = DEFAULT_MEMCACHE_PORT

        # attempt to load an existing cookie
        self._load_cookie()
        self._configure_backend(backend, backend_host, backend_port)

    @property
    def cookie_name(self):
        return self._cookie_name

    @property
    def started(self):
        """
        Has the session been started?
         - True if autosave is on and session has been modified
         - True if autosave is off if session has been saved at least once
         - True is a matching persistent session was found
        """
        return self._started

    @property
    def needs_save(self):
        """Does this session need to be saved."""
        return self._needs_save

    @property
    def auto_save(self):
        """Does this session have auto save enabled."""
        return self._auto_save

    @property
    def timeout(self):
        """Fetch the current timeout value for this session"""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """Sets a custom timeout value for this session"""

        if value == TIMEOUT_SESSION:
            self._timeout = None
            self._backend.expires = None
        else:
            self._timeout = value
            self._calculate_expires()

    def _calculate_expires(self):
        """Calculates the session expiry using the timeout"""
        self._backend.expires = None

        now = datetime.now()
        self._backend.expires = now + timedelta(seconds=self._timeout)

    def _load_cookie(self):
        """Loads HTTP Cookie from environ"""

        cookie = SimpleCookie(self._environ.get('HTTP_COOKIE'))
        vishnu_keys = [key for key in cookie.keys() if key == self._cookie_name]

        # no session was started yet
        if not vishnu_keys:
            return

        cookie_value = cookie[vishnu_keys[0]].value
        if self._encrypt_key:
            cipher = AESCipher(self._encrypt_key)
            cookie_value = cipher.decrypt(cookie_value)
        received_sid = Session.decode_sid(self._secret, cookie_value)
        if received_sid:
            self._sid = received_sid
        else:
            logging.warn("found cookie with invalid signature")

    def _configure_backend(self, backend_type, host, port):
        """Configures a backend for this session to use"""

        if backend_type == BackendType.GoogleAppEngineNDB:
            from vishnu.backend.gae_ndb import Backend
            self._backend = Backend(self._sid)
        elif backend_type == BackendType.GoogleAppEngineMemcache:
            from vishnu.backend.memcache_gae import Backend
            self._backend = Backend(self._sid)
        elif backend_type == BackendType.PythonMemcached:
            from vishnu.backend.memcache_pythonmemcached import Backend
            self._backend = Backend(self._sid, host, port)
        elif backend_type == BackendType.PyMemcache:
            from vishnu.backend.memcache_pymemcache import Backend
            self._backend = Backend(self._sid, host, port)
        else:
            raise ValueError("Unknown backend type: %s" % backend_type)

    def header(self):
        """Generates HTTP header for this cookie."""

        if self._send_cookie:

            cookie_value = Session.encode_sid(self._secret, self._sid)
            if self._encrypt_key:
                cipher = AESCipher(self._encrypt_key)
                cookie_value = cipher.encrypt(cookie_value)

            header = "%s=%s;" % (self._cookie_name, cookie_value)

            if self._domain:
                header += " Domain=%s;" % self._domain

            if self._path:
                header += " Path=%s;" % self._path

            # expire the cookie
            if self._expire_cookie:
                header += " Expires=Wed, 01-Jan-1970 00:00:00 GMT;"
            # set the cookie expiry
            elif self._backend.expires:
                header += " Expires=%s;" % self._backend.expires.strftime(EXPIRES_FORMAT)

            if self._secure:
                header += " Secure;"
            if self._http_only:
                header += " HttpOnly"

            return header
        else:
            return None

    @classmethod
    def encode_sid(cls, secret, sid):
        """Computes the HMAC for the given session id."""
        sig = hmac.new(secret, sid, hashlib.sha512).hexdigest()
        return "%s%s" % (sig, sid)

    @classmethod
    def is_signature_equal(cls, sig_a, sig_b):
        """Compares two signatures using a constant time algorithm to avoid timing attacks."""
        if len(sig_a) != len(sig_b):
            return False

        invalid_chars = 0
        for char_a, char_b in zip(sig_a, sig_b):
            if char_a != char_b:
                invalid_chars += 1
        return invalid_chars == 0

    @classmethod
    def decode_sid(cls, secret, cookie_value):
        """Decodes a cookie value and returns the sid if value or None if invalid."""
        if len(cookie_value) > SIG_LENGTH + SID_LENGTH:
            logging.warn("cookie value is incorrect length")
            return None

        cookie_sig = cookie_value[:SIG_LENGTH]
        cookie_sid = cookie_value[SIG_LENGTH:]
        actual_sig = hmac.new(secret, cookie_sid, hashlib.sha512).hexdigest()

        if not Session.is_signature_equal(cookie_sig, actual_sig):
            return None

        return cookie_sid

    def save(self, sync_only=False):

        # saving a session marks it as started
        self._started = True

        self._backend.save(sync_only)

        self._send_cookie = True
        self._needs_save = False

    def terminate(self):
        """Terminates an active session"""
        self._backend.clear()
        self._needs_save = False
        self._started = False
        self._expire_cookie = True
        self._send_cookie = True

    def get(self, key):
        """Retrieve a value from the session dictionary"""
        self._started = self._backend.load()
        self._needs_save = True

        return self._backend.get(key)

    def __setitem__(self, key, value):
        """Set a value in the session dictionary"""
        self._started = self._backend.load()
        self._needs_save = True

        # if autosave is on then a session is automatically started when set
        if self._auto_save:
            self._started = True

        self._backend[key] = value
