# memcache
from vishnu.backend.config.memcache.gae import Config as GoogleAppEngineMemcache
from vishnu.backend.config.memcache.pylibmc import Config as Pylibmc
from vishnu.backend.config.memcache.pymemcache import Config as PyMemcache
from vishnu.backend.config.memcache.pythonmemcached import Config as PythonMemcached

# redis
from vishnu.backend.config.redis.redis_py import Config as Redis

# NDB
from vishnu.backend.config.ndb.gae import Config as GoogleAppEngineNDB
