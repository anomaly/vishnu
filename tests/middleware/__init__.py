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


class LoginSaveHandler(BaseHandler):

    def on_post(self, req, resp):

        self.session["user"] = "james"
        self.session.save()

        resp.status = falcon.HTTP_200


class LoginNoSaveHandler(BaseHandler):

    def on_post(self, req, resp):

        self.session["user"] = "james"

        resp.status = falcon.HTTP_200


class LogoutHandler(BaseHandler):

    def on_get(self, req, resp):

        self.session.terminate()

        resp.status = falcon.HTTP_200


@pytest.fixture
def test_app(cookie_name=None, encrypt=False, auto_save=False,
             secure=True, domain=None, path=None,
             use_https=False, backend=None):
    from webtest import TestApp
    from vishnu.middleware import SessionMiddleware

    api = falcon.API()
    api.add_route("/private", PrivateHandler())
    api.add_route("/public", PublicHandler())
    api.add_route("/login/save", LoginSaveHandler())
    api.add_route("/login/no/save", LoginNoSaveHandler())
    api.add_route("/logout", LogoutHandler())

    encrypt_key = None
    if encrypt:
        encrypt_key = "YTWRsQIU4lYj4HyP33Uh24nrraDFv0R9"

    config = vishnu.session.Config(
        secret="OVc1Mbt79AK5Pmi6sWnJnXZvEPNO3BnI",
        cookie_name=cookie_name,
        encrypt_key=encrypt_key,
        auto_save=auto_save,
        domain=domain,
        path=path,
        secure=secure,
        http_only=True,
        backend=backend,
    )
    session = SessionMiddleware(api, config)

    extra_environ = {}
    if use_https:
        extra_environ['wsgi.url_scheme'] = 'https'

    return TestApp(app=session, extra_environ=extra_environ)
