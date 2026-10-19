# Google C++ Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/cppguide.html

Rules that changed in recent versions of the guide are marked **(current rule)**. Older habits and older copies of the guide say otherwise; follow this file.

## Files

- Source files end in `.cc`, headers in `.h`. Files meant for textual inclusion at specific points end in `.inc`.
- File names: **all lowercase**, may include `_` or `-`. Follow the project's convention; with no local pattern, prefer `_`. Do not reuse names from `/usr/include` (`db.h`).
- Tests: `foo_test.cc` (`_unittest` and `_regtest` are deprecated).
- Every `.cc` file usually has a matching `.h` (exceptions: tests, small files with only `main()`).
- Headers are self-contained. Do not use separate `-inl.h` files.
- Every file starts with license boilerplate. New files usually have no copyright notice or author line.

### Header Guards
- Every header has a `#define` guard named `<PROJECT>_<PATH>_<FILE>_H_`, based on the full path in the source tree, with a **trailing underscore**.
- The `#endif` carries a comment with the guard name.

```cpp
// foo/src/bar/baz.h in project foo
#ifndef FOO_BAR_BAZ_H_
#define FOO_BAR_BAZ_H_
...
#endif  // FOO_BAR_BAZ_H_
```

---

## Includes

- Include what you use; do not rely on transitive includes.
- Project headers use paths from the source root, never `.` or `..`: `#include "base/logging.h"`.
- Angle brackets only when required: C and C++ standard headers, POSIX/Linux/Windows system headers, rare third-party cases.
- Order, **one blank line between non-empty groups**, alphabetical within each group:
  1. The related header (`foo.h` for `foo.cc` or `foo_test.cc`)
  2. C system headers and other `<...>` headers with `.h` (`<unistd.h>`)
  3. C++ standard library headers without extension (`<string>`)
  4. Other libraries' `.h` files
  5. Your project's `.h` files
- Conditional system-specific includes may come after the other includes.

```cpp
#include "foo/server/fooserver.h"

#include <sys/types.h>
#include <unistd.h>

#include <string>
#include <vector>

#include "base/basictypes.h"
#include "foo/server/bar.h"
#include "third_party/absl/flags/flag.h"
```

---

## Naming Conventions

A "word" is anything written in English without internal spaces.

