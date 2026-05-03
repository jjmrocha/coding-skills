# Google JavaScript Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/jsguide.html

## Naming Conventions

| Identifier | Style | Example |
|-----------|-------|---------|
| Class / Interface | `UpperCamelCase` | `MyClassName`, `Readable` |
| Function / method (public) | `lowerCamelCase` | `sendMessage`, `getValue` |
| Method (private, optional) | `lowerCamelCase_` (trailing underscore) | `myPrivateHelper_` |
| Variable / parameter | `lowerCamelCase` | `myVariable` |
| Constant (module-level, deeply immutable) | `CONSTANT_CASE` | `MAX_SIZE` |
| Module-local `const` | `lowerCamelCase` (not `CONSTANT_CASE`) | `defaultTimeout` |
| Enum name | `UpperCamelCase` | `Direction` |
| Enum member | `CONSTANT_CASE` | `Direction.NORTH` |
| Package / namespace | `lowerCamelCase` | `my.exampleCode.deepSpace` |
| Template parameter | Single word or letter, all uppercase | `TYPE`, `THIS`, `T` |
| File name | Lowercase with underscores or dashes | `my-module.js`, `my_util.js` |

### Naming Principles
- Use **descriptive names**; avoid ambiguous abbreviations.
- Avoid Hungarian notation.
- Single-character names only for variables in scope ≤10 lines (e.g., loop `i`, math `x`).
- Acronyms in names: treat as whole words — `loadHttpUrl` not `loadHTTPURL`.

### Getters/Setters
- `getFoo()`, `isFoo()`, `setFoo(value)` patterns accepted.

---

## Indentation & Line Length

- **2 spaces** per level. **Never tabs.**
- **80 characters** maximum line length.
- Continuation lines: at least **+4 spaces** from original line.
- Exceptions to line limit: `goog.require`, `goog.module`, ES module `import`/`export from` statements, long URLs.

---

## Braces & Control Flow

- K&R style: opening brace on the **same line**.
- Braces **required** for all control structures, even single-line bodies.
- Exception: simple `if` with no `else` can omit braces if it fits on one line.

```javascript
// Correct
if (condition) {
  doSomething();
}

// Allowed (no else, fits on one line)
if (condition) doSomething();

// Wrong — brace required with else
if (condition)
  doSomething();
else
  doOther();
```

---

## Variable Declarations

- Use **`const`** and **`let`**. **Never `var`.**
- **One variable per declaration** (`const a = 1; const b = 2;` not `const a = 1, b = 2;`).
- Declare variables as **close to first use** as possible.

---

## Semicolons

- **Mandatory** at end of every statement. Relying on ASI (Automatic Semicolon Insertion) is forbidden.

---

## Strings

- Ordinary string literals: **single quotes** (`'`).
- Template literals (backticks `` ` ``): for complex concatenation or multi-line strings.
- **No line continuations** in string literals.

```javascript
// Correct
const greeting = 'Hello, world!';
const multi = `Hello,
World!`;

// Wrong — double quotes for ordinary strings
const greeting = "Hello, world!";
```

---

## Imports & Exports

- **Named exports** preferred over default exports.
- ES modules preferred over CommonJS.
- File extensions **required** in import paths (`.js`).
- ES module `import`/`export from` statements are not line-wrapped.

```javascript
// Correct
import {foo, bar} from './my-module.js';
export {MyClass};

// Wrong — default export
export default class MyClass {}
// Wrong — missing .js extension
import {foo} from './my-module';
```

---

## Whitespace

- Single space after keywords (`if`, `for`, `while`, `catch`, `switch`).
- Single space around binary and ternary operators.
- Space after commas and semicolons.
- **No trailing whitespace.**
- **Trailing commas required** in multi-line arrays, objects, function parameters.
- Single blank line between class methods.

```javascript
// Correct — trailing commas in multi-line
const obj = {
  foo: 1,
  bar: 2,
};

function myFunc(
  arg1,
  arg2,
) {}
```

---

## Equality

- Always use **`===`** and **`!==`** (never `==` / `!=`).

---

## Comments

- `/** ... */` (JSDoc): **only** for API documentation (classes, functions, public members).
- `//` or `/* ... */`: for implementation comments.
- Multi-line `/* ... */`: each continuation line starts with `*` aligned to previous.
- **No boxed comments** with rows of asterisks.

```javascript
/**
 * Sends a message to the server.
 * @param {string} message The message to send.
 * @return {boolean} Whether the message was delivered.
 */
function sendMessage(message) {
  // Implementation comment here
}
```

---

## Disallowed Patterns

| Prohibited | Use instead |
|-----------|-------------|
| `var` | `const` or `let` |
| Default exports | Named exports |
| `==` / `!=` | `===` / `!==` |
| Unary `+` for string-to-number | `Number(x)` or `parseInt(x, 10)` |
| `new Object()` / `new Array()` | `{}` / `[]` literals |
| Line continuation in strings (`\` at EOL) | Template literals |
| `arguments` object | Rest parameter `...args` |
