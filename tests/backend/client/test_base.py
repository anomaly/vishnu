import unittest


class BaseClient(unittest.TestCase):

    def test_init(self):
        from vishnu.backend.client import Base
        base = Base(sid="sid")
        self.assertEqual(base.expires, None)
        self.assertEqual(base.last_accessed, None)

    def test_expires(self):
        from datetime import datetime
        from vishnu.backend.client import Base
        base = Base(sid="sid")
        self.assertEqual(base.expires, None)

        expires = datetime(2018, 1, 1, 10, 0, 0)
        base.expires = expires
        self.assertEqual(base.expires, expires)

    def test_last_accessed(self):
        from datetime import datetime
        from vishnu.backend.client import Base
        base = Base(sid="sid")
        self.assertEqual(base.last_accessed, None)

        last_accessed = datetime(2018, 1, 2, 11, 0, 0)
        base.last_accessed = last_accessed
        self.assertEqual(base.last_accessed, last_accessed)

    def test_get_and_set_of_data(self):
        pass

    def test_load_raises_not_implemented_error(self):
        from vishnu.backend.client import Base
        base = Base(sid="sid")
        self.assertRaises(NotImplementedError, base.load)

    def clear(self):
        from datetime import datetime
        from vishnu.backend.client import Base

        base = Base(sid="sid")
        base.expires = datetime.now()
        base.last_accessed = datetime.now()
        base["key"] = "value"

        base.clear()
        self.assertEqual(base.expires, None)
        self.assertEqual(base.last_accessed, None)
        self.assertEqual(base["key"], None)

    def test_save_raises_not_implemented_error(self):
        from vishnu.backend.client import Base
        base = Base(sid="sid")
        self.assertRaises(NotImplementedError, base.save)

