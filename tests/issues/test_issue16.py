"""
Terminating and starting a session within same request fails to send cookie
https://github.com/anomaly/vishnu/issues/16
"""
import falcon
import pytest
import unittest
import vishnu


class BaseHandler(object):

    @property
    def session(self):
        """
        :return: the current vishnu session
        :rtype: vishnu.session.Session
        """
        return vishnu.get_session()


class PrivateHandler(BaseHandler):

    def on_get(self, req, resp):

        if self.session.get("user") == "james":
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class PublicHandler(BaseHandler):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200


class LoginHandler(BaseHandler):

    def on_post(self, req, resp):

        self.session["user"] = "james"
        self.session.save()

        self.session.terminate()

        self.session["user"] = "james"
        self.session.save()

        resp.status = falcon.HTTP_200


class LogoutHandler(BaseHandler):

    def on_get(self, req, resp):

        self.session.terminate()

        resp.status = falcon.HTTP_200


def test_app(backend=None):
    from webtest import TestApp
    from vishnu.backend import Pylibmc
    from vishnu.middleware import SessionMiddleware
    from vishnu.session import Config

    api = falcon.API()
    api.add_route("/private", PrivateHandler())
    api.add_route("/public", PublicHandler())
    api.add_route("/login/save", LoginHandler())
    api.add_route("/logout", LogoutHandler())

    if backend is None:
        backend = Pylibmc()

    config = Config(
        secret="OVc1Mbt79AK5Pmi6sWnJnXZvEPNO3BnI",
        backend=backend
    )
    session = SessionMiddleware(api, config)

    return TestApp(app=session, extra_environ={'wsgi.url_scheme': 'https'})


class Issue16(unittest.TestCase):

    def test_pylibmc(self):
        from vishnu.backend import Pylibmc
        app = test_app(backend=Pylibmc())

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

    def test_pymemcache(self):
        from vishnu.backend import PyMemcache
        app = test_app(backend=PyMemcache())

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

    @unittest.skip(reason="python-memcached is no longer supported")
    def test_python_memcached(self):
        from vishnu.backend import PythonMemcached
        app = test_app(backend=PythonMemcached())

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

    def test_redis(self):
        from vishnu.backend import Redis
        app = test_app(backend=Redis())

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
