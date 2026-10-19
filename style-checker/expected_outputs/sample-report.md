# Google Style Check Report

## Summary
- Files scanned: 6
- Languages: Go, Python, TypeScript
- Total violations: 9 (Critical: 1, High: 3, Medium: 3, Low: 2)

## Critical

### Go
- `internal/parser/parse.go:14` — **Rule**: Constants must use `MixedCaps`, not `UPPER_SNAKE_CASE`. Found `MAX_BUFFER_SIZE`, expected `MaxBufferSize`

## High

### Go
- `internal/parser/parse.go:42` — **Rule**: Receiver name must not be `self`. Found `func (self *Parser)`, expected `func (p *Parser)`

### Python
- `src/models/user.py:18` — **Rule**: Class names must use `CapWords`. Found `class user_model`, expected `class UserModel`
- `src/models/user.py:31` — **Rule**: Constants must use `CAPS_WITH_UNDER`. Found `default_timeout = 30` at module scope, expected `DEFAULT_TIMEOUT = 30`

## Medium

### Go
- `cmd/main.go:7` — **Rule**: A renamed import's local name follows package naming (lowercase, no underscores). Found `my_pkg "github.com/org/mypkg/v2"`, expected `mypkg`
- `internal/parser/parse.go:28` — **Rule**: Import group ordering. Standard library and third-party packages are not separated by a blank line

### TypeScript
- `src/services/auth.service.ts:55` — **Rule**: Use an interface, not a type alias, for object types. Found `type AuthState = {...}`, expected `interface AuthState {...}`

## Low

### Python
- `src/models/user.py:17` — **Rule**: Blank lines between top-level definitions. Expected 2 blank lines before `class user_model`, found 1
- `src/utils/helpers.py:44` — **Rule**: Inline comment spacing. Expected 2 spaces before `#`, found 1

## Clean files
- `cmd/server.go`
