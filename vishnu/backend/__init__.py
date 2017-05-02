import abc


class BackendType(object):
    GoogleAppEngineNDB = "gae-ndb"


class Base(object):

    def __init__(self):
        self._sid = None
        self._data = {}
        self._loaded = False

    @property
    def data(self):
        return self._data

    @abc.abstractmethod
    def load(self, sid):
        return False

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def save(self, last_accessed, expires=None, sync_only=False):
        pass