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


class LoginSaveHandler(BaseHandler):

    def post(self):

        self.session["user"] = "james"
        self.session.save()

        self.response.status = 200


class LoginNoSaveHandler(BaseHandler):

    def post(self):

        self.session["user"] = "james"

        self.response.status = 200


class LogoutHandler(BaseHandler):

    def get(self):

        self.session.terminate()

        self.response.status = 200


@pytest.fixture
def test_app(cookie_name=None, encrypt=False, auto_save=False,
             secure=True, domain=None, path=None,
             use_https=False, backend=None):
    from webtest import TestApp
    from vishnu.middleware import SessionMiddleware

    app = webapp2.WSGIApplication([
        (r'/private', PrivateHandler),
        (r'/public', PublicHandler),
        (r'/login/save', LoginSaveHandler),
        (r'/login/no/save', LoginNoSaveHandler),
        (r'/logout', LogoutHandler)
    ], debug=True)

    encrypt_key = None
    if encrypt:
        encrypt_key = "YTWRsQIU4lYj4HyP33Uh24nrraDFv0R9"

    config = vishnu.session.Config(
        secret="OVc1Mbt79AK5Pmi6sWnJnXZvEPNO3BnI",
        cookie_name=cookie_name,
        encrypt_key=encrypt_key,
        auto_save=auto_save,
        secure=secure,
        backend=backend
    )
    session = SessionMiddleware(app, config)

    extra_environ = {}
    if use_https:
        extra_environ['wsgi.url_scheme'] = 'https'

    return TestApp(app=session, extra_environ=extra_environ)
