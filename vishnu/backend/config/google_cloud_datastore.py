"""
Configuration for Google Cloud Datastore
https://cloud.google.com/datastore
"""
from vishnu.backend.config import Base


class Config(Base):
    """
    Configuration object for Google Cloud Datastore

    Should be imported using the shortcut vishnu.backend.GoogleCloudDatastore
    """

    def client_from_config(self, sid):
        from vishnu.backend.client.google_cloud_datastore import Client
        return Client(sid)
