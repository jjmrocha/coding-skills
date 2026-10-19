# Google Kotlin Style Guide (Android) — Formatting & Naming

Source: https://developer.android.com/kotlin/style-guide

Google's Kotlin style is the Android Kotlin style guide. It differs from JetBrains' Kotlin coding conventions in several places: a 100-column limit, no concise empty blocks `{}`, no backtick function names with spaces (even in tests), and stricter rules on what may be named as a constant. Follow this file, not the JetBrains conventions.

## Source Files

- Encoding: **UTF-8**. The only whitespace character is the ASCII space; tabs are not used for indentation; other whitespace in literals is escaped.
- Use special escape sequences (`\b`, `\n`, `\r`, `\t`, `\'`, `\"`, `\\`, `\$`) instead of Unicode escapes. Unicode escapes for printable characters are discouraged.

### File Names
- A file with a **single top-level class**: the class name + `.kt` (`MyClass.kt`).
- A file with **several top-level declarations**: a PascalCase name describing the contents (`Map.kt`). **camelCase is acceptable when the name is plural**: `extensions.kt` is correct. Do not report it.

### File Structure
In order, with **exactly one blank line** between sections:
1. Copyright / license header (optional)
2. File-level annotations (`@file:...`)
3. `package` statement
4. `import` statements
5. Top-level declarations

- The copyright header is a **`/* ... */` block comment** at the very top. A KDoc-style `/** ... */` or `//` line comments are wrong.
- `package` and `import` lines are never wrapped and have no column limit.
- **Imports form one single list, ASCII sorted**, with no blank lines or groups inside it.
- **No wildcard imports** of any kind (`import kotlinx.coroutines.*` is wrong).
- A file focuses on one theme; members follow some logical order the maintainer could explain (not "appended at the end").

---

## Naming

Identifiers use only ASCII letters and digits (underscores only in the cases below). No special prefixes or suffixes (`name_`, `mName`, `s_name`, `kName`), except backing properties.

| Identifier | Style | Example |
|-----------|-------|---------|
| Package | all lowercase, words concatenated | `com.example.deepspace` (not `deepSpace`, `deep_space`) |
| Class, interface, object, enum, type alias | `PascalCase` | `ImmutableList`, `Readable` |
| Test class | class under test + `Test` | `HashTest`, `HashIntegrationTest` |
| Function | `camelCase` | `sendMessage`, `stop` |
| `@Composable` function returning `Unit` | `PascalCase` noun | `NameTag(name)` |
| Test function | `camelCase`, underscores may separate parts | `pop_emptyStack` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_COUNT` |
| Non-constant property, local, parameter | `camelCase` | `logger`, `mutableCollection` |
| Backing property | `_` + exact name of the real property | `_table` for `table` |
| Type variable | one capital letter, optionally + digit; or class-style name + `T` | `E`, `T2`, `RequestT` |

### What Is a Constant
- A `val` with no custom getter whose contents are **deeply immutable** and whose functions have no side effects: scalars, strings, immutable types, immutable collections of immutable types.
- Constants are defined **only at top level or inside an `object`** (including a `companion object`). A value inside a class body that otherwise qualifies uses a **non-constant (`camelCase`) name**.
- **Scalar constants must use `const`**: `const val NUMBER = 5`. A top-level `val DEFAULT_LIMIT = 5` without `const` is wrong.
- Not constants (use `camelCase`): mutable collections, arrays with content, loggers, anything with observable mutable state: `val logger = Logger.getLogger(...)`, `val pendingIds = mutableListOf<String>()`.

```kotlin
const val NUMBER = 5
val NAMES = listOf("Alice", "Bob")
val EMPTY_ARRAY = arrayOf<SomeMutableType>()

