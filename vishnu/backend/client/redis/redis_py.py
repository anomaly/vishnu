"""
Client wrapper for python redis library
https://pypi.python.org/pypi/redis
"""
from vishnu.backend.client import Base
from vishnu.backend.client import PicklableSession

import pickle
import redis


class Client(Base):
    """
    Client object for python redis library
    """

    def __init__(self, sid, host, port, db):
        super(Client, self).__init__(sid)

        self._redis = redis.StrictRedis(host=host, port=port, db=db)

        self._record = None

    def load(self):

        if not self._loaded:
            found_in_cache = self._redis.get(self._sid)

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
            self._redis.delete(self._sid)

    def save(self, sync_only=False):

        # todo: implement sync only

        self._record = PicklableSession(
            self._expires,
            self._last_accessed,
            self._data
        )

        self._redis.set(self._sid, pickle.dumps(self._record))
