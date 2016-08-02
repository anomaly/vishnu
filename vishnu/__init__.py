import threading

_thread_local = threading.local()

from vishnu.session import Session

def get_session():
    """Returns the session for the current request"""
    return _thread_local.session