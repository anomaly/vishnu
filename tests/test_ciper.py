# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def cipher():
    from vishnu.cipher import AESCipher
    return AESCipher(key="Qv5p0cmYqkcWl0PyOepbFweKxRY0xAiB")


def test_pad_unpad():
    from vishnu.cipher import AESCipher
    from Crypto.Cipher import AES

    data_to_pad = "secret_raw_data"

    padded_data = AESCipher.pad(data_to_pad)
    assert len(padded_data) % AES.block_size == 0
    unpadded_data = AESCipher.unpad(padded_data)
    assert len(data_to_pad) == len(unpadded_data)
    assert data_to_pad == unpadded_data


def test_encrypt_decrypt(cipher):
    data_to_encrypt = "secret_raw_data"

    encrypted = cipher.encrypt(data_to_encrypt)
    decrypted = cipher.decrypt(encrypted)

    assert data_to_encrypt == decrypted
