import pytest

@pytest.fixture
def session():
    # from vishnu.session import Session
    return None


def test_cookie_name(session):
    assert True