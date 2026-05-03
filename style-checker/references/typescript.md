# Google TypeScript Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/tsguide.html

## Naming Conventions

| Identifier | Style | Example |
|-----------|-------|---------|
| Class | `UpperCamelCase` | `MyClass` |
| Interface | `UpperCamelCase` (**no `I` prefix**) | `UserService`, not `IUserService` |
| Type alias | `UpperCamelCase` | `MyType` |
| Enum | `UpperCamelCase` | `Direction` |
| Enum member | `CONSTANT_CASE` | `Direction.NORTH` |
| Decorator | `UpperCamelCase` | `@Component` |
| TSX component | `UpperCamelCase` | `<MyComponent />` |
| Function / method | `lowerCamelCase` | `getValue`, `sendMessage` |
| Variable / parameter | `lowerCamelCase` | `myVariable` |
| Global constant (module-level, immutable) | `CONSTANT_CASE` | `MAX_SIZE` |
| `static readonly` class property | `CONSTANT_CASE` | `static readonly MAX = 10` |
| Local `const` (even if never reassigned) | `lowerCamelCase` | `const defaultTimeout = 5` |
| Type parameter | `UpperCamelCase` or single uppercase letter | `T`, `RequestType` |
| Namespace import alias | `lowerCamelCase` | `import * as fooBar` |
| File name | `snake_case` | `my_module.ts`, `user_service.ts` |
| Test method (allowed exception) | Underscores to separate logical segments | `testX_whenY_doesZ` |

### Specific Naming Rules
- **No `I` prefix** for interfaces: `UserService` not `IUserService`.
- **No leading or trailing underscores** on identifiers (including private ones).
- **No `#private` fields**: use TypeScript's `private` modifier instead.
- **No `opt_` prefix** for optional parameters.
- Treat acronyms as whole words: `loadHttpUrl` not `loadHTTPURL` (exception: `XMLHttpRequest`).
- Observable values may suffix with `$` (team convention, not a hard rule).
- Single `_` as a standalone identifier is disallowed.

---

## Indentation & Line Length

- **2 spaces** per level. **Never tabs.**
- **80 characters** maximum line length (same as JavaScript).
- UTF-8 encoding required.
- Only ASCII horizontal space (0x20) as whitespace character.

---

## Strings

- Ordinary string literals: **single quotes** (`'`).
- Double quotes reserved when the string contains single quotes.
- Template literals (backticks): for multi-line strings or complex interpolation.
- **No line continuations** in string literals.

---

## File Structure

Files consist of, in order (exactly one blank line between each section):
1. Copyright/license (if needed)
2. JSDoc `@fileoverview` (if present)
3. Imports
4. Implementation

---

## Imports & Exports

- Use **relative imports** (`./foo`) rather than absolute paths within a project.
- Prefer **named exports** over default exports.
- **No default exports.**
- **No `require()`**: use ES6 `import` syntax.
- **No namespace keyword** (`namespace Foo { }`): use ES modules.

```typescript
// Correct
import {Foo} from './foo';
export {MyClass};

// Wrong — default export
export default class MyClass {}
// Wrong — no I prefix
interface IUserService {}
// Wrong — require
const foo = require('./foo');
```

### Import Type Organization
- `import type {Foo}` for imports used only as types.
- Module imports: `import * as ng from '@angular/core';` when using many symbols.
- Named imports: `import {Foo} from './foo';` for specific symbols.

---

## Classes

- Class declarations: **no trailing semicolon**.
- Class expressions (assigned to variables): end with semicolon.
- Methods: separated by a **single blank line**; no semicolons between methods.
- Constructor: blank line above and below.
- `new Foo()` (parentheses required even with no arguments).

### Class Members
- Mark properties never reassigned with `readonly`.
- Use parameter properties: `constructor(private readonly service: Service) {}`.
- Initialize fields at declaration when possible.
- **No `public` modifier** except for non-readonly public parameter properties.
- Visibility minimized: use `private` or `protected` where possible.

---

## Functions

- **Prefer function declarations** over arrow functions for named functions.
- **No function expressions for named functions**: use arrow functions instead.
- Use rest parameters (`...args`) instead of `arguments`.
- **No blank lines** at start or end of function body.
- Generator syntax: `function* foo()` and `yield* iter`.

---

## Control Structures

- **Braces required** for all control flow statements, even single-statement bodies.
- Exception: `if` on one line may elide braces.
- `switch` must contain a `default` statement group (last).
- Non-empty cases must end with `break` or `return`.
- Prefer `for (... of ...)` for array iteration.
- **No `for...in`** on arrays — only on dict-style objects with `hasOwnProperty` check.

---

## Type Annotations

- **Annotate** public API: function parameters, return types, exported symbols.
- **Omit** types that TypeScript can trivially infer: `const x = 5` not `const x: number = 5`.
- Array types: `string[]` (simple) or `Array<{x: number}>` (complex types).
- **Avoid `any`**: prefer `unknown` for opaque values.
- `Type | null` or `Type | undefined` instead of wrapper types.
- Prefer optional fields (`?`) over `| undefined` in object types.
- **Type aliases must not include `|null` or `|undefined`** in a union type.

---

## Comments & Documentation

- `/** JSDoc */`: for public API documentation (written in Markdown).
- `//`: for implementation comments (multi-line implementation comments use `//`, not `/* */`).
- Each JSDoc block tag (`@param`, `@returns`, `@deprecated`) on its own line.
- **No boxed comments** with asterisks.

```typescript
/**
 * Sends a message to the server.
 * @param message The message to send.
 * @returns Whether the message was delivered.
 */
function sendMessage(message: string): boolean {
  // Implementation comment
}
```

---

## Semicolons & Trailing Commas

- **Semicolons mandatory** at end of every statement.
- **Trailing commas required** in multi-line arrays, objects, function parameters.

---

## Equality

- Always **`===`** and **`!==`**.
- Exception: `== null` or `!= null` to check both `null` and `undefined`.

---

## Disallowed Patterns

| Prohibited | Use instead |
|-----------|-------------|
| `var` | `const` or `let` |
| Default exports | Named exports |
| `#private` fields | TypeScript `private` modifier |
| `namespace Foo {}` | ES modules |
| `const enum` | Plain `enum` |
| `require()` | `import` |
| `any` type | `unknown` or specific types |
| `IFoo` interface prefix | `Foo` |
| Leading/trailing `_` on identifiers | TypeScript visibility modifiers |
| `new String()`, `new Boolean()`, `new Number()` | Primitives directly |
| `eval` or `Function(string)` | Explicit functions |
| `debugger` in production | Remove before committing |
