#!/usr/bin/env python3
"""Print the OAuth2 login URL to open in a browser.

Run this to discover a provider's registered redirect URI before wiring up
authenticate(): open the printed URL yourself, log in/approve (or let it
auto-redirect), and see exactly where it lands.

Reads config from environment variables:
    OAUTH_AUTHORIZATION_URL  (required) the provider's OAuth2 authorization endpoint
    OAUTH_CLIENT_ID          (required) your OAuth2 client ID
    OAUTH_REDIRECT_PORT      (optional) default: 8765
    OAUTH_SCOPE              (optional) space-separated scope names
"""

import os

from basic_api_client import build_authorization_url

scope = os.environ.get("OAUTH_SCOPE")

print(build_authorization_url(
    authorization_url=os.environ["OAUTH_AUTHORIZATION_URL"],
    client_id=os.environ["OAUTH_CLIENT_ID"],
    redirect_port=int(os.environ.get("OAUTH_REDIRECT_PORT", 8765)),
    scope=scope.split() if scope else None,
))
