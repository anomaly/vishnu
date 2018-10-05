import unittest


class GoogleAppEngineNDBConfig(unittest.TestCase):

    def test_shortcut_import(self):
        from vishnu.backend import GoogleAppEngineNDB
        from vishnu.backend.config.ndb.gae import Config

        shortcut_instance = GoogleAppEngineNDB()
        instance = Config()

        self.assertEquals(type(shortcut_instance), type(instance))

    @unittest.skip
    def test_client_from_config(self):
        from vishnu.backend.config.ndb.gae import Config
        from vishnu.backend.client.google_app_engine_ndb import Client

        client = Config().client_from_config("sid")
        self.assertEquals(type(client), Client)
