import pytest

from vishnu.session import Session
from vishnu.backend import Pylibmc


@pytest.fixture
def memcache_client(sid=None):

    if sid is None:
        sid = Session.generate_sid()

    config = Pylibmc()
    client = config.client_from_config(sid)
    return client


def test_load():
    sid = Session.generate_sid()
    client_a = memcache_client(sid)

    # try to load (not started yet)
    assert client_a.load() is False

    # save
    client_a.save()

    # try to load (should be started)
    assert client_a.load() is True

    # start new client and check already started
    client_b = memcache_client(sid)
    assert client_b.load() is True


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
    client_a = memcache_client(sid)

    assert client_a.load() is False

    client_a.save()

    assert client_a.load() is True

    # save some data to the session
    client_a["key"] = "value"
    client_a.save()

    import time
    time.sleep(1)

    # start another client and check data was loaded
    client_b = memcache_client(sid)

    assert client_b.load() is True
    assert client_b.get("key") == "value"
