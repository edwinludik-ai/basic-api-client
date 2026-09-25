"""OAuth2 authorization-code login (browser-based approval)."""

import webbrowser

from requests_oauthlib import OAuth2Session


def build_authorization_url(authorization_url, client_id, redirect_uri, scope=None):
    """Build the URL a user visits to log in and approve access.

    Useful to run on its own: open the URL in a browser, approve, and see
    where the provider actually redirects to afterward. That reveals its
    registered redirect URI, even without dashboard access.
    """
    session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    auth_url, _state = session.authorization_url(authorization_url)
    return auth_url


def authenticate(authorization_url, token_url, client_id, redirect_uri, client_secret=None, scope=None):
    """Log in via the OAuth2 authorization code flow.

    Opens the provider's login/approval page in a browser. redirect_uri is
    whatever's registered for your client with the provider -- often not an
    address this program can listen on -- so login is completed by pasting
    back the URL your browser lands on after approving.

    Returns an authenticated `requests`-compatible session (supports
    .get/.post/etc.): it attaches the Bearer token to every request and
    refreshes it automatically once it expires, if the provider issues a
    refresh_token.
    """
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

    authorization_response = input("\nAfter approving, paste the full URL your browser landed on: ").strip()

    session.fetch_token(
        token_url,
        authorization_response=authorization_response,
        client_secret=client_secret,
    )
    return session
