"""
Client wrapper for Google App Engine memcache API
https://cloud.google.com/appengine/docs/standard/python/memcache/
"""
from vishnu.backend.client import Base
from vishnu.backend.client import PicklableSession

from google.appengine.api import memcache
import pickle

NAMESPACE = "vishnu"


class Client(Base):
    """
    Client object for Google App Engine memcache API
    """

    def __init__(self, sid):
        super(Client, self).__init__(sid)
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
        super(Client, self).clear()
        if self._sid:
            memcache.delete(self._sid, namespace=NAMESPACE)

    def save(self, sync_only=False):

        # todo: implement sync only

        self._record = PicklableSession(
            self._expires,
            self._last_accessed,
            self._data
        )

        memcache.set(self._sid, pickle.dumps(self._record), namespace=NAMESPACE)
