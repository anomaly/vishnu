"""
Vishnu: A session library for the python runtime of Google App Engine.
"""
from __future__ import absolute_import

import threading

_thread_local = threading.local() # pylint: disable=C0103
_thread_local.session = None

from vishnu.session import Session

def get_session():
    """Returns the session for the current request"""
    return _thread_local.session
