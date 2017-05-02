from vishnu.backend import Base

from google.appengine.ext import ndb


class VishnuSession(ndb.Model):  # pylint: disable=R0903, W0232
    """NDB model for storing session"""
    expires = ndb.DateTimeProperty(required=False)
    last_accessed = ndb.DateTimeProperty(required=True)
    data = ndb.PickleProperty(required=True, compressed=True)


class Backend(Base):

    def __init__(self):
        super(Backend, self).__init__()
        self._model = None

    def load(self, sid):
        self._sid = sid

        if self._model is None and not self._loaded:
            self._model = ndb.Key(VishnuSession, self._sid).get()
            if self._model is None:
                return False, None, None
            else:
                self._loaded = True
                self._data = self._model.data

        return True, self._model.last_accessed, self._model.expires

    def clear(self):
        self._data = {}
        if self._model:
            self._model.key.delete()
            self._model = None

    def save(self, last_accessed, expires=None, sync_only=False):
        # try to find an existing session
        self._model = ndb.Key(VishnuSession, self._sid).get()
        if self._model is None:
            self._model = VishnuSession(id=self._sid)

        if sync_only:
            self._model.last_accessed = last_accessed
        else:
            self._model.data = self._data
            self._model.last_accessed = last_accessed
        if expires:
            self._model.expires = expires

        self._model.put()