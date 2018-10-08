

def google_app_engine_ndb_delete_expired_sessions(dormant_for=86400, limit=500):
    """
    Deletes expired sessions
    A session is expired if it expires date is set and has passed or
    if it has not been accessed for a given period of time.

    :param dormant_for: seconds since last access to delete sessions, defaults to 24 hours.
    :type dormant_for: int
    :param limit: amount to delete in one call of the method, the maximum and default for this is the NDB fetch limit of 500
    :type limit: int
    """
    from vishnu.backend.client.google_app_engine_ndb import VishnuSession
    from google.appengine.ext import ndb
    from datetime import datetime
    from datetime import timedelta

    now = datetime.utcnow()
    last_accessed = now - timedelta(seconds=dormant_for)

    query = VishnuSession.query(ndb.OR(
        ndb.AND(VishnuSession.expires <= now, VishnuSession.expires != None),
        VishnuSession.last_accessed <= last_accessed
    ))
    results = query.fetch(keys_only=True, limit=limit)

    ndb.delete_multi(results)

    return len(results) < limit


def gae_ndb_delete_expired_sessions(dormant_for, limit):
    google_app_engine_ndb_delete_expired_sessions(dormant_for, limit)


def google_cloud_datastore_delete_expired_sessions(dormant_for=86400, limit=500):
    """
    Deletes expired sessions
    A session is expired if it expires date is set and has passed or
    if it has not been accessed for a given period of time.

    :param dormant_for: seconds since last access to delete sessions, defaults to 24 hours.
    :type dormant_for: int
    :param limit: amount to delete in one call of the method, the maximum and default for this is the NDB fetch limit of 500
    :type limit: int
    """
    from vishnu.backend.client.google_cloud_datastore import TABLE_NAME
    from google.cloud import datastore
    from datetime import datetime
    from datetime import timedelta

    now = datetime.utcnow()
    last_accessed = now - timedelta(seconds=dormant_for)

    client = datastore.Client()
    accessed_query = client.query(kind=TABLE_NAME)
    accessed_query.add_filter("last_accessed", "<=", last_accessed)
    accessed_results = accessed_query.fetch(limit=limit)

    expires_query = client.query(kind=TABLE_NAME)
    expires_query.add_filter("expires", "<=", now)
    expires_results = expires_query.fetch(limit=limit)

    keys = list()
    for result in accessed_results:
        keys.append(result.key)
    for result in expires_results:
        if result.key not in keys:
            keys.append(result.key)

    client.delete_multi(keys)

    return len(keys) < limit
