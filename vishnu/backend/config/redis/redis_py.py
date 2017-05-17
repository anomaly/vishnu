"""
Configuration object for python redis library.
https://pypi.python.org/pypi/redis
"""
from vishnu.backend.config import Base
from vishnu.backend.config.redis import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_DB


class Config(Base):
    """
    Configuration object for python redis library.

    Should be imported using the shortcut vishnu.backend.Redis
    """

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, db=DEFAULT_DB):
        """
        :param host: host on which redis is available
        :rtype: string
        :param port: port on which redis is running
        :rtype: int
        :param db: db
        :rtype: int
        """
        super(Config, self).__init__()

        if not isinstance(host, str):
            raise TypeError("host must be a string")

        self._host = host

        if not isinstance(port, int):
            raise TypeError("port must be a non-negative integer")

        if port < 0:
            raise TypeError("port must be a non-negative integer")

        self._port = port

        if not isinstance(db, int):
            raise TypeError("db must be a non-negative integer")

        if db < 0:
            raise TypeError("db must be a non-negative integer")

        self._db = db

    @property
    def host(self):
        """
        :return: the host of the redis instance
        :rtype: string
        """
        return self._host

    @property
    def port(self):
        """
        :return: the port of the redis instance
        :rtype: integer
        """
        return self._port

    @property
    def db(self):
        """
        :return: the db of the redis instance
        :rtype: integer
        """
        return self._db

    def client_from_config(self, sid):
        from vishnu.backend.client.redis.redis_py import Client
        return Client(sid, self._host, self._port, self._db)