val mutableCollection: MutableSet<String> = HashSet()
val logger = Logger.getLogger(MyClass::class.java.name)
```

### Function Names Without Spaces
- **Function names must not contain spaces**, not even in tests: `` fun `test every possible case`() `` is wrong; write `fun testEveryPossibleCase()`.

### Camel Case and Acronyms
- Lowercase everything, including acronyms, then capitalize word starts: `XmlHttpRequest`, `newCustomerId`, `supportsIpv6OnIos`, `parseJson` — not `XMLHTTPRequest`, `newCustomerID`, `parseJSON`.
- `YoutubeImporter` is acceptable but not recommended (`YouTubeImporter`).

---

## Braces

- Braces may be omitted only for an `if` or `when` branch that has **at most one `else` and fits on a single line**: `if (string.isEmpty()) return`, `val v = if (a) 0 else 1`.
- Otherwise braces are **required** for `if`, `for`, `when` branches, `do`, and `while`, even for empty or single-statement bodies. An `if` whose body sits on the next line without braces is wrong. A multi-line `if`/`else` expression without braces is wrong.
- Non-empty blocks use K&R style: no line break before `{`; line break after `{` and before `}`; line break after `}` only if it ends a statement or the body of a function, constructor, or named class (not before `else` or a comma).
- **Empty blocks must also be K&R style.** `catch (e: Exception) {}` is wrong; write `{` then a line break, then `}`.

```kotlin
try {
    doSomething()
} catch (e: Exception) {
} // Okay
```

---

## Indentation, Statements, Line Length

- **+4 spaces** for each new block. 2-space indentation is wrong.
- One statement per line. **No semicolons.**
- **100-column limit.** Exceptions: lines where it is impossible (a long URL in KDoc), `package` and `import` statements, command lines in comments meant to be pasted into a shell.

### Where to Break
- Prefer breaking at a higher syntactic level.
- At an operator or infix function, break **after** it.
- Break **before** `.`, `?.`, and `::`.
- A function or constructor name stays attached to `(`. A comma stays attached to the token before it. A lambda arrow `->` stays attached to its argument list.

### Function Signatures
- When a signature does not fit on one line, put **each parameter on its own line** with a **+4** indent. The closing `)` and the return type go on their own line with no extra indent.

```kotlin
fun <T> Iterable<T>.joinToString(
    separator: CharSequence = ", ",
    prefix: CharSequence = "",
    postfix: CharSequence = ""
): String {
    // ...
}
```

- A function with a single expression may be an expression function: `override fun toString(): String = "Hey"`.

### Properties
- If an initializer does not fit, break after `=` and indent +4.
- `get` / `set` each on their own line, indented +4. A read-only property may use the one-line form: `val defaultExtension: String get() = "kt"`.

### Implicit Types
- A return or property type may be omitted when the body is a scalar or clearly inferred: `override fun toString() = "Hey"`. In a library, keep explicit types that are part of the public API.

---

## Whitespace

### Vertical
- One blank line between consecutive class members (properties, constructors, functions, nested classes). Between two consecutive properties it is optional.
- Blank lines between statements as needed. Before the first statement or member, or after the last member: optional.
- Multiple consecutive blank lines are permitted but never required or encouraged.

### Horizontal — a single space appears only:
- Between a reserved word (`if`, `for`, `catch`) and a following `(`: `for (i in 0..1)`, not `for(`.
- Between a reserved word (`else`, `catch`) and a preceding `}`: `} else {`, not `}else`.
- Before any `{`: `if (list.isEmpty()) {`.
- On both sides of binary operators: `1 + 1`. Also around a lambda arrow: `{ value -> value.toString() }`.
- **Not** around `::` (`Any::toString`), `.` (`it.toString()`), or the range operator `..` (`1..4`).
- **Before a colon only** in a class declaration's supertype list or in a generic constraint: `class Foo : Runnable`, `fun <T : Comparable<T>> max(a: T, b: T)`, `where T : Comparable<T>`. `class Foo: Runnable` and `<T: Comparable<T>>` are wrong.
- After a comma or colon: `listOf(1, 2)`, `class Foo : Runnable`.
- On both sides of the `//` of an end-of-line comment: `var debugging = false // disabled`.

---

## Specific Constructs

### Enum Classes
- An enum with no functions and no documentation on its constants may be on one line: `enum class Answer { YES, NO, MAYBE }`.
- Constants on separate lines need no blank lines between them, except constants with a body.

### Annotations
- Member and type annotations go on separate lines immediately before the declaration.
- Annotations **without arguments** may share one line: `@JvmField @Volatile`.
- A **single annotation without arguments** may sit on the declaration line: `@Volatile var disposable: Disposable? = null`, `@Test fun selectAll()`.
- An annotation **with arguments** goes on its own line: `@Deprecated("Use sumAll") fun oldSum()` on one line is wrong.
- `@[...]` only with an explicit use-site target, to combine two or more argument-less annotations: `@field:[JvmStatic Volatile]`.

---

## Documentation (KDoc)

- Basic form `/** ... */` over several lines; the single-line form `/** Short text. */` only when it fits and has no block tags.
- A line with only `*` separates paragraphs and precedes block tags.
- **Block tag order**: `@constructor`, `@receiver`, `@param`, `@property`, `@return`, `@throws`, `@see`. Tags never have empty descriptions. Wrapped tag lines are indented 4 spaces from the `@`.
- **Summary fragment**: a noun or verb phrase, capitalized and punctuated like a sentence, but not "A `Foo` is a...", not "This method returns...", and not an imperative sentence like "Save the record.". Write `Returns the store for the given region.`
- **KDoc is required** on every public type and every public or protected member of such a type. Exceptions: simple, obvious members like `getFoo` / `foo` with nothing more to say, and overrides. Not an exception when a reader may not know what the term means.
