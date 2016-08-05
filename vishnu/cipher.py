"""
Helper classes for encyption.

With a little help from
http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
"""

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto import Random
import hashlib

class AESCipher:

	def __init__(self, key):
		self._key = hashlib.sha256(key).digest()

	@classmethod
	def pad(cls, data):
		"""Pads data to match AES block size"""
		return data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)

	@classmethod
	def unpad(cls, data):
		return data[:-ord(data[len(data)-1:])]

	def encrypt(self, raw):
		"""Encrypts raw data using AES and then base64 encodes it."""
		padded = AESCipher.pad(raw)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self._key, AES.MODE_CBC, iv)
		return b64encode(iv + cipher.encrypt(padded))

	def decrypt(self, encrypted):
		"""Base64 decodes the data and then decrypts using AES."""
		decoded = b64decode(encrypted)
		iv = decoded[:AES.block_size]
		ciper = AES.new(self._key, AES.MODE_CBC, iv) 
		return AESCipher.unpad(ciper.decrypt(decoded[AES.block_size:]))
