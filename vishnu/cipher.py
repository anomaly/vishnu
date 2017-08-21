"""
Helper classes for encryption.

With a little help from
http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
"""
from __future__ import unicode_literals

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import sys


class AESCipher(object):
    """
    Helper class for using AES encryption.
    """

    def __init__(self, key):
        self._key = hashlib.sha256(key.encode('utf-8')).digest()

    @classmethod
    def pad(cls, data):
        """
        Pads data to match AES block size
        """
        if sys.version_info > (3, 0):
            try:
                data = data.encode("utf-8")
            except AttributeError:
                pass

            length = AES.block_size - (len(data) % AES.block_size)
            data += bytes([length]) * length
            return data
        else:
            return data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)

    @classmethod
    def unpad(cls, data):
        """
        Unpads data that has been padded
        """
        if sys.version_info > (3, 0):
            return data[:-ord(data[len(data)-1:])].decode()
        else:
            return data[:-ord(data[len(data)-1:])]

    def encrypt(self, raw):
        """
        Encrypts raw data using AES and then base64 encodes it.
        :param raw:
        :return:
        """
        padded = AESCipher.pad(raw)
        init_vec = Random.new().read(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, init_vec)
        return b64encode(init_vec + cipher.encrypt(padded))

    def decrypt(self, encrypted):
        """
        Base64 decodes the data and then decrypts using AES.
        :param encrypted:
        :return:
        """
        decoded = b64decode(encrypted)
        init_vec = decoded[:AES.block_size]
        cipher = AES.new(self._key, AES.MODE_CBC, init_vec)

        return AESCipher.unpad(cipher.decrypt(decoded[AES.block_size:]))
