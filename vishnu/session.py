"""
Vishnu session.
"""

from __future__ import absolute_import

from google.appengine.ext import ndb

from  Cookie import SimpleCookie

from datetime import datetime, timedelta
import hashlib
import hmac
import logging
import os
import uuid

class VishnuSession(ndb.Model): #pylint: disable=R0903, W0232
    """NDB model for storing session"""
    expires = ndb.DateTimeProperty(required=False)
    data = ndb.PickleProperty(required=True, compressed=True)

#constant used for specifying this cookie should expire at the end of the session
TIMEOUT_SESSION = "timeout_session"

DEFAULT_COOKIE_NAME = "vishnu"
SIG_LENGTH = 128
SID_LENGTH = 32
EXPIRES_FORMAT = "%a, %d-%b-%Y %H:%M:%S GMT"


class Session(object): #pylint: disable=R0902, R0904
    """The vishnu session object."""

    def __init__(self): #pylint: disable=R0912, R0915
        self._send_cookie = False
        self._expire_cookie = False

        self._data = {}
        self._sid = uuid.uuid4().hex
        self._model = None
        self._loaded = False

        #try to fetch the default values for this session
        #cookie name
        cookie_name = os.environ.get("VISHNU_COOKIE_NAME")
        if cookie_name is None:
            self._cookie_name = DEFAULT_COOKIE_NAME
        else:
            self._cookie_name = cookie_name

        #secret
        self._secret = os.environ.get("VISHNU_SECRET")
        #error if secret missing

        #secure
        secure = os.environ.get("VISHNU_SECURE")
        if secure is None:
            self._secure = True
        else:
            self._secure = secure == "True"

        #domain
        domain = os.environ.get("VISHNU_DOMAIN")
        if domain is None:
            self._domain = None
        else:
            self._domain = domain

        #path
        path = os.environ.get("VISHNU_PATH")
        if path is None:
            self._path = "/"
        else:
            self._path = path

        #http only
        http_only = os.environ.get("VISHNU_HTTP_ONLY")
        if http_only is None:
            self._http_only = True
        else:
            self._http_only = http_only == "True"

        #auto save
        auto_save = os.environ.get("VISHNU_AUTO_SAVE")
        if auto_save is None:
            self._auto_save = False
        else:
            self._auto_save = auto_save == "True"

        #timeout
        timeout = os.environ.get("VISHNU_TIMEOUT")
        if timeout is not None:
            try:
                self._timeout = int(timeout)
            except ValueError:
                raise TypeError("VISHNU_TIMEOUT must be a non-negative integer")

            if self._timeout < 0:
                raise TypeError("VISHNU_TIMEOUT must be a non-negative integer")

            #calculate the expiry date
            self._calculate_expires()
        else:
            self._timeout = None
            self._expires = None

        #attempt to load an existing cookie
        self._load_cookie()

    @property
    def timeout(self):
        """Fetch the current timeout value for this session"""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """Sets a custom timeout value for this session"""

        if value == TIMEOUT_SESSION:
            self._timeout = None
            self._expires = None
        else:
            self._timeout = value
            self._calculate_expires()

    def _calculate_expires(self):
        """Calculates the session expiry using the timeout"""
        self._expires = None

        now = datetime.now()
        self._expires = now + timedelta(seconds=self._timeout)

    def _load_cookie(self):
        """Loads HTTP Cookie from environ"""

        cookie = SimpleCookie(os.environ.get('HTTP_COOKIE'))
        vishnu_keys = [key for key in cookie.keys() if key == self._cookie_name]

        #no session was started yet
        if not vishnu_keys:
            return

        cookie_value = cookie[vishnu_keys[0]].value
        received_sid = Session.decode_sid(self._secret, cookie_value)
        if received_sid:
            self._sid = received_sid
        else:
            logging.warn("found cookie with invalid signature")

    def header(self):
        """Generates HTTP header for this cookie."""

        if self._send_cookie:

            cookie_value = Session.encode_sid(self._secret, self._sid)
            #@todo: encrypt

            header = "%s=%s;" % (self._cookie_name, cookie_value)

            if self._domain:
                header += " Domain=%s;" % self._domain

            if self._path:
                header += " Path=%s;" % self._path

            #expire the cookie
            if self._expire_cookie:
                header += " Expires=Wed, 01-Jan-1970 00:00:00 GMT;"
            #set the cookie expiry
            elif self._timeout:
                header += " Expires=%s;" % self._expires.strftime(EXPIRES_FORMAT)

            if self._secure:
                header += " Secure;"
            if self._http_only:
                header += " HttpOnly"

            return header
        else:
            return None

    @classmethod
    def encrypt_cookie_value(cls, secret, cookie_value):
        """Encrypts the given cookie value."""
        pass

    @classmethod
    def decrypt_cookie_value(cls, secret, cookie_value):
        """Decrypts the given cookie value."""
        pass

    @classmethod
    def encode_sid(cls, secret, sid):
        """Computes the HMAC for the given session id."""
        sig = hmac.new(secret, sid, hashlib.sha512).hexdigest()
        return "%s%s" % (sig, sid)

    @classmethod
    def is_signature_equal(cls, sig_a, sig_b):
        """Compares two signatures using a constant time algorithim to avoid timing attacks."""
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

    def _load_data(self):
        """Loads data dict from NDB datastore."""
        #load the persistent model on first access
        if self._model is None and not self._loaded:
            self._model = ndb.Key(VishnuSession, self._sid).get()
            self._loaded = True
            if self._model:
                self._data = self._model.data

    def _clear_data(self):
        """Deletes session from NDB datastore."""
        self._load_data()
        if self._model:
            self._model.key.delete()
            self._model = None

    def start(self):
        """Starts a new session."""
        self._data = {}

    def save(self):
        """Saves session to persisten storage (NDB datastore)."""

        #try to find an existing session
        self._model = ndb.Key(VishnuSession, self._sid).get()
        if self._model is None:
            self._model = VishnuSession(id=self._sid)
        self._model.data = self._data
        if self._expires:
            self._model.expires = self._expires
        self._model.put()

        self._send_cookie = True

    def terminate(self):
        """Terminates an active session"""
        self._data = {}
        self._clear_data()
        self._expire_cookie = True
        self._send_cookie = True

    def get(self, key):
        """Retrieve a value from the session dictionary"""
        self._load_data()
        return self._data.get(key)

    def __setitem__(self, key, value):
        """Set a value in the session dictionary"""
        self._load_data()

        if self._auto_save:
            self.save()
        self._data[key] = value
