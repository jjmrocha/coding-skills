# Google Go Style Guide — Formatting & Naming

Sources:
- https://google.github.io/styleguide/go/guide
- https://google.github.io/styleguide/go/decisions
- https://google.github.io/styleguide/go/best-practices

## Formatting

- All Go source must be formatted by **`gofmt`**. If `gofmt` would change a file, it is a violation. Generated code should also be formatted.
- Indentation: **tabs** (gofmt enforces this automatically).
- Line length: **No fixed maximum.** If a line feels too long, prefer refactoring over splitting. If it is already as short as practical, let it stay long. Line length is never a valid local style rule.
- Do not split a line before an indentation change (function signature, condition), and do not split a long string such as a URL.

### Indentation Confusion
- Avoid a line break that aligns the rest of the line with an indented block. If unavoidable, leave a space to separate them.
- **Function signatures stay on a single line.**
- Do not split a function call only because of line length. Breaking it is fine when it groups arguments by meaning.
- Do not break a long string literal for line length; put the arguments on following lines instead.
- **`if` conditions are not line-broken.** Extract operands into local variables. Closures and multi-line literals inside `if` must keep matching braces.
- Do not insert artificial line breaks into `for` statements; let the line be long.
- `switch` and `case` lines stay on a single line. If a case list is excessively long, indent all cases and separate them with a blank line.

---

## Naming Conventions

Go uses **MixedCaps** (camelCase) exclusively — **no underscores** in identifiers, with three explicit exceptions:
1. Package names imported only by generated code (such as `_test` packages).
2. Test/Benchmark/Example function names in `*_test.go` files.
3. Low-level libraries interfacing with the OS or cgo.

File names are not identifiers and may contain underscores.

| Identifier | Exported | Unexported | Example |
|-----------|----------|------------|---------|
| Function/method | `UpperCamelCase` | `lowerCamelCase` | `Parse`, `parseInternal` |
| Variable (locals count as unexported) | `UpperCamelCase` | `lowerCamelCase` | `Result`, `result` |
| Type | `UpperCamelCase` | `lowerCamelCase` | `RequestType`, `requestType` |
| Constant | `UpperCamelCase` | `lowerCamelCase` | `MaxSize`, `maxSize` |
| Interface | `UpperCamelCase` | `lowerCamelCase` | `Reader`, `reader` |

**Critical**: **Never** use `UPPER_SNAKE_CASE` or a `k` / `K` prefix for constants in Go. Always use MixedCaps.

```go
// Correct
const MaxRetries = 3

// Wrong — Go does NOT use SCREAMING_SNAKE_CASE or k-prefixes
const MAX_RETRIES = 3
const kMaxBufferSize = 1024
```

- Name constants by their **role**, not their value: `const Twelve = 12` is wrong. A constant with no role apart from its value should not exist.

### Package Names

- **Lowercase letters and digits only** (`k8s`, `oauth2`), no underscores or MixedCaps.
- Multi-word packages: concatenate, no separator (`tabwriter` not `tab_writer` or `tabWriter`).
- Avoid uninformative names: `util`, `utility`, `common`, `helper`, `model`, `testhelper`.
- Avoid names likely to be shadowed by common local variables (`usercount`, not `count`).
- A renamed import's local name follows the same rules; use the same local name everywhere.

```go
// Correct
package http
package strconv
package tabwriter

// Wrong
package my_pkg
package MyPkg
```

### Interfaces

- Single-method interfaces: name = method name + `-er` suffix (`Reader`, `Writer`, `Stringer`).
- Multi-method interfaces: use a noun describing the role.

### Receivers

- **Short** (usually one or two letters), an abbreviation of the type name.
- **Consistent** for every method of a type.
- **Never** `self` or `this`, never `_`. Omit the name if it is unused.

```go
// Correct
func (c *Client) Connect() error { ... }
func (ri *ResearchInfo) Load() { ... }

// Wrong
func (self *Client) Connect() error { ... }
func (client *Client) Connect() error { ... }  // too long

// Wrong — inconsistent receivers on one type
func (this *LRUCache[K, V]) Get(key K) {}
func (cache *LRUCache[K, V]) Put(key K, value V) {}
```

