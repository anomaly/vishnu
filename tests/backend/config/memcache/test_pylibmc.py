import pytest


def test_default():
    from vishnu.backend import Pylibmc
    from vishnu.backend.config.memcache import DEFAULT_HOST, DEFAULT_PORT

    config = Pylibmc()
    assert config.host == DEFAULT_HOST
    assert config.port == DEFAULT_PORT


def test_custom_host():
    from vishnu.backend import Pylibmc
    from vishnu.backend.config.memcache import DEFAULT_PORT

    custom_host = "memcache.cloud"
    config = Pylibmc(host=custom_host)
    assert config.host == custom_host
    assert config.port == DEFAULT_PORT


def test_invalid_host():
    from vishnu.backend import Pylibmc

    with pytest.raises(TypeError) as exp:
        Pylibmc(host=23)


def test_custom_port():
    from vishnu.backend import Pylibmc
    from vishnu.backend.config.memcache import DEFAULT_HOST

    custom_port = 11212
    config = Pylibmc(port=custom_port)
    assert config.host == DEFAULT_HOST
    assert config.port == custom_port


def test_invalid_port():
    from vishnu.backend import Pylibmc

    with pytest.raises(TypeError) as exp:
        Pylibmc(port="string")

    with pytest.raises(TypeError) as exp:
        Pylibmc(port=-100)

