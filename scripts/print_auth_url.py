#!/usr/bin/env python3
"""Print the OAuth2 login URL to open in a browser.

Run this to discover a provider's registered redirect URI before wiring up
authenticate(): open the printed URL yourself, log in/approve (or let it
auto-redirect), and see exactly where it lands.
"""

import argparse

from basic_api_client import build_authorization_url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("authorization_url", help="The provider's OAuth2 authorization endpoint")
    parser.add_argument("client_id", help="Your OAuth2 client ID")
    parser.add_argument("--redirect-port", type=int, default=8765, help="Default: 8765")
    parser.add_argument("--scope", nargs="*", default=None, help="One or more scope names")
    args = parser.parse_args()

    print(build_authorization_url(
        authorization_url=args.authorization_url,
        client_id=args.client_id,
        redirect_port=args.redirect_port,
        scope=args.scope,
    ))


if __name__ == "__main__":
    main()
