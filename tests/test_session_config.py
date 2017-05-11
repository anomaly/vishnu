import pytest

SECRET = "pFaN6k68lhFkOtNMsc1HfcKvE9GoAJ7Y"
ENCRYPT_KEY = "JBW8bCCKxE2XZ23wUgLJ6T6zFqvPEx1J"


def test_secret():
    from vishnu.session import Config

    # short secret
    with pytest.raises(ValueError) as exp:
        short = Config(secret="short")

    # valid secret
    valid = Config(secret=SECRET)
    assert valid.secret == SECRET


def test_cookie_name():
    from vishnu.session import Config
    from vishnu.session import DEFAULT_COOKIE_NAME

    # default
    default = Config(secret=SECRET)
    assert default.cookie_name == DEFAULT_COOKIE_NAME

    # custom
    custom_cookie_name = "custom_cookie_name"
    custom = Config(secret=SECRET, cookie_name=custom_cookie_name)
    assert custom.cookie_name == custom_cookie_name


def test_encrypt_key():
    from vishnu.session import Config

    # no encrypt key
    default = Config(secret=SECRET)

    # short encrypt key
    with pytest.raises(ValueError) as exp:
        short = Config(secret=SECRET, encrypt_key="short")

    # valid encrypt key
    valid = Config(secret=SECRET, encrypt_key=ENCRYPT_KEY)


def test_secure():
    from vishnu.session import Config

    # default
    default = Config(secret=SECRET)
    assert default.secure == True

    # custom
    custom_true = Config(secret=SECRET, secure=True)
    assert custom_true.secure == True

    custom_false = Config(secret=SECRET, secure=False)
    assert custom_false.secure == False


def test_domain():
    from vishnu.session import Config

    # default
    default = Config(secret=SECRET)
    assert default.domain is None

    # custom
    custom_domain = "www.domain.com"
    custom = Config(secret=SECRET, domain=custom_domain)
    assert custom.domain == custom_domain


def test_path():
    from vishnu.session import Config
    from vishnu.session import DEFAULT_PATH

    # default
    default = Config(secret=SECRET)
    assert default.path == DEFAULT_PATH

    # custom
    custom_path = "/custom"
    custom = Config(secret=SECRET, path=custom_path)
    assert custom.path == custom_path


def test_http_only():
    from vishnu.session import Config

    default = Config(secret=SECRET)
    assert default.http_only == True

    custom_true = Config(secret=SECRET, http_only=True)
    assert custom_true.http_only == True

    custom_false = Config(secret=SECRET, http_only=False)
    assert custom_false.http_only == False


def test_auto_save():
    from vishnu.session import Config

    default = Config(secret=SECRET)
    assert default.auto_save == False

    custom_true = Config(secret=SECRET, auto_save=True)
    assert custom_true.auto_save == True

    custom_false = Config(secret=SECRET, auto_save=False)
    assert custom_false.auto_save == False


def test_timeout():
    from vishnu.session import Config

    default = Config(secret=SECRET)
    assert default.timeout is None

    custom_timeout = 1200
    custom = Config(secret=SECRET, timeout=custom_timeout)
    assert custom.timeout == custom_timeout


def test_backend():
    from vishnu.session import Config