### Acronyms and Initialisms

- Each initialism keeps one case: `URL` or `url`, never `Url`. `ID` and `DB` are written as in English prose.
- In names with several initialisms, each initialism has one case, but they may differ: exported `XMLAPI`, unexported `xmlAPI`.
- Initialisms with a lowercase letter keep their prose form, unless the first letter must change for export; then the whole initialism takes one case.

| English | Exported | Unexported | Incorrect |
|--------|----------|------------|-----------|
| XML API | `XMLAPI` | `xmlAPI` | `XmlApi`, `XMLApi`, `xmlapi` |
| iOS | `IOS` | `iOS` | `Ios`, `IoS`, `ios` |
| gRPC | `GRPC` | `gRPC` | `Grpc`, `grpc` |
| DDoS | `DDoS` | `ddos` | `DDOS`, `Ddos`, `dDoS` |
| ID | `ID` | `id` | `Id`, `iD` |
| DB | `DB` | `db` | `Db`, `dB` |
| Txn | `Txn` | `txn` | `TXN` |

```go
// Correct
func ParseURL(rawURL string) {}
var userID int

// Wrong
func ParseUrl(rawUrl string) {}
var userId int
```

### Getters

- **No `Get` prefix** unless the concept itself uses "get" (an HTTP GET). Use the noun directly: `Counts()` not `GetCounts()`.
- Use `Compute` or `Fetch` for expensive or remote retrievals.

```go
// Wrong
func (c *LRUCache[K, V]) GetLen() int {}

// Correct
func (c *LRUCache[K, V]) Len() int {}
```

### Variable Names

- Name length proportional to scope size, inversely proportional to how often it is used.
- Single-letter names: receivers, `r` for `io.Reader` / `*http.Request`, `w` for `io.Writer` / `http.ResponseWriter`, integer loop indices (`i`) and coordinates (`x`, `y`). Short abbreviations in short loops (`for _, n := range nodes`).
- Omit the type from the name: `userCount` or `users`, not `numUsers` or `usersInt`; `users`, not `userSlice`. A type-like qualifier is fine when two forms are in scope (`ageString` and `age`, `limitRaw` and `limit`).
- Do not drop letters to save typing: `Sandbox`, not `Sbx`.
- Omit words already clear from context: in a `UserCount` method, `count` beats `userCount`; in package `sqldb`, `Connection` beats `DBConnection`; `(p *Project) Name()`, not `ProjectName()`.

### Repetition with the Package Name

- The package name is visible at every call site, so do not repeat it in exported names.
- If a package exports one type named after the package, its constructor is `New`.

| Repetitive | Better |
|-----------|--------|
| `widget.NewWidget` | `widget.New` |
| `widget.NewWidgetWithName` | `widget.NewWithName` |
| `db.LoadFromDatabase` | `db.Load` |

### Comparison Style

- Variable on **left**, constant on **right**: `if result == "foo"`.
- **Yoda style** (`if "foo" == result`) is wrong.

### `any` Type

- Prefer `any` over `interface{}` in new code (Go 1.18+).

### Type Aliases

- Use a type definition (`type T1 T2`) for a new type. Use an alias (`type T1 = T2`) only when needed, mainly for package migrations.

### Nil Slices

- For an empty local slice, prefer `var s []int` over `s := []int{}`.
- Do not design APIs that distinguish a nil slice from an empty one. Check emptiness with `len(s) == 0`.

### Named Result Parameters

- Name results when returning several values of the same type, or to suggest a caller action (`cancel func()`).
- Do not name results when the name repeats the type: `(node *Node)` is wrong.
- Do not name results just to skip declaring a local variable or to enable naked `return`. Naked returns only in small functions.
- Naming a result is always fine when a deferred closure must change it.

### `%q` Verb

- Prefer `%q` over manually quoting with `"%s"` or `'%s'`.

### Error Naming

