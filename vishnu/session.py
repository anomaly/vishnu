from google.appengine.ext import ndb

class SavedSession(ndb.Model):
	expires = ndb.DateTimeProperty(required=False)

class Session(object):

	def __init__(self, sid=None, secure=False, timeout=None):
		self._data = dict()
		self._secure = secure
		self._timeout = timeout

	def headers(self):
		headers = list()

		header = "key=value;"
		if self._secure:
			header += " Secure; HttpOnly"

		if header:
			headers.append(header)

		#no timeout means this cookie is session only

		return headers

	def start(self):
		pass

	def end(self):
		pass

	def get(self, key):
		return self._data.get(key)