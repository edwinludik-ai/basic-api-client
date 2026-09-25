// Command testapi logs in via OAuth2 and makes an authenticated GET request,
// to check that login and the API both actually work end to end.
//
// Usage:
//
//	go run ./cmd/testapi https://api.example.com/some-endpoint
//
// Reads config from environment variables (or a .env file):
//
//	OAUTH_AUTHORIZATION_URL  (required) the provider's OAuth2 authorization endpoint
//	OAUTH_TOKEN_URL          (required) the provider's OAuth2 token endpoint
//	OAUTH_CLIENT_ID          (required) your OAuth2 client ID
//	OAUTH_CLIENT_SECRET      (optional) your OAuth2 client secret, if your client has one
//	OAUTH_REDIRECT_URI       (required) your OAuth2 client's registered redirect URI
//	OAUTH_SCOPE              (optional) space-separated scope names
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	"github.com/joho/godotenv"

	"github.com/edwinludik-ai/basic-api-client/apiclient"
)

func main() {
	if len(os.Args) != 2 {
		log.Fatalf("usage: %s <api-url>", os.Args[0])
	}
	apiURL := os.Args[1]

	_ = godotenv.Load() // optional; fine if there's no .env file

	authorizationURL := os.Getenv("OAUTH_AUTHORIZATION_URL")
	tokenURL := os.Getenv("OAUTH_TOKEN_URL")
	clientID := os.Getenv("OAUTH_CLIENT_ID")
	clientSecret := os.Getenv("OAUTH_CLIENT_SECRET")
	redirectURI := os.Getenv("OAUTH_REDIRECT_URI")
	if authorizationURL == "" || tokenURL == "" || clientID == "" || redirectURI == "" {
		log.Fatal("OAUTH_AUTHORIZATION_URL, OAUTH_TOKEN_URL, OAUTH_CLIENT_ID and OAUTH_REDIRECT_URI must be set")
	}

	var scopes []string
	if scope := os.Getenv("OAUTH_SCOPE"); scope != "" {
		scopes = strings.Fields(scope)
	}

	client, err := apiclient.Authenticate(context.Background(), authorizationURL, tokenURL, clientID, clientSecret, redirectURI, scopes, os.Stdin)
	if err != nil {
		log.Fatalf("authenticating: %v", err)
	}

	resp, err := client.Get(apiURL)
	if err != nil {
		log.Fatalf("calling %s: %v", apiURL, err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("reading response body: %v", err)
	}

	fmt.Println(resp.Status)
	fmt.Println(string(body))
}
