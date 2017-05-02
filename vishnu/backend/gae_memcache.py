from vishnu.backend import Base

from google.appengine.api import memcache


class VishnuSession(object):

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


class Backend(Base):

    def __init__(self, sid):
        super(Backend, self).__init__(sid)
        self._record = None

    def load(self):

        if self._record is None and not self._loaded:
            self._record = memcache.get(self._sid)

            if self._record is None:
                return False, None, None
            else:
                self._loaded = True
                self._data = self._record.data

        return True, self._record.last_accessed, self._record.expires

    def clear(self):
        super(Backend, self).clear()
        if self._sid:
            memcache.delete(self._sid)

    def save(self, last_accessed, expires=None, sync_only=False):

        self._record = memcache.get(self._sid)