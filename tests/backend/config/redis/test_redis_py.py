import pytest


def test_default():
    from vishnu.backend import Redis
    from vishnu.backend.config.redis import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_DB

    config = Redis()
    assert config.host == DEFAULT_HOST
    assert config.port == DEFAULT_PORT
    assert config.db == DEFAULT_DB


def test_custom_host():
    from vishnu.backend import Redis
    from vishnu.backend.config.redis import DEFAULT_PORT, DEFAULT_DB

    custom_host = "memcache.cloud"
    config = Redis(host=custom_host)
    assert config.host == custom_host
    assert config.port == DEFAULT_PORT
    assert config.db == DEFAULT_DB


def test_invalid_host():
    from vishnu.backend import Redis

    with pytest.raises(TypeError) as exp:
        Redis(host=23)


def test_custom_port():
    from vishnu.backend import Redis
    from vishnu.backend.config.redis import DEFAULT_HOST, DEFAULT_DB

    custom_port = 6380
    config = Redis(port=custom_port)
    assert config.host == DEFAULT_HOST
    assert config.port == custom_port
    assert config.db == DEFAULT_DB


def test_invalid_port():
    from vishnu.backend import Redis

    with pytest.raises(TypeError) as exp:
        Redis(port="string")

    with pytest.raises(TypeError) as exp:
        Redis(port=-100)


def test_invalid_db():
    from vishnu.backend import Redis

    with pytest.raises(TypeError) as exp:
        Redis(db=-1)

    with pytest.raises(TypeError) as exp:
        Redis(db="db")


def test_custom_db():
    from vishnu.backend import Redis

    custom_db = 1
    config = Redis(db=custom_db)
    assert config.db == custom_db
