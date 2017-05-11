"""
Configuration for pymemcache memcache library.
https://pypi.python.org/pypi/pymemcache
"""
from vishnu.backend.config import Base
from vishnu.backend.config.memcache import DEFAULT_HOST, DEFAULT_PORT


class Config(Base):
    """
    Configuration object for pymemcache memcache library.

    Should be imported using the shortcut vishnu.backend.PyMemcache
    """

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super(Config, self).__init__()

        # todo: check valid host
        self._host = host

        # todo: check valid port
        self._port = port

    def client_from_config(self, sid):
        from vishnu.backend.client.memcache.pymemcache import Client
        return Client(sid, self._host, self._port)
