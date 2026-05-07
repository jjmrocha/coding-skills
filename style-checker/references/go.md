# Google Go Style Guide — Formatting & Naming

Sources:
- https://google.github.io/styleguide/go/guide
- https://google.github.io/styleguide/go/decisions

## Formatting

- All Go source must be formatted by **`gofmt`**. If `gofmt` would change a file, it is a violation.
- Indentation: **tabs** (gofmt enforces this automatically).
- Line length: **No fixed maximum.** Prefer refactoring long lines over splitting. URLs and string literals are exempt.
- Comments: commonly wrapped at 80–100 columns for readability (not enforced).

---

## Naming Conventions

Go uses **MixedCaps** (camelCase) exclusively — **no underscores** in identifiers, with three explicit exceptions:
1. Package names imported only by generated code.
2. Test/Benchmark/Example function names in `*_test.go` files.
3. Low-level libraries interfacing with the OS or cgo.

| Identifier | Exported | Unexported | Example |
|-----------|----------|------------|---------|
| Function/method | `UpperCamelCase` | `lowerCamelCase` | `Parse`, `parseInternal` |
| Variable | `UpperCamelCase` | `lowerCamelCase` | `Result`, `result` |
| Type | `UpperCamelCase` | `lowerCamelCase` | `RequestType`, `requestType` |
| Constant | `UpperCamelCase` | `lowerCamelCase` | `MaxSize`, `maxSize` |
| Interface | `UpperCamelCase` | `lowerCamelCase` | `Reader`, `reader` |

**Critical**: **Never** use `UPPER_SNAKE_CASE` for constants in Go. Always use MixedCaps.

```go
// Correct
const MaxRetries = 3

// Wrong — Go does NOT use SCREAMING_SNAKE_CASE
const MAX_RETRIES = 3
```

### Package Names

- **All lowercase**, single word, no underscores or MixedCaps.
- Multi-word packages: concatenate, no separator (`tabwriter` not `tab_writer` or `tabWriter`).
- Avoid uninformative names: `util`, `helper`, `common`, `misc`.
- Package name should match the last element of the import path.

```go
// Correct
package http
package strconv
package mypkg

// Wrong
package my_pkg
package MyPkg
```

### Interfaces

- Single-method interfaces: name = method name + `-er` suffix (`Reader`, `Writer`, `Stringer`).
- Multi-method interfaces: use a noun describing the role.

### Receivers

- **Short** (1–2 characters), abbreviation of the type name.
- **Consistent** within a type — never mix `c` and `client` for the same type.
- **Never** use `self` or `this`.

```go
// Correct
func (c *Client) Connect() error { ... }

// Wrong
func (self *Client) Connect() error { ... }
func (client *Client) Connect() error { ... }  // too long
```

**MixedCaps receiver example:**

```go
// Wrong — inconsistent receivers
func (this *LRUCache[K, V]) Get(key K) {}
func (cache *LRUCache[K, V]) Put(key K, value V) {}

// Correct — consistent 1-2 letter receivers
func (c *LRUCache[K, V]) Get(key K) {}
func (c *LRUCache[K, V]) Put(key K, value V) {}
```

### Acronyms and Initialisms

- Treat acronyms as a consistent unit — all uppercase or all lowercase:
  - `URL` → exported: `URL`, unexported: `url`
  - `HTTP` → exported: `HTTP`, unexported: `http`
  - `ID` → exported: `ID`, unexported: `id`
- **Never** use mixed-case initialisms like `Url`, `Http`, `UserId`, `HttpUrl`.

```go
// Correct
func ParseURL(rawURL string) {}
var userID int

// Wrong
func ParseUrl(rawUrl string) {}
var userId int
```

### Getters

- **No `Get` prefix** on getter methods. Use the noun directly:
  - `Counts()` not `GetCounts()`
  - `Name()` not `GetName()`
- Complex retrievals may use `Compute`, `Fetch`, `Find`.

```go
// Wrong
func (c *LRUCache[K, V]) GetLen() int {}
func (c *LRUCache[K, V]) GetCapacity() int {}

// Correct
func (c *LRUCache[K, V]) Len() int {}
func (c *LRUCache[K, V]) Cap() int {}
```

### Variable Names

- Name length proportional to scope size.
- Single-letter names acceptable in tight scopes: `i`, `j` for loops, `x`/`y` for coordinates.
- Omit type information from names when the type is clear: `userCount` not `numUsers`.
- Omit words already clear from context (avoid repetition with package name).

```go
// Wrong — type in name, over-qualified
var usersInt int
var numUsers int
for userIndex, userValue := range users {}

// Correct — concise, scope-appropriate names
var users int
for i, u := range users {}
```

