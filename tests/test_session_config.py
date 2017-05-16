import pytest

SECRET = "pFaN6k68lhFkOtNMsc1HfcKvE9GoAJ7Y"
ENCRYPT_KEY = "JBW8bCCKxE2XZ23wUgLJ6T6zFqvPEx1J"


def test_secret():
    from vishnu.session import Config
    from vishnu.backend import Redis

    # short secret
    with pytest.raises(ValueError) as exp:
        short = Config(secret="short")

    # valid secret
    valid = Config(secret=SECRET, backend=Redis())
    assert valid.secret == SECRET


def test_cookie_name():
    from vishnu.backend import Redis
    from vishnu.session import Config
    from vishnu.session import DEFAULT_COOKIE_NAME

    # default
    default = Config(secret=SECRET, backend=Redis())
    assert default.cookie_name == DEFAULT_COOKIE_NAME

    # custom
    custom_cookie_name = "custom_cookie_name"
    custom = Config(secret=SECRET, cookie_name=custom_cookie_name, backend=Redis())
    assert custom.cookie_name == custom_cookie_name


def test_encrypt_key():
    from vishnu.backend import Redis
    from vishnu.session import Config

    # no encrypt key
    default = Config(secret=SECRET, backend=Redis())

    # short encrypt key
    with pytest.raises(ValueError) as exp:
        short = Config(secret=SECRET, encrypt_key="short", backend=Redis())

    # valid encrypt key
    valid = Config(secret=SECRET, encrypt_key=ENCRYPT_KEY, backend=Redis())


def test_secure():
    from vishnu.backend import Redis
    from vishnu.session import Config

    # default
    default = Config(secret=SECRET, backend=Redis())
    assert default.secure == True

    # custom
    custom_true = Config(secret=SECRET, secure=True, backend=Redis())
    assert custom_true.secure == True

    custom_false = Config(secret=SECRET, secure=False, backend=Redis())
    assert custom_false.secure == False


def test_domain():
    from vishnu.backend import Redis
    from vishnu.session import Config

    # default
    default = Config(secret=SECRET, backend=Redis())
    assert default.domain is None

    # custom
    custom_domain = "www.domain.com"
    custom = Config(secret=SECRET, domain=custom_domain, backend=Redis())
    assert custom.domain == custom_domain


def test_path():
    from vishnu.backend import Redis
    from vishnu.session import Config
    from vishnu.session import DEFAULT_PATH

    # default
    default = Config(secret=SECRET, backend=Redis())
    assert default.path == DEFAULT_PATH

    # custom
    custom_path = "/custom"
    custom = Config(secret=SECRET, path=custom_path, backend=Redis())
    assert custom.path == custom_path


def test_http_only():
    from vishnu.backend import Redis
    from vishnu.session import Config

    default = Config(secret=SECRET, backend=Redis())
    assert default.http_only == True

    custom_true = Config(secret=SECRET, http_only=True, backend=Redis())
    assert custom_true.http_only == True

    custom_false = Config(secret=SECRET, http_only=False, backend=Redis())
    assert custom_false.http_only == False


def test_auto_save():
    from vishnu.backend import Redis
    from vishnu.session import Config

    default = Config(secret=SECRET, backend=Redis())
    assert default.auto_save == False

    custom_true = Config(secret=SECRET, auto_save=True, backend=Redis())
    assert custom_true.auto_save == True

    custom_false = Config(secret=SECRET, auto_save=False, backend=Redis())
    assert custom_false.auto_save == False


def test_timeout():
    from vishnu.backend import Redis
    from vishnu.session import Config

    default = Config(secret=SECRET, backend=Redis())
    assert default.timeout is None

    custom_timeout = 1200
    custom = Config(secret=SECRET, timeout=custom_timeout, backend=Redis())
    assert custom.timeout == custom_timeout


def test_backend():
    from vishnu.backend import GoogleAppEngineMemcache
    from vishnu.backend import GoogleAppEngineNDB
    from vishnu.backend import PyMemcache
    from vishnu.backend import PythonMemcached
    from vishnu.backend import Redis
    from vishnu.session import Config

    gae_memcache_config = Config(secret=SECRET, backend=GoogleAppEngineMemcache())

    gae_ndb_config = Config(secret=SECRET, backend=GoogleAppEngineNDB())

    pymemcache_config = Config(secret=SECRET, backend=PyMemcache())

    python_memcached_config = Config(secret=SECRET, backend=PythonMemcached())

    redis_config = Config(secret=SECRET, backend=Redis())

    with pytest.raises(TypeError) as exp:
        unknown_config = Config(secret=SECRET)
