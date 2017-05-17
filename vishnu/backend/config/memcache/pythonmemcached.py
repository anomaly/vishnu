"""
Configuration for python-memcached memcache library
https://pypi.python.org/pypi/python-memcached
"""
from vishnu.backend.config import Base
from vishnu.backend.config.memcache import DEFAULT_HOST, DEFAULT_PORT


class Config(Base):
    """
    Configuration object for python-memcached memcache library.

    Should be imported using the shortcut vishnu.backend.PythonMemcached
    """

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super(Config, self).__init__()

        if not isinstance(host, str):
            raise TypeError("host must be a string")

        self._host = host

        if not isinstance(port, int):
            raise TypeError("port must be a non-negative integer")

        if port < 0:
            raise TypeError("port must be a non-negative integer")

        self._port = port

    @property
    def host(self):
        """
        :return: the host of the memcache instance
        :rtype: string
        """
        return self._host

    @property
    def port(self):
        """
        :return: the port of the memcache instance
        :rtype: integer
        """
        return self._port

    def client_from_config(self, sid):
        from vishnu.backend.client.memcache.pythonmemcached import Client
        return Client(sid, self._host, self._port)
