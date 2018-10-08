import unittest


class GoogleAppEngineNDBConfig(unittest.TestCase):

    def test_shortcut_import(self):
        from vishnu.backend import GoogleAppEngineNDB
        from vishnu.backend.config.google_app_engine_ndb import Config

        shortcut_instance = GoogleAppEngineNDB()
        instance = Config()

        self.assertEqual(type(shortcut_instance), type(instance))

    @unittest.skip
    def test_client_from_config(self):
        from vishnu.backend.config.google_app_engine_ndb import Config
        from vishnu.backend.client.google_app_engine_ndb import Client

        client = Config().client_from_config("sid")
        self.assertEqual(type(client), Client)
