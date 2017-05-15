import abc
from datetime import datetime


class PicklableSession(object):

    def __init__(self, expires, last_accessed, data):
        self._expires = expires
        self._last_accessed = last_accessed
        self._data = data

    @property
    def expires(self):
        return self._expires

    @property
    def last_accessed(self):
        return self._last_accessed

    @property
    def data(self):
        return self._data


class Base(object):

    def __init__(self, sid):
        self._sid = sid
        self._loaded = False

        self._expires = None
        self._last_accessed = None

        self._data = {}

    @property
    def expires(self):
        return self._expires

    @expires.setter
    def expires(self, value):
        self._expires = value

    @property
    def last_accessed(self):
        return self._last_accessed

    @last_accessed.setter
    def last_accessed(self, value):
        self._last_accessed = value

    def get(self, key):
        self.last_accessed = datetime.now()
        return self._data.get(key)

    def __setitem__(self, key, value):
        self.last_accessed = datetime.now()
        self._data[key] = value

    @abc.abstractmethod
    def load(self):
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self):
        self._loaded = False

        self._expires = None
        self._last_accessed = None
        self._data = {}

    @abc.abstractmethod
    def save(self, sync_only=False):
        raise NotImplementedError
