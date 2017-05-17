"""
Configuration for Google App Engine NDB.
https://cloud.google.com/appengine/docs/standard/python/ndb/
"""
from vishnu.backend.config import Base


class Config(Base):
    """
    Configuration object for Google App Engine NDB.

    Should be imported using the shortcut vishnu.backend.GoogleAppEngineNDB
    """

    def client_from_config(self, sid):
        from vishnu.backend.client.ndb.gae import Client
        return Client(sid)
