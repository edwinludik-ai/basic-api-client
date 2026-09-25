"""OAuth2 authorization-code login (browser-based approval)."""

import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from requests_oauthlib import OAuth2Session


def authenticate(authorization_url, token_url, client_id, client_secret=None, scope=None, redirect_port=8765):
    """Log in via the OAuth2 authorization code flow.

    Opens the provider's login/approval page in a browser, catches the
    redirect on a local server, and exchanges the returned code for a token.

    Returns an authenticated `requests`-compatible session (supports
    .get/.post/etc.): it attaches the Bearer token to every request and
    refreshes it automatically once it expires, if the provider issues a
    refresh_token.

    Note: `http://localhost:<redirect_port>/callback` must be registered as
    an allowed redirect URI with your OAuth provider.
    """
    redirect_uri = f"http://localhost:{redirect_port}/callback"
    session = OAuth2Session(
        client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        auto_refresh_url=token_url,
        auto_refresh_kwargs={"client_id": client_id, "client_secret": client_secret},
    )

    auth_url, _state = session.authorization_url(authorization_url)
    webbrowser.open(auth_url)
    print(f"Opened browser for login. If it didn't open, visit:\n{auth_url}")

    authorization_response = _await_redirect(redirect_port)
    session.fetch_token(
        token_url,
        authorization_response=authorization_response,
        client_secret=client_secret,
    )
    return session


def _await_redirect(port):
    """Run a one-shot local server that captures the OAuth2 redirect URL."""
    callback = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            callback["url"] = f"http://localhost:{port}{self.path}"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Login complete.</h1>You can close this tab.")

        def log_message(self, *_args):
            pass

    HTTPServer(("localhost", port), Handler).handle_request()
    return callback["url"]
