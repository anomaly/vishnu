import unittest


class PickleableSession(unittest.TestCase):

    def test_constructor_and_properties(self):
        from vishnu.backend.client import PickleableSession
        from datetime import datetime

        expires = datetime(2018, 1, 1, 0, 0, 0)
        last_accessed = (2017, 12, 30, 10, 0, 0)
        data = "data"

        ps = PickleableSession(
            expires=expires,
            last_accessed=last_accessed,
            data=data
        )
        self.assertEqual(ps.expires, expires)
        self.assertEqual(ps.last_accessed, last_accessed)
        self.assertEqual(ps.data, data)

    def test_can_pickle(self):
        pass
