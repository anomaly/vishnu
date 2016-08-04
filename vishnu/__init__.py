import threading

_thread_local = threading.local()
_thread_local.session = None

from vishnu.session import Session

def get_session():
    """Returns the session for the current request"""
    return _thread_local.session