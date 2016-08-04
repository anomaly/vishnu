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
- HMAC
- Autosave setting which automatically saves anytime a session value is added
- Optional Encryption of cookie data
- Custom timeout per session

## Configuration

### app.yaml
Vishnu will automatically look for and use the following variables from your `app.yaml` config.

| name | required | default | description |
| ---- | -------- | ------- | ----------- |
| `VISHNU_COOKIE_NAME` | no |  `vishnu` | The name to use for the cookie. If omitted it wull default to `vishnu`. |
| `VISHNU_SECRET` | yes | N/A | secret |
| `VISHNU_DOMAIN` | no | N/A | The domain to set the cookie for. If omitted it will default to the domain the cookie was served from. |
| `VISHNU_PATH` | no | `/` | The path to set the cookie for. If omitted it will default to `/`. |
| `VISHNU_SECURE` | no | true | Only serve this cookie over SSL. |
| `VISHNU_HTTP_ONLY` | no | true | Only allows cookie access via HTTP/HTTPS. |
| `VISHNU_AUTO_SAVE` | no | false | Automatically save the session when a value is set. |
| `VISHNU_TIMEOUT` | no | N/A | How long until this cookie expires. If omitted it will last for the length of the browser session. |

### WSGI Middleware

### Setting a Custom Timeout
