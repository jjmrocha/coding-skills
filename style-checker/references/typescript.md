# Google TypeScript Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/tsguide.html

Examples in the guide are non-normative: optional formatting choices shown in them must not be enforced as rules.

## Naming Conventions

Identifiers use only ASCII letters, digits, underscores (constants and structured test names), and rarely `$`.

| Identifier | Style | Example |
|-----------|-------|---------|
| Class | `UpperCamelCase` | `MyClass` |
| Interface | `UpperCamelCase` (**no `I` prefix**, no `Interface` suffix) | `UserService`, not `IUserService` |
| Type alias | `UpperCamelCase` | `MyType` |
| Enum | `UpperCamelCase` | `Direction` |
| Enum member | `CONSTANT_CASE` | `Direction.NORTH` |
| Decorator | `UpperCamelCase` | `@Component` |
| TSX component function | `UpperCamelCase` | `<MyComponent />` |
| Function / method / property | `lowerCamelCase` | `getValue`, `sendMessage` |
| Variable / parameter | `lowerCamelCase` | `myVariable` |
| Module-level constant | `CONSTANT_CASE` | `MAX_SIZE` |
| `static readonly` property of a module-level class | `CONSTANT_CASE` | `static readonly MAX = 10` |
| Local `const` inside a function (even if never reassigned) | `lowerCamelCase` | `const defaultTimeout = 5` |
| Type parameter | Single uppercase letter or `UpperCamelCase` | `T`, `RequestType` |
| Namespace import alias | `lowerCamelCase` | `import * as fooBar from './foo_bar'` |
| File name | `snake_case` | `foo_bar.ts` |
| Test method (allowed exception) | Underscores to separate logical segments | `testX_whenY_doesZ` |

### Specific Naming Rules
- **No `I` prefix** for interfaces. Name an interface for why it exists (`TodoItemStorage`).
- **No leading or trailing underscores** on identifiers, including private members. `_` alone (for unused parameters) is also disallowed; skip array elements with extra commas instead: `const [a, , b] = arr;`.
- **No `#private` fields**: use TypeScript's `private` modifier instead.
- **No `opt_` prefix** for optional parameters.
- Treat acronyms as whole words: `loadHttpUrl` not `loadHTTPURL`, `customerId` not `customerID` (exception: platform names such as `XMLHttpRequest`).
- `CONSTANT_CASE` signals "do not modify", so it may be used on values that are not deeply frozen. It is only for module-level symbols, static fields of module-level classes, and enum values. Anything instantiated more than once (a local in a function) uses `lowerCamelCase`.
- A local alias keeps the format of the original name: `const {BrewStateEnum} = SomeType; const CAPACITY = 5;`.
- Observable values may be suffixed with `$` (team convention; be consistent within a project).
- Do not use ambiguous abbreviations or delete letters within a word. Short names only for variables in scope for 10 lines or fewer.

---

## Formatting

- The TypeScript guide sets **no column limit and no indentation size**; Google formats TypeScript with an automatic formatter. Do not report line length. The guide's examples use 2-space indentation; report indentation only when it is inconsistent within a file.
- UTF-8 encoding. The only whitespace character is the ASCII space; other whitespace in strings is escaped.
- Use special escape sequences (`\n`, `\t`, `\'`) over numeric escapes. Use real Unicode characters, not escapes, except for non-printable characters (with a comment).
- No blank lines at the start or end of a function body.
- No space after `...` in rest or spread.
- Generators: `function* foo()` and `yield* iter`, not `function *foo()`.
- Parentheses around a single arrow-function parameter are recommended but not required.

---

## Strings

