"""
Client wrapper for Google App Engine NDB
https://cloud.google.com/appengine/docs/standard/python/ndb/
"""
from vishnu.backend.client import Base

from google.appengine.ext import ndb


class VishnuSession(ndb.Model):  # pylint: disable=R0903, W0232
    """NDB model for storing session"""
    expires = ndb.DateTimeProperty(required=False)
    last_accessed = ndb.DateTimeProperty(required=True)
    data = ndb.PickleProperty(required=True, compressed=True)


class Client(Base):
    """
    Client object for Google App Engine NDB
    """

    def __init__(self, sid):
        super(Client, self).__init__(sid)
        self._model = None

    def load(self):
        if self._model is None and not self._loaded:
            self._model = ndb.Key(VishnuSession, self._sid).get()
            if self._model is None:
                return False
            else:
                self._loaded = True

                self.expires = self._model.expires
                self.last_accessed = self._model.last_accessed
                self._data = self._model.data

        return True

    def clear(self):
        self._data = {}
        if self._model:
            self._model.key.delete()
            self._model = None

    def save(self, sync_only=False):
        # try to find an existing session
        self._model = ndb.Key(VishnuSession, self._sid).get()
        if self._model is None:
            self._model = VishnuSession(id=self._sid)

        if sync_only:
            self._model.last_accessed = self.last_accessed
        else:
            self._model.data = self._data
            self._model.last_accessed = self.last_accessed
        if self.expires:
            self._model.expires = self.expires

        self._model.put()
