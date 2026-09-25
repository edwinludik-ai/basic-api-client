# basic-api-client

A minimal Python client for logging in to an API via OAuth2 (authorization
code flow) and calling it with an authenticated `requests` session.

## Install

Dependencies are vendored into `src/_vendor/` (a pure-Python copy of
`requests`, `requests-oauthlib`, `oauthlib`, and `python-dotenv`, plus
their own dependencies), so nothing here needs `pip install` or network
access at all -- just add `src/` to your path:

```python
import sys
sys.path.insert(0, "src")

from basic_api_client import authenticate
```

If you do have network access and prefer a normal install instead
(e.g. for use in another project), `pip install -e .` works too --
`pyproject.toml` declares the same dependencies for that case.

## Usage

```python
import sys
sys.path.insert(0, "src")

from basic_api_client import authenticate

session = authenticate(
    authorization_url="https://auth.example.com/oauth2/authorize",
    token_url="https://auth.example.com/oauth2/token",
    client_id="your-client-id",
    redirect_uri="https://your-app.example.com/callback",  # must match what's registered for client_id
    client_secret=None,  # if your client has one
    scope=None,  # e.g. ["read", "write"]
)

response = session.get("https://api.example.com/some-endpoint")
```

`authenticate` opens the login URL in your browser. Since `redirect_uri`
is normally fixed to wherever your OAuth client is registered -- often
not an address this program can listen on -- login is completed by
pasting back the URL your browser lands on after approving.

The returned session is a `requests_oauthlib.OAuth2Session` (a drop-in
`requests.Session`): it attaches the bearer token to every request
automatically, and refreshes it once it expires, if the provider issues
a refresh token.

### Just building the login URL

`build_authorization_url` is the piece of `authenticate` that builds the
login URL, without opening a browser or waiting for input. Useful for
checking what a login attempt looks like, or for discovering a
provider's registered redirect URI when you don't have dashboard
access -- open the URL yourself and see where it lands:

```python
from basic_api_client import build_authorization_url

print(build_authorization_url(authorization_url, client_id, redirect_uri, scope))
```

### scripts/print_auth_url.py

A small CLI wrapper around `build_authorization_url`, reading config
from environment variables or a `.env` file:

```
cp .env.example .env
# fill in OAUTH_AUTHORIZATION_URL, OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI
python3 scripts/print_auth_url.py
```

Reads:

| Variable | Required | Description |
|---|---|---|
| `OAUTH_AUTHORIZATION_URL` | yes | The provider's OAuth2 authorization endpoint |
| `OAUTH_CLIENT_ID` | yes | Your OAuth2 client ID |
| `OAUTH_REDIRECT_URI` | yes | Your OAuth2 client's registered redirect URI |
| `OAUTH_SCOPE` | no | Space-separated scope names |

### scripts/test_api.py

Logs in via `authenticate` and makes an authenticated GET request to a
URL you give it, to check that login and the API both actually work
end to end:

```
cp .env.example .env
# fill in OAUTH_AUTHORIZATION_URL, OAUTH_TOKEN_URL, OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI
python3 scripts/test_api.py https://api.example.com/some-endpoint
```

Prints the response status and body. Reads the same variables as
`print_auth_url.py`, plus:

| Variable | Required | Description |
|---|---|---|
| `OAUTH_TOKEN_URL` | yes | The provider's OAuth2 token endpoint |
| `OAUTH_CLIENT_SECRET` | no | Your OAuth2 client secret, if it has one |

## Testing

```
python3 -m unittest discover
```

## License

BSD Zero Clause License (0BSD) -- see [LICENSE](LICENSE). No conditions
at all: use, copy, modify, and distribute for any purpose, without even
needing to retain the copyright/license notice in copies.
