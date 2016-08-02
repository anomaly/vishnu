import theading

thread_local_data = threading.local()

def get_session():
    """Returns the session for the current request"""
    return thread_local_data.session