"""
Client wrapper for pylibmc memcache library
http://sendapatch.se/projects/pylibmc/
"""
from __future__ import absolute_import

from vishnu.backend.client import Base
from vishnu.backend.client import PicklableSession

import pickle
from pylibmc import Client as PylibmcClient


class Client(Base):
    """
    Client object for pylibmc memcache library
    """

    def __init__(self, sid, host, port):
        super(Client, self).__init__(sid)
        self._memcache = PylibmcClient(["%s:%s" % (host, port)])

        self._record = None

    def load(self):

        if not self._loaded:
            found_in_cache = self._memcache.get(self._sid)

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
            self._memcache.delete(self._sid)

    def save(self, sync_only=False):

        # todo: implement sync only

        self._record = PicklableSession(
            self._expires,
            self._last_accessed,
            self._data
        )

        self._memcache.set(self._sid, pickle.dumps(self._record))
