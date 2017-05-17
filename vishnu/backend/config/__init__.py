import abc

DEFAULT_REDIS_HOST = "localhost"
DEFAULT_REDIS_PORT = 6379


class Base(object):

    @abc.abstractmethod
    def client_from_config(self, sid):
        raise NotImplementedError
