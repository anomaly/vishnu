from ..middleware import test_app


def test_manual_save():
    from vishnu.backend import PythonMemcached
    app = test_app(use_https=True, backend=PythonMemcached())

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


def test_auto_save():
    from vishnu.backend import PythonMemcached
    app = test_app(use_https=True, auto_save=True, backend=PythonMemcached())

    # check public before login
    public_resp = app.get('/public')
    assert public_resp.status_int == 200

    # check private before login
    private_resp = app.get('/private', status=401)
    assert private_resp.status_int == 401

    # start session (manual save)
    login_resp = app.post("/login/no/save")
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


def test_default_cookie_name():
    from vishnu.backend import PythonMemcached
    from vishnu.session import DEFAULT_COOKIE_NAME
    app = test_app(use_https=True, backend=PythonMemcached())

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
    assert DEFAULT_COOKIE_NAME in app.cookies

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


def test_custom_cookie_name():
    from vishnu.backend import PythonMemcached
    custom_cookie_name = "my-cookie-name"
    app = test_app(use_https=True, cookie_name=custom_cookie_name, backend=PythonMemcached())

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
    assert custom_cookie_name in app.cookies

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


def test_encrypted():
    from vishnu.backend import PythonMemcached
    app = test_app(use_https=True, encrypt=True, backend=PythonMemcached())

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


def test_insecure_http():
    from vishnu.backend import PythonMemcached
    app = test_app(use_https=False, secure=False, backend=PythonMemcached())

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


def test_secure_https():
    from vishnu.backend import PythonMemcached
    app = test_app(use_https=True, secure=True, backend=PythonMemcached())

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


def test_secure_http():
    from vishnu.backend import PythonMemcached
    app = test_app(use_https=False, secure=True, backend=PythonMemcached())

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
    private_resp = app.get('/private', status=401)
    assert private_resp.status_int == 401

    # end session
    logout_resp = app.get("/logout")
    assert logout_resp.status_int == 200

    # check public after logout
    public_resp = app.get("/public")
    assert public_resp.status_int == 200

    # check private after logout
    private_resp = app.get("/private", status=401)
    assert private_resp.status_int == 401
