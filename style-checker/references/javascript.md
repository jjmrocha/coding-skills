# Google JavaScript Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/jsguide.html

## Source File Basics & Structure

- File names: **all lowercase**, may include `_` or `-`, no other punctuation, extension `.js`. Follow the project's convention.
- Encoding: **UTF-8**. The only ASCII whitespace is the space (0x20) — **tabs forbidden** for indentation; other whitespace in strings is escaped.
- Use special escape sequences (`\'`, `\"`, `\\`, `\b`, `\f`, `\n`, `\r`, `\t`, `\v`) over numeric escapes (`\x0a`, `\u000a`, `\u{a}`). Legacy octal escapes are never used.
- New files are either a `goog.module` file or an ES module.
- File sections in order, exactly one blank line between each present section (the implementation may be preceded by 1 or 2):
  1. License / copyright (if present)
  2. `@fileoverview` JSDoc (if present)
  3. `goog.module` statement (goog.module file)
  4. ES `import` statements (ES module)
  5. `goog.require` / `goog.requireType` statements
  6. Implementation

---

## Naming Conventions

Identifiers use only ASCII letters and digits (underscores in the cases below; `$` only when a framework requires it).

| Identifier | Style | Example |
|-----------|-------|---------|
| Class / Interface / Record / Typedef | `UpperCamelCase` | `Request`, `Readable` |
| Function / method | `lowerCamelCase` | `sendMessage`, `stop` |
| Private method or field (optional) | `lowerCamelCase_` (trailing underscore) | `myPrivateHelper_`, `index_` |
| Variable / parameter | `lowerCamelCase` (even if it holds a constructor) | `myVariable` |
| Constant (module-level or `@const` static, deeply immutable) | `CONSTANT_CASE` | `MAX_SIZE` |
| `const` inside a function, or a mutable module-level `const` | `lowerCamelCase` | `defaultTimeout`, `logger` |
| Enum name | `UpperCamelCase`, singular noun | `Direction` |
| Enum member | `CONSTANT_CASE` | `Direction.NORTH` |
| Package / namespace | `lowerCamelCase` | `my.exampleCode.deepSpace` |
| Template parameter | Single word or letter, all caps | `TYPE`, `THIS`, `T` |
| Module import (`import * as`) | `lowerCamelCase` derived from the file name | `import * as fileOne from '../file-one.js'` |
| JsUnit test method | underscores may separate components | `testPop_emptyStack_throws` |

### Naming Principles
- Use **descriptive names**. Do not use ambiguous or project-only abbreviations, or abbreviate by deleting letters (`cstmrId`).
- Avoid Hungarian notation (`kSecondsPerDay`).
- Short (single-letter) names only for variables in scope for 10 lines or fewer, including non-exported parameters.
- One-character parameter names are not used in public methods.
- Acronyms in names: treat as whole words — `loadHttpUrl` not `loadHTTPURL`, `newCustomerId` not `newCustomerID`.
- Constants never end with a trailing underscore.
- Module-local names are not marked `@private`.
- A named import keeps its name. Avoid aliasing (`import {Foo as Bar}`); if needed, build the alias from the imported file's name or path.

### Getters/Setters
- Never required. If used: `getFoo()`, `isFoo()` / `hasFoo()` for booleans, `setFoo(value)`.

---

## Indentation & Line Length

- **2 spaces** per block level. **Never tabs.**
- **80 characters** maximum line length.
- Continuation lines: at least **+4 spaces** from original line. Deeper syntactic levels use larger multiples of 4.
- Exceptions to line limit: `goog.module`, `goog.require`, `goog.requireType`, ES `import` and `export from` statements (these are never wrapped), and lines where the limit is impossible or would hurt searchability (long URL, shell command, long file path string).

### Line Wrapping
- Break at the **highest syntactic level** possible.
- When breaking at an operator, the break comes **after** the symbol (unlike Java). The dot `.` is not an operator: break before it.
- Method name stays attached to `(`. Comma stays attached to the preceding token.
- Never break between `return` and the return value.
- Function arguments that don't fit: start them on a new line indented 4, or one per line indented 4. Aligning to the parenthesis is allowed but discouraged.

---

## Braces & Control Flow

