"""
Configuration for Google App Engine memcache API.
https://cloud.google.com/appengine/docs/standard/python/memcache/
"""
from vishnu.backend.config import Base


class Config(Base):
    """
    Configuration object for Google App Engine memcache API.

    Should be imported using the shortcut vishnu.backend.GoogleAppEngineMemcache
    """

    def client_from_config(self, sid):
        from vishnu.backend.client.memcache.gae import Client
        return Client(sid)
