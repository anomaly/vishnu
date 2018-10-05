"""
Client wrapper for Google Cloud Datastore
https://cloud.google.com/datastore
"""
from vishnu.backend.client import Base

from google.cloud import datastore
#
#
# class VishnuSession(ndb.Model):  # pylint: disable=R0903, W0232
#     """NDB model for storing session"""
#     expires = ndb.DateTimeProperty(required=False)
#     last_accessed = ndb.DateTimeProperty(required=True)
#     data = ndb.PickleProperty(required=True, compressed=True)


class Client(Base):
    """
    Client object for Google Cloud Datastore
    """

    def __init__(self, sid):
        super(Client, self).__init__(sid)

        self._client = datastore.Client()
        self._key = self._client.key('VishnuSession', self._sid)

    def load(self):
        if not self._loaded:
            entity = self._client.get(self._key)
            if entity is None:
                return False
            else:
                self._loaded = True

                self.expires = entity.get("expires")
                self.last_accessed = entity.get("last_accessed")

                data = entity.get("data")
                if data is not None:
                    self._data = data

        return True

    def clear(self):
        self._data = {}
        self._client.delete(self._key)

    def save(self, sync_only=False):
        """
        :param sync_only:
        :type: bool
        """

        entity = datastore.Entity(key=self._key)
        entity["last_accessed"] = self.last_accessed

        if not sync_only:
            entity["data"] = self._data
            if self.expires:
                entity["expires"] = self.expires

        self._client.put(entity)