- K&R style: no line break before `{`; line break after `{` and before `}`. No line break after `}` when followed by `else`, `catch`, `while`, `,`, `;`, or `)`.
- Braces **required** for all control structures, even single-statement bodies. The first statement of a non-empty block starts on its own line.
- Only exception: a simple `if` with no `else` that fits on one line may omit braces.
- Empty blocks may be `{}`, but **not** in multi-block statements (`if/else`, `try/catch/finally`).
- **`for...of`** preferred. **`for...in`** only on dict-style objects, never on arrays, with a `hasOwnProperty` check. Prefer `Object.keys` over `for...in`.

```javascript
// Correct
if (condition) {
  doSomething();
}

// Allowed (no else, fits on one line)
if (condition) doSomething();

// Wrong — braces required
for (let i = 0; i < foo.length; i++) bar(foo[i]);
```

---

## Switch Statements

- Contents indented +2; statements after a label indented a further +2.
- Each group ends with `break`, `return`, or `throw`, or is marked with a comment such as `// fall through` (not needed for the last group).
- Every switch has a `default` group, even if empty, and it is **last**.

---

## Variable Declarations

- Use **`const`** by default, **`let`** when reassigned. **Never `var`.**
- **One variable per declaration** (`let a = 1; let b = 2;` not `let a = 1, b = 2;`).
- Declare variables **close to first use** and initialize them as soon as possible.
- JSDoc types go on the line above or inline (`const /** !Array<number> */ data = [];`), never both.

---

## Object & Array Literals

- Use `{}` and `[]` literals — never `new Object()` or the variadic `new Array(a, b)` (`new Array(length)` is allowed).
- **Do not mix** quoted and unquoted keys in a single object literal. Computed keys count as quoted unless they are symbols.
- Method shorthand (`{method() {}}`) and property shorthand (`{foo, bar}`) are allowed.
- **Trailing comma** whenever a line break separates the final element from the closing `]` or `}`.
- No non-numeric properties on arrays (other than `length`).
- Destructured parameters: one level of unquoted shorthand properties; defaults on the left side (`{str = 'x'} = {}`); an optional destructured object defaults to `{}`, an optional array to `[]`.
- No space after `...` in spread and rest.

### Enums
- Defined with `@enum` on an object literal, module-local or directly on `exports`.
- Values are string literals or numbers; string values are never computed.

---

## Number Literals

- Use exactly `0x`, `0o`, `0b` prefixes with **lowercase** letters (`0xff`, not `0XFF`).
- Never a leading zero unless it is followed by `x`, `o`, or `b`.

---

## Functions

- **Arrow functions** are preferred over `function` for nested functions and callbacks, and over `bind(this)` or `const self = this`.
- Top-level functions may be declared locally (including `const f = (x) => {...}`) or defined on `exports`.
- A named nested function is assigned to a local `const`.
- Arrow body: a single expression only when a value must be returned, or when `void` precedes a single call. Otherwise use a block.
- Parentheses around a single non-destructured arrow parameter are optional.
- Generators: `function* name()`, and `yield* iter` for delegation.
- Rest parameters (`...numbers`) over the `arguments` object. Never name a variable `arguments` or a rest parameter `var_args`.
- **Spread** preferred over `Array.prototype.slice.call()` and `.concat()`.

```javascript
// Correct
items.map((x) => x * 2);
getValue((result) => void alert(`Got ${result}`));

// Wrong — single-expression body with no value needed and no void
const moduleLocalFunc = () => anotherFunction();
```

---

## Classes

- No semicolon after methods or after a class **declaration**.
- Subclass constructors call `super()` before touching `this`.
- Define all fields in the constructor. Mark never-reassigned fields `@const`, non-public fields `@private` / `@protected` / `@package`.
- Do not manipulate `prototype` directly. Getters and setters (`get`/`set`) are allowed.

---

## Semicolons

- **Mandatory** at end of every statement. Relying on ASI (Automatic Semicolon Insertion) is forbidden.

---

## Strings

