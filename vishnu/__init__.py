"""
Vishnu: A session library for the python runtime of Google App Engine.
"""
from __future__ import absolute_import

import threading

__version_info__ = (2, 0, 0)
__version__ = '.'.join(str(v) for v in __version_info__)

_thread_local = threading.local()  # pylint: disable=C0103
_thread_local.session = None


def get_session():
    """Returns the session for the current request"""
    return _thread_local.session
