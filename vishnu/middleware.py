import threading

from vishnu import _thread_local
from vishnu.session import Session

class SessionMiddleware(object):
    """WSGI middleware for adding support for sessions."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        _thread_local.session = Session()

        def vishnu_start_response(status, headers, exc_info=None):
 
            for header in _thread_local.session.headers():
                headers.append(("Set-Cookie", header))

            return start_response(status, headers, exc_info)

        return self.app(environ, vishnu_start_response)
