import threading

TIMEOUT_SESSION = "timeout_session" #constant used for specifying this cookie should expire at the end of the session

_thread_local = threading.local()
_thread_local.session = None

from vishnu.session import Session

def get_session():
    """Returns the session for the current request"""
    return _thread_local.session