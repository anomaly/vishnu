# memcache
from config.memcache.gae import Config as GoogleAppEngineMemcache
from config.memcache.pymemcache import Config as PyMemcache
from config.memcache.pythonmemcached import Config as PythonMemcached

# redis
from config.redis.redis_py import Config as Redis

# NDB
from config.ndb.gae import Config as GoogleAppEngineNDB
