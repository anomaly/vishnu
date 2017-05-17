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
from vishnu.backend.config import Base as BackendConfig

# constant used for specifying this cookie should expire at the end of the session
TIMEOUT_SESSION = "timeout_session"

SECRET_MIN_LEN = 32
ENCRYPT_KEY_MIN_LEN = 32

DEFAULT_COOKIE_NAME = "vishnu"
DEFAULT_PATH = "/"

SIG_LENGTH = 128
SID_LENGTH = 32
EXPIRES_FORMAT = "%a, %d-%b-%Y %H:%M:%S GMT"


class Config(object):

    def __init__(self, secret, cookie_name=None, encrypt_key=None,
                 secure=True, domain=None, path=None, http_only=True,
                 auto_save=False, timeout=None, backend=None):

        self._secret = secret
        if self._secret is None or len(self._secret) < SECRET_MIN_LEN:
            raise ValueError("Secret should be at least %i characters" % SECRET_MIN_LEN)

        if cookie_name is None:
            cookie_name = DEFAULT_COOKIE_NAME

        # todo: check cookie name is a string

        self._cookie_name = cookie_name

        self._encrypt_key = encrypt_key
        if self._encrypt_key is not None and len(self._encrypt_key) < ENCRYPT_KEY_MIN_LEN:
            raise ValueError("Encrypt key should be at least %i characters" % ENCRYPT_KEY_MIN_LEN)

        # todo: check secure is a bool

        self._secure = secure

        # todo: check domain is a string

        self._domain = domain

        if path is None:
            path = DEFAULT_PATH

        # todo: check path is a string

        self._path = path

        # todo: check http_only is a bool

        self._http_only = http_only

        # todo: check auto save is a bool

        self._auto_save = auto_save

        self._timeout = None
        if timeout is not None:
            try:
                self._timeout = int(timeout)
            except ValueError:
                raise TypeError("timeout must be a non-negative integer")

            if self._timeout < 0:
                raise TypeError("timeout must be a non-negative integer")

        if backend is None or not isinstance(backend, BackendConfig):
            raise TypeError("unknown backend configuration received")
        self._backend = backend

    @property
    def secret(self):
        """
        :return: secret used for HMAC signature
        :rtype: string
        """
        return self._secret

    @property
    def cookie_name(self):
        """
        :return: the name for the cookie
        :rtype: string
        """
        return self._cookie_name

    @property
    def encrypt_key(self):
        """
        :return: key to use for encryption
        :rtype: string
        """
        return self._encrypt_key

    @property
    def secure(self):
        """
        :return: whether the cookie can only be transmitted over HTTPS
        :rtype: boolean
        """
        return self._secure

    @property
    def domain(self):
        """
        :return: the domain the cookie is valid for
        :rtype: string
        """
        return self._domain

    @property
    def path(self):
        """
        :return: the path the cookie is valid for
        :rtype: string
        """
        return self._path

    @property
    def http_only(self):
        """
        :return: whether the cookie should only be sent over HTTP/HTTPS
        :rtype: boolean
        """
        return self._http_only

    @property
    def auto_save(self):
        """
        :return: whether this session should auto save
        :rtype: boolean
        """
        return self._auto_save

    @property
    def timeout(self):
        return self._timeout

    @property
    def backend(self):
        """
        :return: config for desired backend
        :rtype: vishnu.backend.config.Base
        """
        return self._backend


class Session(object):
    """The vishnu session object."""

    def __init__(self, environ, config):

        self._environ = environ

        self._send_cookie = False
        self._expire_cookie = False
        self._started = False

        self._sid = Session.generate_sid()
        self._loaded = False
        self._needs_save = False

        # todo: check config is correct class
        self._config = config

        # calculate the expiry date if a timeout exists
        if self._config.timeout:
            self._calculate_expires()

        # attempt to load an existing cookie
        self._load_cookie()
        self._backend_client = self._config.backend.client_from_config(self._sid)

    @classmethod
    def generate_sid(cls):
        """
        :return: generates a unique ID for use by a session
        :rtype: string
        """
        return uuid.uuid4().hex


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
    def auto_save(self):
        return self._config.auto_save

    @property
    def needs_save(self):
        """Does this session need to be saved."""
        return self._needs_save

    @property
    def timeout(self):
        """Fetch the current timeout value for this session"""
        return self._config.timeout

    @timeout.setter
    def timeout(self, value):
        """Sets a custom timeout value for this session"""

        if value == TIMEOUT_SESSION:
            self._config.timeout = None
            self._backend_client.expires = None
        else:
            self._config.timeout = value
            self._calculate_expires()

    def _calculate_expires(self):
        """Calculates the session expiry using the timeout"""
        self._backend_client.expires = None

        now = datetime.now()
        self._backend_client.expires = now + timedelta(seconds=self._config.timeout)

    def _load_cookie(self):
        """Loads HTTP Cookie from environ"""

        cookie = SimpleCookie(self._environ.get('HTTP_COOKIE'))
        vishnu_keys = [key for key in cookie.keys() if key == self._config.cookie_name]

        # no session was started yet
        if not vishnu_keys:
            return

        cookie_value = cookie[vishnu_keys[0]].value
        if self._config.encrypt_key:
            cipher = AESCipher(self._config.encrypt_key)
            cookie_value = cipher.decrypt(cookie_value)
        received_sid = Session.decode_sid(self._config.secret, cookie_value)
        if received_sid:
            self._sid = received_sid
        else:
            logging.warn("found cookie with invalid signature")

    def header(self):
        """Generates HTTP header for this cookie."""

        if self._send_cookie:

            cookie_value = Session.encode_sid(self._config.secret, self._sid)
            if self._config.encrypt_key:
                cipher = AESCipher(self._config.encrypt_key)
                cookie_value = cipher.encrypt(cookie_value)

            header = "%s=%s;" % (self._config.cookie_name, cookie_value)

            if self._config.domain:
                header += " Domain=%s;" % self._config.domain

            if self._config.path:
                header += " Path=%s;" % self._config.path

            # expire the cookie
            if self._expire_cookie:
                header += " Expires=Wed, 01-Jan-1970 00:00:00 GMT;"
            # set the cookie expiry
            elif self._backend_client.expires:
                header += " Expires=%s;" % self._backend_client.expires.strftime(EXPIRES_FORMAT)

            if self._config.secure:
                header += " Secure;"
            if self._config.http_only:
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

        self._backend_client.save(sync_only)

        self._expire_cookie = False
        self._send_cookie = True
        self._needs_save = False

    def terminate(self):
        """Terminates an active session"""
        self._backend_client.clear()
        self._needs_save = False
        self._started = False
        self._expire_cookie = True
        self._send_cookie = True

    def get(self, key):
        """Retrieve a value from the session dictionary"""
        self._started = self._backend_client.load()
        self._needs_save = True

        return self._backend_client.get(key)

    def __setitem__(self, key, value):
        """Set a value in the session dictionary"""
        self._started = self._backend_client.load()
        self._needs_save = True

        # if autosave is on then a session is automatically started when set
        if self._config.auto_save:
            self._started = True

        self._backend_client[key] = value
