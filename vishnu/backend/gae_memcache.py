from vishnu.backend import Base

import pickle

from google.appengine.api import memcache

NAMESPACE = "vishnu"


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

        if not self._loaded:
            found_in_cache = memcache.get(self._sid, namespace=NAMESPACE)

            if found_in_cache is None:
                return False
            else:
                self._record = pickle.loads(found_in_cache)
                self._loaded = True

                self._expires = self._record.expires
                self._last_accessed = self._record.last_accessed
                self._data = self._record.data

        return True

    def clear(self):
        super(Backend, self).clear()
        if self._sid:
            memcache.delete(self._sid, namespace=NAMESPACE)

    def save(self, sync_only=False):
        import logging
        logging.error(self._sid)

        # todo: implement sync only

        self._record = VishnuSession(
            self._expires,
            self._last_accessed,
            self._data
        )

        memcache.set(self._sid, pickle.dumps(self._record), namespace=NAMESPACE)
