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

        # todo: check valid host
        self._host = host

        # todo: check valid port
        self._port = port

        # todo: check valid db
        self._db = db

    def client_from_config(self, sid):
        from vishnu.backend.client.redis.redis_py import Client
        return Client(sid, self._host, self._port, self._db)
