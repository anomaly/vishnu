import unittest


class BaseConfig(unittest.TestCase):

    def test_client_from_config_raises_not_implemented_error(self):
        from vishnu.backend.config import Base
        config = Base()

        self.assertRaises(NotImplementedError, config.client_from_config, "sid")
