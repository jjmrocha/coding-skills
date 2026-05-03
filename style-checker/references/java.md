# Google Java Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/javaguide.html

## Naming Conventions

| Identifier | Style | Example |
|-----------|-------|---------|
| Package | `lowercase`, no underscores | `com.example.mypackage` |
| Class / Interface / Enum / Annotation | `UpperCamelCase` | `MyClass`, `ImmutableList` |
| Test class | `UpperCamelCase` ending in `Test` | `MyClassTest` |
| Method | `lowerCamelCase` | `sendMessage`, `getValue` |
| JUnit test method (allowed exception) | `lowerCamelCase` with underscores between logical components | `transferMoney_deductsFromSource` |
| Constant (`static final`, deeply immutable) | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `EMPTY_ARRAY` |
| Non-constant field | `lowerCamelCase` | `computedValues` |
| Local variable | `lowerCamelCase` | `count`, `itemList` |
| Parameter | `lowerCamelCase` | `userName` |
| Type parameter | Single uppercase letter or `ClassNameT` | `E`, `T`, `RequestT` |

**Avoid**: Hungarian notation, underscores in class/method names (except JUnit tests).

**Constant definition**: A field is a constant only if it is `static`, `final`, and its content is **deeply immutable** with no detectable side effects. A `static final ArrayList` is **NOT** a constant — use `lowerCamelCase`.

### CamelCase Conversion Algorithm
1. Convert to ASCII, remove apostrophes.
2. Split on spaces and punctuation marks.
3. Lowercase everything, then uppercase first letter of each word.
4. Join into single identifier.
- Example: `"XML HTTP request"` → `XmlHttpRequest` (not `XMLHTTPRequest`)
- Example: `"supports IPv6 on iOS?"` → `SupportsIpv6OnIos`

---

## Indentation

- **+2 spaces** per block level. **Never tabs.**
- Continuation lines: minimum **+4 spaces** from the original line.
- Multiple continuation lines at the same syntactic level: same indentation.

---

## Line Length

- **100 characters** maximum.
- Exceptions: package and import statements, long URLs in Javadoc, text block contents, shell commands in comments.

### Line-Wrapping Rules
- Break at **higher syntactic levels** when possible.
- Non-assignment operators: break **before** the symbol.
- Assignment operators: break **after** the symbol.
- Method/constructor name stays attached to `(`.
- Comma stays attached to preceding token.
- Lambda arrow `->`: do not break adjacent to it, except after arrow for single unbraced expression.

---

## Braces (K&R Style)

- Opening brace on the **same line** as the statement. **No line break before `{`.**
- Closing brace on its **own line**.
- Braces are **always required** for `if`, `else`, `for`, `do`, `while` — even single-line bodies.
- Empty blocks: `{}` is fine, but **not** in multi-block statements (`if/else`, `try/catch`).

```java
// Correct
if (condition) {
  doSomething();
} else {
  doOther();
}

// Wrong — missing braces
if (condition)
  doSomething();
```

---

## Imports

- **No wildcard imports** (`import java.util.*` is forbidden).
- Static imports NOT used for static nested classes.
- Not line-wrapped (column limit does not apply to imports).
- Order (blank line between groups):
  1. Static imports (one group, sorted alphabetically)
  2. Non-static imports (one group, sorted alphabetically)
- Sort by full package path, ASCII order.

---

## Blank Lines (Vertical Whitespace)

- Exactly **one blank line** between consecutive class members (fields, constructors, methods, nested classes, static/instance initializers).
- Optional blank line between consecutive fields (for logical grouping).
- One blank line between source file sections (license, package, imports, class declaration).
- Multiple consecutive blank lines are permitted but not required.

---

## Horizontal Whitespace

**Required spaces:**
- After keywords (`if`, `for`, `catch`, `while`, `switch`) before `(`.
- Before `{` in most cases (except `@SomeAnnotation({a, b})` and `{{"foo"}}`).
- On both sides of binary and ternary operators.
- On both sides of `&` (type bounds), `|` (catch blocks), `->` (lambda), `:` (enhanced for).
- After `,`, `;`, and `)` of a cast.
- Between `//` comment delimiter and comment text.

**Prohibited spaces:**
- No space around `::` (method reference) or `.` (field/method access).
- No horizontal alignment across consecutive lines.

---

## Statements

- **One statement per line.**
- **One variable per declaration** (`int a; int b;` not `int a, b;`).
  - Exception: multiple variables allowed in `for` loop header.
- Declare local variables **close to their first use**, not at block start.
- Typically initialize variables at declaration.

---

## Modifiers Ordering

```
public protected private abstract default static final sealed non-sealed
transient volatile synchronized native strictfp
```

---

## Array Declarations

- C-style forbidden: use `String[] args` not `String args[]`.
- Array initializers may optionally be formatted as block-like constructs.

---

## Numeric Literals

- Long-valued integer literals: **uppercase `L` suffix** (never lowercase `l`).
  - `100L` not `100l` (lowercase `l` looks like digit `1`).

---

## Annotations

- Class/package/module annotations: immediately after documentation block, **one per line**.
- Method/constructor annotations: same; single parameterless annotation may share first signature line.
- Field annotations: multiple may appear on same line.

---

## Switch Statements

- Cases indented +2 from `switch`.
- Case contents indented +2 from case label.
- Fall-through in old-style (`:`): always marked with `// fall through` comment.
- All switch statements must be **exhaustive**: use `default` or cover all enum values.

---

## Comments & Javadoc

- Javadoc required for all **`public`** and **`protected`** members.
- Exception: self-explanatory simple getters (`getFoo()`), overriding supertype methods.
- Block tag order: `@param`, `@return`, `@throws`, `@deprecated`.
- Summary fragment: noun phrase or verb phrase (not "This method does…" or "Returns a…").
- Paragraphs: blank line (line with only `*`) between them; subsequent paragraphs start with `<p>`.
- `TODO` format: `// TODO: [bug-link] - Explanation`

```java
/**
 * Returns the sum of {@code a} and {@code b}.
 *
 * @param a the first value
 * @param b the second value
 * @return the sum of {@code a} and {@code b}
 * @throws IllegalArgumentException if {@code a} is negative
 */
public int add(int a, int b) {
```

---

## Programming Practices

- Always use `@Override` when legal (except when parent method is `@Deprecated`).
- Qualify static member access with **class name**, not instance: `Foo.staticMethod()`, not `foo.staticMethod()`.
- Do not override `Object.finalize`.
- Caught exceptions: log, rethrow, or explain in comment why no action is correct.
