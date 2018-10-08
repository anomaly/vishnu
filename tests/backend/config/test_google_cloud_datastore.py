import unittest


class GoogleCloudDatastoreConfig(unittest.TestCase):

    def test_import_shortcut(self):
        from vishnu.backend import GoogleCloudDatastore
        from vishnu.backend.config.google_cloud_datastore import Config

        shortcut_instance = GoogleCloudDatastore()
        instance = Config()

        self.assertEqual(type(shortcut_instance), type(instance))

    def test_client_from_config(self):
        from vishnu.backend.config.google_cloud_datastore import Config
        from vishnu.backend.client.google_cloud_datastore import Client

        client = Config().client_from_config("sid")
        self.assertEqual(type(client), Client)