- Error variables use MixedCaps with an `Err` prefix: exported `ErrNotFound`, unexported `errInternal`.
- Error strings: **lowercase** (unless they begin with an exported name, a proper noun, or an acronym), **no trailing punctuation**.
- Full log or UI messages are typically capitalized: `log.Errorf("Operation aborted: %v", err)`.

```go
// Wrong
errors.New("Invalid capacity.")

// Correct
errors.New("invalid capacity")
fmt.Errorf("NewLRUCache: capacity must be > 0, got %d", capacity)
```

### Error Handling Style

- `error` is the last result. Exported functions return the `error` interface, not a concrete error type.
- Do not discard errors with `_` without a comment explaining why it is safe.
- Prefer an extra `ok bool` or `error` result over in-band error values like `-1` or `""`.
- Comparing with a sentinel error using `==` is fine. Use `errors.Is` / `errors.As` when the error may be wrapped. Never inspect the error's string.

---

## Comments (godoc)

- All **exported** top-level names must have a doc comment. Unexported types and functions with unobvious behavior should have one too.
- Doc comments are **full sentences** that begin with the name, optionally preceded by an article: `// Encode writes...`, `// A Request represents...`.
- Other complete-sentence comments are capitalized and punctuated. End-of-line comments on struct fields may be fragments.
- **No fixed comment line length.** Wrap long comments; 80 or 100 columns are common choices. Be consistent within a file. A long URL may stay on its own line. Do not put a long paragraph on one line.
- Package comment: immediately above the `package` clause, **no blank line between**. Exactly one per package. `// Package name provides ...`. For `main`, use the binary name (`// The seed_generator command ...`).

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
2. Other (project and vendored) packages
3. Protocol Buffer imports
4. Side-effect imports (`import _`)

- **No dot imports** (`import .`).
- Blank imports (`import _`) only in `main` packages or tests. Exceptions: `embed` with `//go:embed`, and bypassing the nogo disallowed-import check.
- Do not rename imports without need. Rename on a collision (rename the most local import), for generated proto packages (remove underscores, add a `pb` suffix), or for uninformative names (`v1`). To free a common variable name, use a `pkg` suffix (`urlpkg`).

```go
import (
	"fmt"
	"os"

	"github.com/myorg/myproject/pkg/foo"

	foopb "github.com/myorg/myproject/proto/foo_go_proto"

	_ "github.com/myorg/myproject/pkg/init"
)
```

---

## Literals

- Struct literals for types from **other packages** must specify field names. For local types field names are optional but recommended for large structs.
- **Matching braces**: the closing brace sits at the same indentation as the opening line. In a multi-line literal the last line ends with a comma and `}` goes on the next line.
- Cuddled braces (`[]*T{{` ... `}, {` ... `}}`) only when indentation matches and the inner values are literals.
- Omit repeated type names in slice and map literals (`gofmt -s`): `[]*Type{{A: 42}}`, not `[]*Type{&Type{A: 42}}`.
- Zero-value fields may be omitted when clarity is not lost.

```go
// Correct — field names specified, trailing comma
cfg := &pkg.Config{
	Host: "localhost",
	Port: 8080,
}

// Wrong — no field names for another package's type
cfg := &pkg.Config{"localhost", 8080}

// Wrong — closing brace on the same line as the last value
bad := []*Type{
	{Key: "multi"},
	{Key: "line"}}
```

---

## Blank Lines

- `gofmt` manages blank lines between declarations.
- Blank lines within a function body are used for logical grouping (not enforced mechanically).

---

## Error-Flow Indentation

- **Handle errors before proceeding** — do not put the normal path in an `else`. This applies to any block ending in `return`, `panic`, or `log.Fatal`.
- If a variable is used for more than a few lines, declare it outside the `if` instead of using the `if x, err := f(); ... else` form.

```go
// Correct — happy path is not indented
f, err := os.Open(name)
if err != nil {
	return err
}
return f.Chdir()

// Wrong — happy path inside else
f, err := os.Open(name)
if err == nil {
	return f.Chdir()
} else {
	return err
}
```

---

## Switch

- **No `break` at the end of a `switch` clause** — Go cases do not fall through. Use a comment to explain an empty clause. Use a labeled `break` to exit an enclosing `for`.
