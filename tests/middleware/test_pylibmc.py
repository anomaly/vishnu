import unittest


class MiddlewareWithPylibmcBackend(unittest.TestCase):

    def test_manual_save(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        app = test_app(use_https=True, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_auto_save(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        app = test_app(use_https=True, auto_save=True, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/no/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_default_cookie_name(self):
        from vishnu.backend import Pylibmc
        from vishnu.session import DEFAULT_COOKIE_NAME
        from ..middleware import test_app
        app = test_app(use_https=True, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)
        self.assertTrue(DEFAULT_COOKIE_NAME in app.cookies)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_custom_cookie_name(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        custom_cookie_name = "my-cookie-name"
        app = test_app(use_https=True, cookie_name=custom_cookie_name, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)
        self.assertTrue(custom_cookie_name in app.cookies)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_encrypted(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        app = test_app(use_https=True, encrypt=True, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_unencrypted(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        app = test_app(use_https=True, encrypt=False, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_insecure_http(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        app = test_app(use_https=False, secure=False, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_secure_https(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        app = test_app(use_https=True, secure=True, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private after login
        private_resp = app.get('/private')
        self.assertEqual(private_resp.status_int, 200)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)

    def test_secure_http(self):
        from vishnu.backend import Pylibmc
        from ..middleware import test_app
        app = test_app(use_https=False, secure=True, backend=Pylibmc())

        # check public before login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private before login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # start session (manual save)
        login_resp = app.post("/login/save")
        self.assertEqual(login_resp.status_int, 200)

        # check public after login
        public_resp = app.get('/public')
        self.assertEqual(public_resp.status_int, 200)

        # check private after login
        private_resp = app.get('/private', status=401)
        self.assertEqual(private_resp.status_int, 401)

        # end session
        logout_resp = app.get("/logout")
        self.assertEqual(logout_resp.status_int, 200)

        # check public after logout
        public_resp = app.get("/public")
        self.assertEqual(public_resp.status_int, 200)

        # check private after logout
        private_resp = app.get("/private", status=401)
        self.assertEqual(private_resp.status_int, 401)
