package apiclient

import (
	"context"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestBuildAuthorizationURL(t *testing.T) {
	got := BuildAuthorizationURL(
		"https://provider.example.com/oauth/authorize",
		"my-client-id",
		"https://myapp.example.com/callback",
		nil,
	)

	for _, want := range []string{
		"client_id=my-client-id",
		"redirect_uri=https%3A%2F%2Fmyapp.example.com%2Fcallback",
	} {
		if !strings.Contains(got, want) {
			t.Errorf("authorization URL %q missing %q", got, want)
		}
	}
}

func TestAuthenticate(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"access_token": "abc123", "token_type": "Bearer"}`))
	}))
	defer server.Close()

	originalState, originalBrowser := randomState, openBrowser
	randomState = func() string { return "fixed-state" }
	openBrowser = func(string) error { return nil }
	defer func() { randomState, openBrowser = originalState, originalBrowser }()

	stdin := strings.NewReader("https://myapp.example.com/callback?code=fake-code&state=fixed-state\n")

	client, err := Authenticate(
		context.Background(),
		"https://provider.example.com/oauth/authorize",
		server.URL,
		"my-client-id",
		"",
		"https://myapp.example.com/callback",
		nil,
		stdin,
	)
	if err != nil {
		t.Fatalf("Authenticate returned error: %v", err)
	}
	if client == nil {
		t.Fatal("expected a non-nil http.Client")
	}
}

func TestAuthenticateRejectsStateMismatch(t *testing.T) {
	originalState, originalBrowser := randomState, openBrowser
	randomState = func() string { return "expected-state" }
	openBrowser = func(string) error { return nil }
	defer func() { randomState, openBrowser = originalState, originalBrowser }()

	stdin := strings.NewReader("https://myapp.example.com/callback?code=fake-code&state=wrong-state\n")

	_, err := Authenticate(
		context.Background(),
		"https://provider.example.com/oauth/authorize",
		"https://provider.example.com/oauth/token",
		"my-client-id",
		"",
		"https://myapp.example.com/callback",
		nil,
		stdin,
	)
	if err == nil {
		t.Fatal("expected a state mismatch error, got nil")
	}
}
