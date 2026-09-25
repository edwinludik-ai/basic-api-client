# basic-api-client

A minimal Go client for logging in to an API via OAuth2 (authorization
code flow) and calling it with an authenticated `*http.Client`.

## Install

```
go get github.com/edwinludik-ai/basic-api-client
```

Dependencies are vendored (see `vendor/`), so `go build`, `go test`, and
`go run` all work with no network access once the repo is cloned.
Requires Go 1.26 or newer.

## Usage

```go
package main

import (
	"context"
	"os"

	"github.com/edwinludik-ai/basic-api-client/apiclient"
)

func main() {
	client, err := apiclient.Authenticate(
		context.Background(),
		"https://auth.example.com/oauth2/authorize",  // authorization_url
		"https://auth.example.com/oauth2/token",      // token_url
		"your-client-id",                             // client_id
		"",                                            // client_secret, if your client has one
		"https://your-app.example.com/callback",      // redirect_uri -- must match what's registered for client_id
		nil,                                           // scopes, e.g. []string{"read", "write"}
		os.Stdin,
	)
	if err != nil {
		panic(err)
	}

	resp, err := client.Get("https://api.example.com/some-endpoint")
	// ...
}
```

`Authenticate` opens the login URL in your browser. Since `redirect_uri`
is normally fixed to wherever your OAuth client is registered -- often
not an address this program can listen on -- login is completed by
pasting back the URL your browser lands on after approving (read from
the `io.Reader` passed in, typically `os.Stdin`).

The returned `*http.Client` attaches the bearer token to every request
automatically, and refreshes it once it expires, if the provider issues
a refresh token.

### Just building the login URL

`BuildAuthorizationURL` is the piece of `Authenticate` that builds the
login URL, without opening a browser or waiting for input. Useful for
checking what a login attempt looks like, or for discovering a
provider's registered redirect URI when you don't have dashboard
access -- open the URL yourself and see where it lands:

```go
url := apiclient.BuildAuthorizationURL(authorizationURL, clientID, redirectURI, scopes)
fmt.Println(url)
```

### cmd/printauthurl

A small CLI wrapper around `BuildAuthorizationURL`, reading config from
environment variables or a `.env` file:

```
cp .env.example .env
# fill in OAUTH_AUTHORIZATION_URL, OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI
go run ./cmd/printauthurl
```

Reads:

| Variable | Required | Description |
|---|---|---|
| `OAUTH_AUTHORIZATION_URL` | yes | The provider's OAuth2 authorization endpoint |
| `OAUTH_CLIENT_ID` | yes | Your OAuth2 client ID |
| `OAUTH_REDIRECT_URI` | yes | Your OAuth2 client's registered redirect URI |
| `OAUTH_SCOPE` | no | Space-separated scope names |

## Testing

```
go test ./...
```

## License

BSD Zero Clause License (0BSD) -- see [LICENSE](LICENSE). No conditions
at all: use, copy, modify, and distribute for any purpose, without even
needing to retain the copyright/license notice in copies.
