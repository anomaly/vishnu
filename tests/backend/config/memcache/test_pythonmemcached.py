import pytest
import sys


@pytest.mark.skipif(sys.version_info > (3, 0), reason="python-memcached is not supported under python3")
def test_default():
    from vishnu.backend import PythonMemcached
    from vishnu.backend.config.memcache import DEFAULT_HOST, DEFAULT_PORT

    config = PythonMemcached()
    assert config.host == DEFAULT_HOST
    assert config.port == DEFAULT_PORT


@pytest.mark.skipif(sys.version_info > (3, 0), reason="python-memcached is not supported under python3")
def test_custom_host():
    from vishnu.backend import PythonMemcached
    from vishnu.backend.config.memcache import DEFAULT_PORT

    custom_host = "memcache.cloud"
    config = PythonMemcached(host=custom_host)
    assert config.host == custom_host
    assert config.port == DEFAULT_PORT


@pytest.mark.skipif(sys.version_info > (3, 0), reason="python-memcached is not supported under python3")
def test_invalid_host():
    from vishnu.backend import PythonMemcached

    with pytest.raises(TypeError):
        PythonMemcached(host=23)


@pytest.mark.skipif(sys.version_info > (3, 0), reason="python-memcached is not supported under python3")
def test_custom_port():
    from vishnu.backend import PythonMemcached
    from vishnu.backend.config.memcache import DEFAULT_HOST

    custom_port = 11212
    config = PythonMemcached(port=custom_port)
    assert config.host == DEFAULT_HOST
    assert config.port == custom_port


@pytest.mark.skipif(sys.version_info > (3, 0), reason="python-memcached is not supported under python3")
def test_invalid_port():
    from vishnu.backend import PythonMemcached

    with pytest.raises(TypeError):
        PythonMemcached(port="string")

    with pytest.raises(TypeError):
        PythonMemcached(port=-100)