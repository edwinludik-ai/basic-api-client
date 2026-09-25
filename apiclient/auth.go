// Package apiclient implements OAuth2 authorization-code login for talking to an API.
package apiclient

import (
	"bufio"
	"context"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"

	"github.com/pkg/browser"
	"golang.org/x/oauth2"
)

// randomState and openBrowser are declared as vars so tests can override them.
var (
	randomState = func() string {
		b := make([]byte, 16)
		if _, err := rand.Read(b); err != nil {
			panic(err) // crypto/rand failing means the system RNG is broken
		}
		return base64.RawURLEncoding.EncodeToString(b)
	}
	openBrowser = browser.OpenURL
)

// BuildAuthorizationURL builds the URL a user visits to log in and approve access.
//
// Useful to run on its own: open the URL in a browser, approve, and see
// where the provider actually redirects to afterward. That reveals its
// registered redirect URI, even without dashboard access.
func BuildAuthorizationURL(authorizationURL, clientID, redirectURI string, scopes []string) string {
	cfg := &oauth2.Config{
		ClientID:    clientID,
		RedirectURL: redirectURI,
		Scopes:      scopes,
		Endpoint:    oauth2.Endpoint{AuthURL: authorizationURL},
	}
	return cfg.AuthCodeURL(randomState())
}

// Authenticate logs in via the OAuth2 authorization code flow.
//
// It opens the provider's login/approval page in a browser. redirectURI is
// whatever's registered for your client with the provider -- often not an
// address this program can listen on -- so login is completed by pasting
// back the URL the browser lands on after approving, read from stdin.
//
// Returns an *http.Client that attaches the bearer token to every request
// and refreshes it automatically once it expires, if the provider issues a
// refresh token.
func Authenticate(ctx context.Context, authorizationURL, tokenURL, clientID, clientSecret, redirectURI string, scopes []string, stdin io.Reader) (*http.Client, error) {
	cfg := &oauth2.Config{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		RedirectURL:  redirectURI,
		Scopes:       scopes,
		Endpoint: oauth2.Endpoint{
			AuthURL:  authorizationURL,
			TokenURL: tokenURL,
		},
	}

	state := randomState()
	authURL := cfg.AuthCodeURL(state)

	_ = openBrowser(authURL) // best-effort; the printed URL is the fallback
	fmt.Printf("Opened browser for login. If it didn't open, visit:\n%s\n", authURL)
	fmt.Print("\nAfter approving, paste the full URL your browser landed on: ")

	line, err := bufio.NewReader(stdin).ReadString('\n')
	if err != nil && err != io.EOF {
		return nil, fmt.Errorf("reading redirect URL: %w", err)
	}

	redirected, err := url.Parse(strings.TrimSpace(line))
	if err != nil {
		return nil, fmt.Errorf("parsing redirect URL: %w", err)
	}

	query := redirected.Query()
	if got := query.Get("state"); got != state {
		return nil, fmt.Errorf("state mismatch: got %q, want %q", got, state)
	}
	code := query.Get("code")
	if code == "" {
		return nil, fmt.Errorf("redirect URL has no code parameter")
	}

	token, err := cfg.Exchange(ctx, code)
	if err != nil {
		return nil, fmt.Errorf("exchanging code for token: %w", err)
	}

	return cfg.Client(ctx, token), nil
}
