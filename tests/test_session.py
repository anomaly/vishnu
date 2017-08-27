import pytest

SECRET = "pFaN6k68lhFkOtNMsc1HfcKvE9GoAJ7Y"
ENCRYPT_KEY = "JBW8bCCKxE2XZ23wUgLJ6T6zFqvPEx1J"


def test_sid_encoding_unencrypted():
    from vishnu.session import Session

    sid = Session.generate_sid()

    encoded_sid = Session.encode_sid(SECRET, sid)
    decoded_sid = Session.decode_sid(SECRET, encoded_sid)

    assert sid == decoded_sid


def test_sid_encoding_encrypted():
    from vishnu.session import Session

    sid = Session.generate_sid()

    encoded_sid = Session.encode_sid(SECRET, sid)
    decoded_sid = Session.decode_sid(SECRET, encoded_sid)

    assert sid == decoded_sid
