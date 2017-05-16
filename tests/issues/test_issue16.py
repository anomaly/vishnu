"""
Terminating and starting a session within same request fails to send cookie
https://github.com/anomaly/vishnu/issues/16
"""
import pytest
import vishnu
import webapp2


class BaseHandler(webapp2.RequestHandler):

    @property
    def session(self):
        """
        :return: the current vishnu session
        :rtype: vishnu.session.Session
        """
        return vishnu.get_session()


class PrivateHandler(BaseHandler):

    def get(self):

        if self.session.get("user") == "james":
            self.response.status = 200
        else:
            self.response.status = 401


class PublicHandler(BaseHandler):

    def get(self):
        self.response.status = 200


class LoginHandler(BaseHandler):

    def post(self):

        self.session["user"] = "james"
        self.session.save()

        self.session.terminate()

        self.session["user"] = "james"
        self.session.save()

        self.response.status = 200


class LogoutHandler(BaseHandler):

    def get(self):

        self.session.terminate()

        self.response.status = 200


@pytest.fixture
def test_app(backend):
    from webtest import TestApp
    from vishnu.middleware import SessionMiddleware
    from vishnu.session import Config

    app = webapp2.WSGIApplication([
        (r'/private', PrivateHandler),
        (r'/public', PublicHandler),
        (r'/login/save', LoginHandler),
        (r'/logout', LogoutHandler)
    ], debug=True)

    config = Config(
        secret="OVc1Mbt79AK5Pmi6sWnJnXZvEPNO3BnI",
        backend=backend
    )
    session = SessionMiddleware(app, config)

    return TestApp(app=session, extra_environ={'wsgi.url_scheme': 'https'})


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
