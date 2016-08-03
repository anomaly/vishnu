from google.appengine.ext import ndb

from  Cookie import SimpleCookie

from base64 import b64decode, b64encode
import hashlib
import hmac
import logging
import os
import uuid

class SavedSession(ndb.Model):
    expires = ndb.DateTimeProperty(required=False)

COOKIE_NAME = "vishnu"
SIG_LENGTH = 128
SID_LENGTH = 32

class Session(object):

    def __init__(self):
        self._needs_save = True
        self._data = {}
        self._sid = uuid.uuid4().hex

        #try to fetch the default values for this session

        self._secret = os.environ.get("VISHNU_SECRET")
        #error if secret missing

        secure = os.environ.get("VISHNU_SECURE")
        if secure is None:
            self._secure = True
        else:
            self._secure = secure == "True"

        http_only = os.environ.get("VISHNU_HTTP_ONLY")
        if http_only is None:
            self._http_only = True
        else:
            self._http_only = http_only == "True"

        timeout = os.environ.get("VISHNU_TIMEOUT")
        if timeout is not None:
            try:
                self._timeout = int(timeout)
            except ValueError:
                raise TypeError("VISHNU_TIMEOUT must be a non-negative integer")

            if self._timeout < 0:
                raise TypeError("VISHNU_TIMEOUT must be a non-negative integer")
        else:
            self._timeout = None

        #attempt to load an existing cookie
        self._load_cookie()

    def _load_cookie(self):

        cookie = SimpleCookie(os.environ.get('HTTP_COOKIE'))
        vishnu_keys = filter(lambda key: key == COOKIE_NAME, cookie.keys())
        
        #no session was started yet
        if not vishnu_keys:
            return

        cookie_value = cookie[vishnu_keys[0]].value
        received_sid = Session.decode_sid(self._secret, cookie_value)
        if received_sid:
            self._sid = received_sid
            self._needs_save = False
        else:
            logging.warn("found cookie with invalid signature")

    def headers(self):
        headers = []

        if self._needs_save:

            cookie_value = Session.encode_sid(self._secret, self._sid)

            #@todo: encrypt

            header = "vishnu=%s;" % cookie_value
            if self._secure:
                header += " Secure;"
            if self._http_only:
                header += " HttpOnly"

            if header:
                headers.append(header)

            #no timeout means this cookie is session only

        return headers

    def encrypt_data(self, data):
        pass

    def decrypt_data(self, data):
        pass

    @classmethod
    def encode_sid(cls, secret, sid):
        """
        Computes the HMAC for the given session id.
        """
        sig = hmac.new(secret, sid, hashlib.sha512).hexdigest()
        return "%s%s" % (sig, sid)

    @classmethod
    def is_signature_equal(cls, a, b):
        """Compares two signatures using a constant time algorithim to avoid timing attacks."""
        if len(a) != len(b):
            return False

        invalid_chars = 0
        for x, y in zip(a, b):
            if x != y:
                invalid_chars += 1
        return invalid_chars == 0

    @classmethod
    def decode_sid(cls, secret, cookie_value):
        """
        Decodes a cookie value and returns the sid if value or None if invalid.
        """
        if len(cookie_value) > SIG_LENGTH + SID_LENGTH:
            logging.warn("cookie value is incorrect length")
            return None

        cookie_sig = cookie_value[:SIG_LENGTH]
        cookie_sid = cookie_value[SIG_LENGTH:]
        actual_sig = hmac.new(secret, cookie_sid, hashlib.sha512).hexdigest()

        if not Session.is_signature_equal(cookie_sig, actual_sig):
            return None
        
        return cookie_sid

    def start(self):
        self._needs_save = True

    def end(self):
        pass

    def get(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        self._data[key] = value