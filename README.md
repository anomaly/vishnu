# vishnu
Sessions for the Google App Engine python runtime

## Configuration
Vishnu will automatically look for and use the following variables from your `app.yaml` config.

| name | required | default |
| ---- | -------- | ------- |
| `VISHNU_SECRET` | yes | `None` |
| `VISHNU_DOMAIN` | no | omitted |
| `VISHNU_PATH` | no | `/` |
| `VISHNU_SECURE` | no | true |
| `VISHNU_HTTP_ONLY` | no | true |
| `VISHNU_AUTO_SAVE` | no | false |
