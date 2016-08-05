"""
Vishnu: A session library for the python runtime of Google App Engine.
"""
from __future__ import absolute_import

import threading

_thread_local = threading.local() # pylint: disable=C0103
_thread_local.session = None

def get_session():
    """Returns the session for the current request"""
    return _thread_local.session

def delete_expired_sessions(limit=500):
    """Deletes expired sessions
       A session is expired if it expires date is set and has passed or
       if it has not been accessed for a given period of time."""
    from .session import VishnuSession
    from google.appengine.ext import ndb
    from datetime import datetime

    now = datetime.now()

    query = VishnuSession.query(ndb.AND(VishnuSession.expires <= now, VishnuSession.expires!=None))
    results = query.fetch(keys_only=True, limit=limit)

    ndb.delete_multi(results)

    return len(results) < limit
