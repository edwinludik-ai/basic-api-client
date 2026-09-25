#!/usr/bin/env python3
"""Log in via OAuth2 and make an authenticated GET request, to check that
login and the API both actually work end to end.

Usage:
    python3 scripts/test_api.py https://api.example.com/some-endpoint

Reads config from environment variables:
    OAUTH_AUTHORIZATION_URL  (required) the provider's OAuth2 authorization endpoint
    OAUTH_TOKEN_URL          (required) the provider's OAuth2 token endpoint
    OAUTH_CLIENT_ID          (required) your OAuth2 client ID
    OAUTH_CLIENT_SECRET      (optional) your OAuth2 client secret, if your client has one
    OAUTH_REDIRECT_URI       (required) your OAuth2 client's registered redirect URI
    OAUTH_SCOPE              (optional) space-separated scope names
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# basic_api_client must be imported before any vendored package (dotenv,
# requests, ...): its __init__.py is what puts src/_vendor on sys.path.
from basic_api_client import authenticate
from dotenv import load_dotenv

if len(sys.argv) != 2:
    sys.exit(f"usage: {sys.argv[0]} <api-url>")
api_url = sys.argv[1]

load_dotenv()

scope = os.environ.get("OAUTH_SCOPE")

session = authenticate(
    authorization_url=os.environ["OAUTH_AUTHORIZATION_URL"],
    token_url=os.environ["OAUTH_TOKEN_URL"],
    client_id=os.environ["OAUTH_CLIENT_ID"],
    client_secret=os.environ.get("OAUTH_CLIENT_SECRET") or None,
    redirect_uri=os.environ["OAUTH_REDIRECT_URI"],
    scope=scope.split() if scope else None,
)

response = session.get(api_url)
print(response.status_code, response.reason)
print(response.text)
