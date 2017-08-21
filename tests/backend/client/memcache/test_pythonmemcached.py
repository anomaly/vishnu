import pytest

from vishnu.session import Session
from vishnu.backend import PythonMemcached

@pytest.fixture
def memcache_client(sid=None):

    if sid is None:
        sid = Session.generate_sid()

    config = PythonMemcached()
    client = config.client_from_config(sid)
    return client


def test_load():
    sid = Session.generate_sid()
    clientA = memcache_client(sid)

    # try to load (not started yet)
    assert clientA.load() is False

    # save
    clientA.save()

    # try to load (should be started)
    assert clientA.load() is True

    # start new client and check already started
    clientB = memcache_client(sid)
    assert clientB.load() is True


def test_clear():
    client = memcache_client()

    # save the session to start it
    client.save()

    # try to load (should be started)
    assert client.load() is True

    # clear
    client.clear()

    # try to load (not started yet)
    assert client.load() is False


def test_save():
    sid = Session.generate_sid()
    clientA = memcache_client(sid)

    assert clientA.load() is False

    clientA.save()

    assert clientA.load() is True

    # save some data to the session
    clientA["key"] = "value"
    clientA.save()

    # start another client and check data was loaded
    clientB = memcache_client(sid)

    assert clientB.load() is True
    assert clientB.get("key") == "value"