| Identifier | Style | Example |
|-----------|-------|---------|
| Type (class, struct, alias, enum, type template parameter, concept) | `PascalCase`, no underscores | `UrlTable`, `PropertiesMap` |
| Variable, function parameter | `snake_case` | `table_name` |
| Class data member (static or not) | `snake_case_` with **trailing underscore** | `table_name_` |
| Struct data member | `snake_case`, **no** trailing underscore | `num_entries` |
| Constant (`const`/`constexpr`, fixed for the program's duration, static storage) | `k` + `PascalCase` | `kDaysInAWeek`, `kAndroid8_0_0` |
| Function | `PascalCase` | `AddTableEntry()`, `OpenFileOrDie()` |
| Accessor / mutator (optional) | `snake_case` like a variable | `count()`, `set_count(int count)` |
| Namespace | `snake_case` | `my_project` |
| Enumerator (scoped or unscoped) | `k` + `PascalCase` — **not** `MACRO_CASE` | `kOutOfMemory` |
| Macro | `UPPER_SNAKE_CASE` with a **project prefix** | `MYPROJECT_ROUND(x)` |
| Non-type template parameter | variable or constant rules | `kMaxAttempts` |

### Naming Rules
- Abbreviations are capitalized as a single word: `StartRpc()`, not `StartRPC()`; `UrlTable`, not `URLTable`.
- Do not abbreviate by deleting letters (`cstmr_id`). Avoid abbreviations unknown outside the project; one listed in Wikipedia is probably fine. `i` for a loop index and `T` for a template parameter are fine.
- Descriptiveness proportional to scope: `n` is fine in a short loop; `kNum` is too vague at class scope.
- **Underscores in constants** are allowed only where capitalization cannot separate words, such as digits: `kAndroid8_0_0`.
- The `k` prefix is **optional** for constants with automatic storage (locals): both `const int kPrefix` and `const int prefix` are fine inside a function. A local whose value differs per call (`const std::string kCombined = StrCat(...)`) must **not** use `k`.
- Constants exposed as part of an API that are meant to look like functions may be named like functions.
- Names analogous to existing C/C++ entities may follow that convention: `bigopen()`, `sparse_hash_map`, `LONGLONG_MAX`.
- Top-level namespaces are globally unique and named after the owning project. Nested namespaces avoid well-known names such as `std` and `absl`.
- Internal namespaces include the file name: `gshoe::internal_widget`, not `gshoe::internal`.

---

## Indentation & Line Length

- **2 spaces** per level. **Never tabs.**
- **80 characters** maximum.
- A line may exceed 80 characters only for: a comment that cannot be split without harming readability (a long URL or example command); a string literal that cannot easily be wrapped (URIs, embedded language, significant newlines); an `#include`; a header guard; a using-declaration.
- Non-ASCII characters are rare and always UTF-8. Avoid the `u8` prefix. Do not use `char16_t`, `char32_t`, or `wchar_t` (except for the Windows API).

---

## Namespaces

- **Namespace contents are not indented.**
- Multi-line namespaces end with a comment: `}  // namespace mynamespace`, and `}  // namespace` for an unnamed namespace.
- **No using-directives**: `using namespace foo;` is forbidden.
- No namespace aliases at namespace scope in headers, except in internal-only namespaces.
- No inline namespaces. Do not declare anything in namespace `std`.
- Single-line nested declarations (`namespace a::b {`) are preferred in new code but not required.

```cpp
namespace mynamespace {

class MyClass {
 public:
  void Foo();
};

}  // namespace mynamespace
```

---

## Classes

- Sections in order `public:`, `protected:`, `private:`, omitting empty ones.
- **Access specifiers are indented 1 space**; members are indented 2.
- A blank line before each access specifier except the first (optional in small classes). **No blank line after** an access specifier.
- The base class name stays on the same line as the class name (within 80 columns).
- Data members are private unless they are constants (test fixtures in a `.cc` file may use protected).
- Use `struct` only for passive data carriers with all-public fields and no invariants; otherwise `class`.
- Declaration order within a section: types and aliases; (structs only) data members; static constants; factory functions; constructors and assignment operators; destructor; other functions; other data members.
- Only trivial, very short methods are defined inline in the class body.

```cpp
class MyClass : public OtherClass {
 public:      // 1-space indent
  MyClass();  // 2-space indent
  explicit MyClass(int var);

  int some_var() const { return some_var_; }
  void set_some_var(int var) { some_var_ = var; }

 private:
  int some_var_;
};
```

### Constructor Initializer Lists
- All on one line, or break **before the colon** with a 4-space indent.
- When the list spans several lines, one member per line, aligned.

```cpp
MyClass::MyClass(int var)
    : some_var_(var),             // 4-space indent
      some_other_var_(var + 1) {  // lined up
  DoSomething();
}
```

---

## Functions

- Return type on the same line as the name; parameters too if they fit.
- Wrapped parameters align with the first parameter, or start on the next line with a **4-space** indent.
- If the return type and name do not fit on one line, break between them without indenting.
- `(` always on the same line as the name; no space between the name and `(`; no space inside the parentheses.
- `{` at the end of the last line of the declaration, with a space before it. `}` on its own line, or on the same line as `{`.
- Unused parameters: omit the name only when obvious from context; otherwise comment it out: `void Circle::Rotate(double /*radians*/) {}`.
- Attributes go before the return type: `[[nodiscard]] bool IsOk();`.

### Function Calls and Braced Lists
- All on one line; or wrap and align with the first argument; or start arguments on a new line with a 4-space indent.
- Prefer several arguments per line over one per line, unless an argument needs its own line for readability.
- A braced initializer list is formatted exactly like a function call in its place.

### Lambdas
- Format like any function. No space between `&` and the name in by-reference captures: `[&x]`.

---

## Control Flow

- Single spaces between parts: `if (condition) {`, `} else {`, `for (int i = 0; i < 10; ++i) {`.
- No space just inside the parentheses of a condition (spaces there are allowed but rare; be consistent).
- A space after each `;` in a `for` header. Range `for` has spaces around `:`.
- Controlled statements go in braces, with a line break after `{` and before `}`.
- Allowed but **discouraged**: omitting braces when the whole statement fits on one line (`if (x == kFoo) return new Foo();`), or the condition fits on one line and the body on the next. Never for `if ... else` or `do ... while`.
- Empty loop bodies: `{}` or `continue;`, **never a bare `;`** (`while (condition);` is wrong).
- `switch` on a non-enum value has a `default` case. Fall-through between non-empty cases is marked with `[[fallthrough]];`. Case braces, if used, follow the 2-space / 4-space layout:

```cpp
switch (var) {
  case 0: {  // 2-space indent
    Foo();   // 4-space indent
    break;
  }
  default: {
    Bar();
  }
}
```

---

## Expressions and Types

- **Pointer and reference declarations: no space before `*` or `&`; one space between the type and the name (current rule).** `char* c;`, `const std::string& str;`. `int *x;`, `char * c;`, and `const std::string & str;` are all wrong.
- Multiple declarators in one declaration are allowed, but **never** with `*` or `&` (`int x, *y;` is disallowed).
- No spaces around `.` or `->`; no space after unary `*` or `&`: `x = *p;`, `p = &x;`.
- Long boolean expressions: break consistently, operators usually at the end of the line.
- Use punctuation operators (`&&`, `||`, `!`, `~`), **never word operators** (`and`, `or`, `not`, `compl`).
- **Do not wrap a return value in needless parentheses**: `return result;`, not `return (result);` or `return(result);`.
- Initialization with `=`, `()`, or `{}` is all fine.
- **Floating-point literals have digits on both sides of the point**, even with an exponent: `1.0f`, `0.5L`, `1248.0e6`. Wrong: `1.f`, `.5L`, `1248e6`. An integer literal may initialize a float variable.
- Use `nullptr` for pointers and `'\0'` for chars, never `NULL` or `0`.
- Prefix `++i` / `--i` unless the postfix result is needed.
- `const` before the type (`const int*`) is encouraged but not required; be consistent.

### Integer Types
- Of the built-in integer types, use only `int`. Use `int64_t`, `int32_t`, etc. instead of `short`, `long`, `long long`.
- **Omit the `std::` prefix on these types (current rule)**: `int64_t`, not `std::int64_t`. Report as Low.
- Do not use unsigned types just to say a value is never negative.

---

## Preprocessor

- `#` always at the beginning of the line, even inside indented code. Spaces after `#` for nested directives are optional.
- Avoid macros. If needed, `UPPER_SNAKE_CASE` with a project prefix.

---

## Whitespace

- **No trailing whitespace.**
- Two spaces before an end-of-line comment.
- A space before an opening `{`. Spaces inside braced-init-lists are optional but symmetric (`{0}` or `{ 0 }`).
- Spaces around `:` in inheritance and initializer lists.
- Assignment operators always have spaces around them. Other binary operators usually do; removing spaces around factors is allowed (`v = w*x + y/z;`).
- No space inside `<` `>`, before `<`, or between `>(` in a cast: `static_cast<char*>(x)`.
- No space before the `:` of a `case`; a space after it when code follows on the same line.
- Use vertical whitespace sparingly. **No blank line at the start or end of a block.**

---

## Comments

- `//` or `/* */`, consistently; `//` is far more common.
- Comments read like prose: capitalized and punctuated. End-of-line comments may be less formal.
- File comment: needed when a file declares several abstractions, or for a `.cc` file without a header.
- Every non-obvious class or struct has a comment describing what it is for and how to use it.
- Almost every function declaration has a comment, written with an implied subject: **"Opens the file."**, not "Open the file.". Omit it only for simple, obvious functions such as accessors. Private methods are not exempt.
- Overrides document only what differs; often no comment is needed.
- Global variables have a comment saying what they are and why they are global.
- Do not state the obvious; explain why, not what.
- Non-obvious arguments: prefer named constants, enums instead of `bool`, or option structs. As a last resort: `CalculateProduct(values, options, /*completion_callback=*/nullptr)`.
- `TODO` format: `TODO` in capitals, then the bug ID, name, e-mail, or other identifier in parentheses, then a colon:

```cpp
// TODO(bug 12345): Remove the "Last visitors" feature.
// TODO(kl@gmail.com): Use a "*" here for concatenation operator.
// TODO(example.com/my-design-doc): Fix up this code next time it's touched.
```

A `// TODO: text` with no identifier is wrong.

---

## Other Rules Worth Reporting

- Mark single-argument constructors and conversion operators `explicit` (not copy, move, or `std::initializer_list` constructors).
- Every class's public interface makes clear whether it is copyable, move-only, or neither, by declaring or deleting the copy and move operations.
- Mark overrides with exactly one of `override` or `final`; do not repeat `virtual`. All inheritance is public.
- No C-style casts. Use brace conversion for arithmetic types (`int64_t{x}`), function-style casts for class types, then `static_cast` and friends.
- Google code does not use C++ exceptions. Avoid RTTI (`dynamic_cast`, `typeid`) outside unit tests.
- Do not use `<ratio>`, `<cfenv>` / `<fenv.h>`, or `<filesystem>`.
