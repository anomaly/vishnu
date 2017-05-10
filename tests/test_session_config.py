import pytest

SECRET = "pFaN6k68lhFkOtNMsc1HfcKvE9GoAJ7Y"

def test_cookie_name():
    from vishnu.session import Session
    from vishnu.session import DEFAULT_COOKIE_NAME
    import os

    os.environ["VISHNU_SECRET"] = SECRET

    # test the default cookie name
    default = Session(os.environ)
    assert default.cookie_name == DEFAULT_COOKIE_NAME

    # test a custom cookie name
    custom_cookie_name = "custom_cookie_name"
    os.environ["VISHNU_COOKIE_NAME"] = custom_cookie_name
    custom = Session(os.environ)
    assert custom.cookie_name == custom_cookie_name


def test_secret():
    from vishnu.session import Session

    # test no secret provided

    # test short secret provided

    # test secret provided
    import os
    os.environ["VISHNU_SECRET"] = SECRET

    secret_provided = Session(os.environ)

