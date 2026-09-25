#!/usr/bin/env python3
"""Print the OAuth2 login URL to open in a browser.

Run this to check what a login attempt looks like before wiring up
authenticate(): open the printed URL yourself, log in/approve, and see
exactly where it lands.

Reads config from environment variables:
    OAUTH_AUTHORIZATION_URL  (required) the provider's OAuth2 authorization endpoint
    OAUTH_CLIENT_ID          (required) your OAuth2 client ID
    OAUTH_REDIRECT_URI       (required) your OAuth2 client's registered redirect URI
    OAUTH_SCOPE              (optional) space-separated scope names
"""

import os

from dotenv import load_dotenv

from basic_api_client import build_authorization_url

load_dotenv()

scope = os.environ.get("OAUTH_SCOPE")

print(build_authorization_url(
    authorization_url=os.environ["OAUTH_AUTHORIZATION_URL"],
    client_id=os.environ["OAUTH_CLIENT_ID"],
    redirect_uri=os.environ["OAUTH_REDIRECT_URI"],
    scope=scope.split() if scope else None,
))