- Ordinary string literals: **single quotes** (`'`). If a string contains a single quote, consider a template literal.
- Template literals (backticks): for complex concatenation or multi-line strings.
- **No line continuations** (`\` at end of line) in string literals. Use `+` concatenation.

---

## File Structure

Files consist of, in order (exactly one blank line between each present section):
1. Copyright/license, in a JSDoc at the top (if needed)
2. JSDoc `@fileoverview` (if present; wrapped lines are not indented)
3. Imports
4. Implementation

---

## Imports & Exports

- Use **relative imports** (`./foo`) for files in the same project. Limit `../../../` chains.
- **Named exports only. No default exports.** Default imports only for external code that requires them.
- **No `require()`** (`import x = require('...')`) and no `/// <reference>`: use ES6 `import`.
- **No `namespace Foo {}`** (or `module Foo {}`): use ES modules.
- **No `export let`**: mutable exports are not allowed; export a getter function instead.
- No container classes with only static members for namespacing; export individual constants and functions.
- Only export what is used outside the module.

```typescript
// Correct
import {Foo} from './foo';
export {MyClass};

// Wrong — default export
export default class MyClass {}
// Wrong — require
import foo = require('./foo');
```

### Import Style
- Namespace imports (`import * as tableview from './tableview'`) for many symbols from a large API. Named imports (`import {describe, it} from './testing'`) for frequently used, clearly named symbols. Both are allowed.
- Fix name collisions with a namespace import or by renaming the export. Renaming an import with `as` is allowed when needed.
- `import type {Foo}` **may** be used for type-only imports; it is not required. Use `export type` when re-exporting a type.

---

## Variables, Arrays, Objects

- `const` by default, `let` when reassigned. **Never `var`.** Do not use a variable before its declaration.
- **One variable per declaration.**
- No `Array()` constructor (with or without `new`) and no `Object` constructor. Use literals.
- No non-numeric properties on arrays.
- Spread only matching shapes: iterables into arrays, objects into objects. Never spread `null`, `undefined`, or primitives.
- Destructured parameters: one level of unquoted shorthand properties; defaults on the left (`{num, str = 'default'}: Options = {}`).
- Do not use unfiltered `for...in`. Filter with `hasOwnProperty`, or use `for...of` with `Object.keys`, `Object.values`, or `Object.entries`.
- Do not mix quoted and unquoted keys in an object literal.

---

## Classes

- Class declarations: **no trailing semicolon**. Statements containing class expressions end with a semicolon.
- No semicolons between methods. Methods are separated by a **single blank line**.
- The constructor is separated from surrounding code by a blank line above and below.
- Blank lines just inside the class braces are neither encouraged nor discouraged.
- `new Foo()` — parentheses required even with no arguments.
- Omit empty constructors and constructors that only call `super()`. Keep constructors that have parameter properties, visibility modifiers, or parameter decorators.

### Class Members
- Mark properties never reassigned outside the constructor with `readonly`.
- Use parameter properties: `constructor(private readonly service: Service) {}`.
- Initialize fields at declaration when possible.
- **No `public` modifier**, except for non-readonly public parameter properties.
- Limit visibility as much as possible. Properties used from templates are `protected` (Angular) or `public` (Polymer), not `private`. Never use `obj['foo']` to bypass visibility.
- Prefer module-local functions over **private static methods**.
- **Static methods**: call them only on the class that defines them. Never use `this` in a static context.
- **Getters**: must be pure (no observable side effects). At least one accessor of a pair must have logic; do not hide a property behind pass-through accessors. Never define accessors with `Object.defineProperty`.
- Computed class properties only for symbols.
- Classes usually should not have properties initialized to arrow functions. Exception: event handlers that must be uninstalled.
- `toString` may be overridden, but must always succeed and have no side effects.
- Do not manipulate prototypes directly.

---

## Functions

- **Prefer function declarations** for named top-level functions. An arrow function is fine when an explicit type annotation is needed.
- Nested functions may be declarations or arrow functions; in methods prefer arrow functions.
- **No function expressions** (`function() {...}` as a value). Use arrow functions. Exception: rebinding `this` (discouraged) and generators.
- Use a concise arrow body only when the return value is used. Otherwise use a block body or `void`: `promise.then(v => void console.log(v))`.
- Prefer passing an arrow function that forwards arguments over passing a named function as a callback: `.map((n) => parseInt(n))`, not `.map(parseInt)`.
- Prefer arrow functions over `f.bind(this)` or `const self = this`. Do not use `bind` when installing an event handler.
- Parameter default initializers must have no side effects and stay simple.
- Rest parameters (`...args`) instead of `arguments`; spread instead of `Function.prototype.apply`.
- `this` only in constructors, methods, functions with an explicit `this` type, and arrow functions inside those.

---

## Control Structures

- **Braces required** for all control flow statements. The first statement of a non-empty block starts on its own line.
- Exception: an `if` that fits on one line may omit braces: `if (x) x.doFoo();`.
- Avoid assignment inside conditions. If intended, wrap it in extra parentheses: `while ((x = next())) {`.
- `switch` must contain a `default` group, placed last. Non-empty groups must not fall through; empty groups may.
- Prefer `for (... of ...)` for arrays; `forEach` and indexed `for` are allowed. **No `for...in` on arrays.**
- Grouping parentheses are recommended; no unnecessary parentheses after `delete`, `typeof`, `void`, `return`, `throw`, `case`, `in`, `of`, `yield`.
- Keep `try` blocks focused on the code that can throw.

---

## Exceptions

- Always `new Error()`, never `Error()` alone.
- Throw and reject only `Error` or its subclasses: never `throw 'text'` or `Promise.reject('text')`.
- In `catch`, assume the value is an `Error`. Handle non-`Error` values only when an API is known to throw them, with a comment.
- An empty `catch` block requires a comment explaining why doing nothing is correct.

---

## Type Coercion

- Coerce with `String()`, `Boolean()` (no `new`), template literals, or `!!`.
- Parse numbers with `Number()` and check for `NaN`. **No unary `+`** to convert strings. No `parseInt`/`parseFloat` except for non-base-10 strings after validating the digits.
- Do not convert enum values to booleans (`Boolean(level)`, `!!level`, `if (level)`). Compare explicitly: `level !== SupportLevel.NONE`.
- Do not write `!!x` in an `if`, `for`, or `while` condition: write `if (x)`.

---

## Type Annotations

- Leave out types that are trivially inferred from a string, number, boolean, RegExp literal, or `new` expression: `const x = 5`, not `const x: number = 5`.
- Return type annotations are **up to the author**. Do not report a missing return type.
- Use **lowercase primitive types**: `string`, `number`, `boolean` — never `String`, `Number`, `Boolean`, or `Object`.
- **Use interfaces, not type aliases, for object types**: `interface User {...}`, not `type User = {...}`.
- Declare the type of a structural value at its declaration: `const foo: Foo = {...}`. Use interfaces, not classes, to define structural types.
- Array types: `T[]` / `readonly T[]` for simple types (letters, digits, dots), at every nesting level. `Array<T>` / `ReadonlyArray<T>` for anything more complex: `Array<{n: number}>`, `Array<string|number>`.
- Index signatures use a **meaningful key label**: `{[userName: string]: number}`, not `{[key: string]: number}`. Consider `Map` or `Set` instead.
- **No `{}` type** in most cases — prefer `unknown`, `Record<string, T>`, or `object`.
- **Avoid `any`**: prefer a specific type or `unknown`. If `any` is needed, suppress the lint warning and explain why.
- **Type aliases must not include `|null` or `|undefined`**. Add them where the alias is used.
- Prefer optional fields and parameters (`?`) over `|undefined`.
- Prefer tuples over ad-hoc `Pair` interfaces, or better, an object type with named properties.
- Use the simplest type construct that works; mapped and conditional types are allowed but interface extension is often clearer.
- Avoid return-type-only generics; when calling such APIs, specify the generic explicitly.

## Type Assertions

- Use **`as` syntax** (`value as Type`), never angle brackets (`<Type>value`).
- Type assertions and non-null assertions (`y!`) need an obvious reason or a comment explaining why they are safe. Prefer a runtime check.
- Double assertions go through `unknown`: `value as unknown as NarrowType`.
- Use a type annotation, not an assertion, to type an object literal: `const foo: Foo = {...}`, not `{...} as Foo`.
- **Never** use `@ts-ignore`, `@ts-expect-error`, or `@ts-nocheck`. `@ts-expect-error` may be used in unit tests, though generally it should not.

---

## Decorators

- Do not define new decorators; use only framework decorators (Angular, Polymer).
- A decorator immediately precedes what it decorates, with no blank line. Field decorators may share the line.
- JSDoc goes **before** the decorator, never between the decorator and the declaration.

---

## Comments & Documentation

- `/** JSDoc */` for documentation that users of the code read; `//` for implementation comments.
- **Multi-line implementation comments use several `//` lines, not `/* */`.**
- **No boxed comments** with asterisks.
- A one-line JSDoc that overflows must switch to the multi-line form. JSDoc is Markdown; use Markdown lists, not indented text.
- Most JSDoc tags occupy their own line. Wrapped block tag lines are indented **4 spaces**.
- **No JSDoc types** in `@param`/`@return`, and no `@implements`, `@enum`, `@private`, `@override` where the TypeScript keyword exists.
- `@param` and `@return` only when they add information beyond the name and type. Do not just restate the parameter name.
- Document all top-level exports, except symbols consumed only by tooling (such as `@NgModule` classes).
- Method descriptions are third-person verb phrases (`Sends a message.`), not imperative.
- Document parameter properties with `@param` on the constructor.
- Parameter name comments: `someFunction(obviousParam, /* shouldRender= */ true)`.
- Deprecations use `@deprecated` with directions for fixing call sites.

```typescript
/**
 * Sends a message to the server.
 * @param message The message to send. Must be shorter than the
 *     server's limit.
 */
function sendMessage(message: string): boolean {
  // Implementation comment
}
```

---

## Semicolons & Trailing Commas

- **Semicolons mandatory** at end of every statement. Do not rely on automatic semicolon insertion.
- Trailing commas: the guide sets no rule. Its examples use them in multi-line array and object literals. Do not report their absence in function parameters.

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
| `export let` (mutable binding export) | Export a `const`, or a getter |
| `with` statement | Explicit property access |
| `#private` fields | TypeScript `private` modifier |
| `namespace Foo {}` | ES modules |
| `const enum` | Plain `enum` |
| `require()` | `import` |
| `any` type | `unknown` or specific types |
| `IFoo` interface prefix | `Foo` |
| Leading/trailing `_` on identifiers | TypeScript visibility modifiers |
| `new String()`, `new Boolean()`, `new Number()` | Primitives directly |
| Unary `+`, `parseInt` / `parseFloat` for base 10 | `Number()` with a `NaN` check |
| `eval` or `Function(string)` | Explicit functions |
| `debugger` in production | Remove before committing |
| `@ts-ignore` / `@ts-nocheck` / `@ts-expect-error` | Fix the type error (`@ts-expect-error` tolerated in unit tests) |
| `<Type>value` assertions | `value as Type` |
| `type Foo = {...}` for object types | `interface Foo {...}` |
| Function expressions | Arrow functions |
| Modifying builtin prototypes | — |
