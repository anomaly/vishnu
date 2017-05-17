def gae_ndb_delete_expired_sessions(dormant_for=86400, limit=500):
    """Deletes expired sessions
       A session is expired if it expires date is set and has passed or
       if it has not been accessed for a given period of time.
       max_age: seconds since last access to delete sessions, defaults
       to 24 hours.
       limit: amount to delete in one call of the method, the maximum
       and default for this is the NDB fetch limit of 500"""
    from vishnu.backend.client.ndb.gae import VishnuSession
    from google.appengine.ext import ndb
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()
    last_accessed = now - timedelta(seconds=dormant_for)

    query = VishnuSession.query(ndb.OR(
        ndb.AND(VishnuSession.expires <= now, VishnuSession.expires != None),
        VishnuSession.last_accessed <= last_accessed
    ))
    results = query.fetch(keys_only=True, limit=limit)

    ndb.delete_multi(results)

    return len(results) < limit