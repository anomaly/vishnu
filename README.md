# vishnu
Sessions for the Google App Engine python runtime

## Features

- Cookie based session for Google App Engine using the NDB datastore
- Configurable for the following cookie settings:
 - Domain
 - Path
 - Secure
 - HttpOnly
 - Expires (timeout)
- HMAC signature to verify cookie has not been tampered
- Autosave option which saves anytime a session value is modified
- Optional Encryption of cookie data using AES
- Custom timeout per session

## Configuration

### app.yaml
Vishnu will automatically look for and use the following variables from your `app.yaml` config.

| name | required | default | description |
| ---- | -------- | ------- | ----------- |
| `VISHNU_COOKIE_NAME` | no |  `vishnu` | The name to use for the cookie. If omitted it will default to `vishnu`. |
| `VISHNU_SECRET` | yes | N/A | Secret used for HMAC signature |
| `VISHNU_ENCRYPT_KEY` | no | N/A | Key used to encrypt cookie data, it omitted then value will not be encrypted. |
| `VISHNU_DOMAIN` | no | N/A | The domain to set the cookie for. If omitted it will default to the domain the cookie was served from. |
| `VISHNU_PATH` | no | `/` | The path to set the cookie for. If omitted it will default to `/`. |
| `VISHNU_SECURE` | no | true | Only send this cookie over SSL. |
| `VISHNU_HTTP_ONLY` | no | true | Only allow cookie access via HTTP/HTTPS. |
| `VISHNU_AUTO_SAVE` | no | false | Automatically save the session when a value is set. |
| `VISHNU_TIMEOUT` | no | N/A | How long until this cookie expires. If omitted it will last for the length of the browser session. |

### Dependencies

If using encryption you will need to add the following to your `app.yaml`.
```
libraries:
- name: pycrypto
  version: "2.6"
```

### WSGI Middleware

To use vishnu you must add it as a middle to your WSGI application.
```
from vishnu.middleware import SessionMiddleware
app = SessionMiddleware(app)
```

### Setting a Custom Timeout

Each session uses the default timeout specified in `app.yaml` but if you want to
have particular sessions differ to this you can do the following.
```
session = vishnu.get_session()
session.timeout = 3600
session.save()
```
The timeout is in seconds. To set the timeout to expire at the end of this session
 you can use the `vishnu.session.TIMEOUT_SESSION` constant.
```
session = vishnu.get_session()
session.timeout = vishnu.session.TIMEOUT_SESSION
session.save()
```

### Cleaning up Expired Sessions

Add the following to a cron handler.
```
```