### Constructor Pattern

- Use `New` or `New<Type>` for constructors.
- **Do not repeat the package name** in the constructor or type.

```go
// Correct — package is "cache"
func New() *Widget { ... }

// Wrong — redundant with package name
func NewWidget() *Widget { ... }
func NewCacheEntry() {}    // "cache.CacheEntry" is redundant
```

### Comparison Style

- Variable on **left**, constant on **right**: `if result == "foo"`.
- Avoid **Yoda style**: `if "foo" == result`.

### `any` Type

- Prefer `any` over `interface{}` in new code (Go 1.18+).

### Nil Slices

- Prefer `nil` slice initialization for local variables over empty slice literals.
- There is no functional difference; `nil` is idiomatic.

```go
// Prefer
var s []int

// Avoid
s := []int{}
```

### Named Result Parameters

- Use names when returning multiple parameters of the same type (to disambiguate).
- Use names to suggest a required caller action (e.g., `dst` suggests caller reads it).
- **Avoid** named results solely to enable naked `return` — only acceptable for small functions.
- **Avoid** names that create repetition with the function signature.

### `%q` Verb

- Prefer `%q` for printing strings in double-quotes — it handles empty strings and special characters better than manual `%s` wrapping.

### Error Naming

- Error variables follow standard MixedCaps: exported `ErrNotFound`, unexported `errInternal`.
- Error strings: **lowercase**, **no trailing punctuation**.
  - `"something bad happened"` not `"Something bad happened."`
- Sentinel error variables: prefix `Err`: `io.ErrUnexpectedEOF`.

```go
// Wrong
errors.New("Invalid capacity.")
errors.New("Key not found")    // capitalized

// Correct
errors.New("invalid capacity")
errors.New("key not found")
fmt.Errorf("NewLRUCache: capacity must be > 0, got %d", capacity)
```

**Always compare errors with `errors.Is` or `errors.As` — never `==`:**

```go
// Wrong
if err == ErrNotFound {}
if err == io.EOF {}

// Correct
if errors.Is(err, ErrNotFound) {}
if errors.Is(err, io.EOF) {}
```

---

## Comments (godoc)

- All **exported** top-level identifiers must have a doc comment.
- Doc comment starts with the **identifier name**: `// MyFunc does ...`
- Package comment: `// Package name provides ...`
- Comments are **full sentences**: capitalized, punctuated.
- `gofmt` handles indentation; wrap long comments manually at ~80–100 chars.

```go
// Package strconv implements conversions to and from string representations
// of basic data types.
package strconv

// ParseInt interprets a string s in the given base (0, 2 to 36) and bit size
// (0 to 64) and returns the corresponding value i.
func ParseInt(s string, base int, bitSize int) (i int64, err error) {
```

---

## Imports

Four groups in order, separated by blank lines:
1. Standard library packages
2. Project and vendored packages
3. Protocol Buffer imports (if any)
4. Side-effect imports (`import _`)

- **No dot imports** (`import .`).
- Blank imports (`import _`) only in `main` packages or tests.
- Generated proto packages: rename to remove underscores, add `pb` suffix.
- Use `goimports` to manage import formatting automatically.

```go
import (
    "fmt"
    "os"

    "github.com/myorg/myproject/pkg/foo"

    pb "github.com/myorg/myproject/proto/bar_pb"

    _ "github.com/myorg/myproject/pkg/init"
)
```

---

## Struct Literals

- Struct literals from other packages must **specify field names**.
- Multi-line structs: closing `}` at same indentation as opening; trailing comma on last field.

```go
// Correct — field names specified, trailing comma
cfg := &Config{
    Host: "localhost",
    Port: 8080,
}

// Wrong — no field names
cfg := &Config{"localhost", 8080}
```

---

## Blank Lines

- `gofmt` manages blank lines between declarations.
- Blank lines within a function body are used for logical grouping (not enforced mechanically).
- No blank line between a function signature and its first statement.

---

## Error-Flow Indentation

- **Handle errors before proceeding** with normal code — don't indent the happy path inside `else`.
- Checking `err != nil` first lets the reader find the normal path quickly without tracking else branches.

```go
// Correct — happy path is not indented
f, err := os.Open(name)
if err != nil {
    return err
}
return f.Chdir()

// Avoid — happy path inside else
f, err := os.Open(name)
if err == nil {
    return f.Chdir()
} else {
    return err
}
```

---

## Conditionals & Loops

- `if` statements should **not be line-broken**; extract boolean operands to separate variables when the condition is too long.
- `for` and `switch` (old-style `:` colon statements) should remain on a single line.
- Yoda conditions (`if nil == err`) are **prohibited** — place the variable on the left.
