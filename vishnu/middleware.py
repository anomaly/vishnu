"""
WSGI Middleware.
"""
from __future__ import absolute_import

from vishnu import _thread_local
from vishnu.session import Session


class SessionMiddleware(object):  # pylint: disable=R0903
    """WSGI middleware for adding support for sessions."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        _thread_local.session = Session()

        def vishnu_start_response(status, headers, exc_info=None):
            """Our start_response wrapper so we can insert cookie header"""
            if _thread_local.session.needs_save and _thread_local.session.auto_save:
                _thread_local.session.save()
            elif _thread_local.session.needs_save and _thread_local.session.started:
                _thread_local.session.save(sync_only=True)

            header = _thread_local.session.header()
            if header:
                headers.append(("Set-Cookie", header))

            return start_response(status, headers, exc_info)

        return self.app(environ, vishnu_start_response)
