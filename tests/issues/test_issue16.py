"""
Terminating and starting a session within same request fails to send cookie
https://github.com/anomaly/vishnu/issues/16
"""
import falcon
import pytest
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


@pytest.fixture
def test_app(backend):
    from webtest import TestApp
    from vishnu.middleware import SessionMiddleware
    from vishnu.session import Config

    api = falcon.API()
    api.add_route("/private", PrivateHandler())
    api.add_route("/public", PublicHandler())
    api.add_route("/login/save", LoginHandler())
    api.add_route("/logout", LogoutHandler())

    config = Config(
        secret="OVc1Mbt79AK5Pmi6sWnJnXZvEPNO3BnI",
        backend=backend
    )
    session = SessionMiddleware(api, config)

    return TestApp(app=session, extra_environ={'wsgi.url_scheme': 'https'})


def test_pylibmc():
    from vishnu.backend import Pylibmc
    app = test_app(backend=Pylibmc())

    # check public before login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private before login
    private_resp = app.get('/private', status=401)
    assert private_resp.status_int == 401

    # start session (manual save)
    login_resp = app.post("/login/save")
    assert login_resp.status_int == 200

    # check public after login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private after login
    private_resp = app.get('/private')
    assert private_resp.status_int == 200

    # end session
    logout_resp = app.get("/logout")
    assert logout_resp.status_int == 200

    # check public after logout
    public_resp = app.get("/public")
    assert public_resp.status_int == 200

    # check private after logout
    private_resp = app.get("/private", status=401)
    assert private_resp.status_int == 401


def test_pymemcache():
    from vishnu.backend import PyMemcache
    app = test_app(backend=PyMemcache())

    # check public before login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private before login
    private_resp = app.get('/private', status=401)
    assert private_resp.status_int == 401

    # start session (manual save)
    login_resp = app.post("/login/save")
    assert login_resp.status_int == 200

    # check public after login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private after login
    private_resp = app.get('/private')
    assert private_resp.status_int == 200

    # end session
    logout_resp = app.get("/logout")
    assert logout_resp.status_int == 200

    # check public after logout
    public_resp = app.get("/public")
    assert public_resp.status_int == 200

    # check private after logout
    private_resp = app.get("/private", status=401)
    assert private_resp.status_int == 401


@pytest.mark.skip(reason="python-memcached is no longer supported")
def test_python_memcached():
    from vishnu.backend import PythonMemcached
    app = test_app(backend=PythonMemcached())

    # check public before login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private before login
    private_resp = app.get('/private', status=401)
    assert private_resp.status_int == 401

    # start session (manual save)
    login_resp = app.post("/login/save")
    assert login_resp.status_int == 200

    # check public after login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private after login
    private_resp = app.get('/private')
    assert private_resp.status_int == 200

    # end session
    logout_resp = app.get("/logout")
    assert logout_resp.status_int == 200

    # check public after logout
    public_resp = app.get("/public")
    assert public_resp.status_int == 200

    # check private after logout
    private_resp = app.get("/private", status=401)
    assert private_resp.status_int == 401


def test_redis():
    from vishnu.backend import Redis
    app = test_app(backend=Redis())

    # check public before login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private before login
    private_resp = app.get('/private', status=401)
    assert private_resp.status_int == 401

    # start session (manual save)
    login_resp = app.post("/login/save")
    assert login_resp.status_int == 200

    # check public after login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private after login
    private_resp = app.get('/private')
    assert private_resp.status_int == 200

    # end session
    logout_resp = app.get("/logout")
    assert logout_resp.status_int == 200

    # check public after logout
    public_resp = app.get("/public")
    assert public_resp.status_int == 200

    # check private after logout
    private_resp = app.get("/private", status=401)
    assert private_resp.status_int == 401
