// Command printauthurl prints the OAuth2 login URL to open in a browser.
//
// Run this to check what a login attempt looks like before wiring up
// Authenticate(): open the printed URL yourself, log in/approve, and see
// exactly where it lands.
//
// Reads config from environment variables:
//
//	OAUTH_AUTHORIZATION_URL  (required) the provider's OAuth2 authorization endpoint
//	OAUTH_CLIENT_ID          (required) your OAuth2 client ID
//	OAUTH_REDIRECT_URI       (required) your OAuth2 client's registered redirect URI
//	OAUTH_SCOPE              (optional) space-separated scope names
package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/joho/godotenv"

	"github.com/edwinludik-ai/basic-api-client/apiclient"
)

func main() {
	_ = godotenv.Load() // optional; fine if there's no .env file

	authorizationURL := os.Getenv("OAUTH_AUTHORIZATION_URL")
	clientID := os.Getenv("OAUTH_CLIENT_ID")
	redirectURI := os.Getenv("OAUTH_REDIRECT_URI")
	if authorizationURL == "" || clientID == "" || redirectURI == "" {
		log.Fatal("OAUTH_AUTHORIZATION_URL, OAUTH_CLIENT_ID and OAUTH_REDIRECT_URI must be set")
	}

	var scopes []string
	if scope := os.Getenv("OAUTH_SCOPE"); scope != "" {
		scopes = strings.Fields(scope)
	}

	fmt.Println(apiclient.BuildAuthorizationURL(authorizationURL, clientID, redirectURI, scopes))
}