- Ordinary string literals: **single quotes** (`'`). They may not span multiple lines.
- Template literals (backticks): for complex concatenation or multi-line strings. Multi-line templates need not follow block indentation.
- **No line continuations** (`\` at end of line) in any string literal. Use `+` concatenation instead.

```javascript
// Correct
const greeting = 'Hello, world!';

// Wrong — double quotes for ordinary strings
const greeting = "Hello, world!";
```

---

## Imports & Exports

- **Named exports only**. Default exports are not used.
- File extension **required** in import paths (`.js`).
- Do not import the same file more than once.
- ES module files import other ES modules with `import`, never `goog.require`.
- Exported variables are not mutated outside module initialization.

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

### Vertical
- One blank line between consecutive methods in a class or object literal.
- Blank lines inside function bodies sparingly; **no blank line at the start or end of a function body**.
- Multiple consecutive blank lines are permitted, never required.

### Horizontal — a single space appears only:
- Between a reserved word (except `function` and `super`) and a following `(`.
- Between `}` and a following `else` or `catch`.
- Before `{`, except an object literal that is the first argument or first array element (`foo({a: [{c: d}]})`) and inside `${}`.
- On both sides of binary and ternary operators.
- After `,` and `;` — **never before** them.
- After `:` in an object literal.
- On both sides of the `//` of an end-of-line comment (multiple spaces allowed).
- Inside short type comments: `/** @type {number} */ (bar)`, `baz(/* buzz= */ true)`.
- **No trailing whitespace.**

**Horizontal alignment** of tokens across lines is permitted but **discouraged**. Report it as Low.

---

## Parentheses

- Grouping parentheses are recommended; omit them only when nobody could misread the code.
- No unnecessary parentheses around the whole expression after `delete`, `typeof`, `void`, `return`, `throw`, `case`, `in`, `of`, `yield`.
- Always use `()` with `new`: `new Foo()`, never `new Foo`.

---

## Equality

- Use **`===`** and **`!==`**. Exception: `x == null` is allowed to catch both `null` and `undefined`.

---

## Error Handling

- Always **`throw new Error()`** or a subclass — never throw strings or plain objects. The same applies to `Promise.reject()`.
- An **empty catch block** requires a comment explaining why doing nothing is correct.

```javascript
try {
  return handleNumericResponse(response);
} catch (ok) {
  // it's not numeric; that's fine, just continue
}
```

---

## Comments

- Block comments are indented like the surrounding code, `/* ... */` or `//` style. Continuation lines of `/* */` start with `*` aligned with the `*` above.
- **No boxed comments**. **No JSDoc (`/** */`) for implementation comments.**
- Parameter name comments: `someFunction(obviousParam, /* shouldRender= */ true)`.

### JSDoc
- Used on all classes, fields, and methods. Written in Markdown.
- Most tags occupy their own line. Simple tags (`@private`, `@const`, `@final`, `@export`) may share a line.
- Wrapped block tag lines are indented **4 spaces**. `@fileoverview` and `@desc` text is not indented when wrapped.
- A one-line JSDoc that overflows must switch to the multi-line form.
- Method descriptions are third-person verb phrases (`Sends a message.`), not imperative.
- Parameter and return types are always documented; descriptions may be omitted when obvious.
- An overriding method has `@override` and repeats all `@param` and `@return` tags.
- Classes, interfaces, and records have a description. Enums and typedefs have `@enum` / `@typedef`; public ones also have a description.

```javascript
/**
 * Sends a message to the server.
 * @param {string} message The message to send, with a description long
 *     enough to wrap onto a second line.
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
| `==` / `!=` (except `== null`) | `===` / `!==` |
| `new Boolean()`, `new Number()`, `new String()` | Call them as functions to coerce: `Number(x)` (preferred over unary `+`) |
| `new Object()` / variadic `new Array()` | `{}` / `[]` literals |
| Line continuation in strings (`\` at EOL) | `+` concatenation or template literals |
| `arguments` object | Rest parameter `...args` |
| `for...in` on arrays | `for...of` |
| Throwing non-`Error` values | `throw new Error()` |
| Empty catch without comment | Comment explaining why |
| `with`, `eval`, `Function(string)` | — |
| Modifying builtin prototypes | — |
| `this` outside classes, their arrow functions, or an explicit `@this` | — |
| Non-standard language features | Standard ECMA-262 / WHATWG features |
