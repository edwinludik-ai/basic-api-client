import unittest
from unittest.mock import patch

from requests_oauthlib import OAuth2Session

from basic_api_client import authenticate, build_authorization_url


class BuildAuthorizationUrlTests(unittest.TestCase):
    def test_includes_client_id_and_redirect_uri(self):
        url = build_authorization_url(
            authorization_url="https://provider.example.com/oauth/authorize",
            client_id="my-client-id",
            redirect_uri="https://myapp.example.com/callback",
        )

        self.assertIn("client_id=my-client-id", url)
        self.assertIn("redirect_uri=https%3A%2F%2Fmyapp.example.com%2Fcallback", url)


class AuthenticateTests(unittest.TestCase):
    @patch("basic_api_client.auth.input")
    @patch("basic_api_client.auth.webbrowser.open")
    @patch.object(OAuth2Session, "fetch_token")
    def test_logs_in_with_authorization_code_flow(self, fetch_token, browser_open, mock_input):
        fetch_token.return_value = {"access_token": "abc123", "token_type": "Bearer"}
        mock_input.return_value = "https://myapp.example.com/callback?code=fake-code&state=xyz"

        session = authenticate(
            authorization_url="https://provider.example.com/oauth/authorize",
            token_url="https://provider.example.com/oauth/token",
            client_id="my-client-id",
            redirect_uri="https://myapp.example.com/callback",
        )

        self.assertIsInstance(session, OAuth2Session)
        browser_open.assert_called_once()
        fetch_token.assert_called_once_with(
            "https://provider.example.com/oauth/token",
            authorization_response="https://myapp.example.com/callback?code=fake-code&state=xyz",
            client_secret=None,
        )


if __name__ == "__main__":
    unittest.main()
