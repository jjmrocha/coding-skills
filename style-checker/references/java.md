# Google Java Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/javaguide.html

Examples in the guide are non-normative: optional formatting choices shown in them are not rules.

## Source File Basics

- **Exactly one top-level class per file** (§3.4.1).
- **File name = top-level class name** + `.java` (case-sensitive). `MyClass` lives in `MyClass.java`.
- Encoding: **UTF-8**.
- Whitespace: the **only** ASCII whitespace character is the space (0x20) — tabs are forbidden for indentation, and other whitespace characters are escaped inside literals and text blocks.
- Use **special escape sequences** (`\b`, `\t`, `\n`, `\f`, `\r`, `\s`, `\"`, `\'`, `\\`) over octal (`\012`) or Unicode (`\u000a`) escapes for the same character.
- Other non-ASCII characters: use the real character or a Unicode escape, whichever is easier to read. Unicode escapes outside string literals and comments are strongly discouraged.
- File sections in order, exactly one blank line between each present section: license/copyright → `package` → imports → exactly one top-level class.
- **Every file has a `package` declaration** (except `module-info.java`). Compact source files are not used.
- The `package` line is never wrapped; the column limit does not apply to it.

### Class Contents
- Members follow **some logical order** the maintainer could explain. Not "new methods appended at the end".
- **Overloads are never split**: methods with the same name (and all constructors) form one contiguous group, even when their modifiers differ.

---

## Naming Conventions

Identifiers use only ASCII letters and digits (plus underscores in the few cases below).

| Identifier | Style | Example |
|-----------|-------|---------|
| Package / module | `lowercase`, words concatenated, no underscores | `com.example.deepspace` (not `deepSpace`, `deep_space`) |
| Class / Interface / Enum / Record / Annotation | `UpperCamelCase` | `MyClass`, `ImmutableList` |
| Test class | `UpperCamelCase` ending in `Test` | `HashImplTest` |
| Method | `lowerCamelCase` | `sendMessage`, `stop` |
| JUnit test method (allowed exception) | `lowerCamelCase` components joined by underscores | `transferMoney_deductsFromSource` |
| Constant (`static final`, deeply immutable) | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `EMPTY_ARRAY` |
| Non-constant field (static or not) | `lowerCamelCase` | `computedValues` |
| Local variable (even if `final`) | `lowerCamelCase` | `count`, `itemList` |
| Parameter | `lowerCamelCase` | `userName` |
| Type parameter | Single capital letter, optionally + one digit, **or** class-style name + `T` | `E`, `T`, `T2`, `RequestT` |

**Avoid**: Hungarian notation, underscores in class/method names (except JUnit tests), and special prefixes/suffixes (`mName`, `s_name`, `kName`, `name_`).

**Parameters**: avoid one-character parameter names in public methods.

**Constant definition**: A field is a constant only if it is `static`, `final`, and its content is **deeply immutable** with no detectable side effects. Merely intending never to mutate it is not enough.

```java
// Constants
static final int NUMBER = 5;
static final ImmutableList<String> NAMES = ImmutableList.of("Ed", "Ann");
static final Joiner COMMA_JOINER = Joiner.on(',');  // Joiner is immutable
static final SomeMutableType[] EMPTY_ARRAY = {};

// Not constants — use lowerCamelCase
static final Set<String> mutableCollection = new HashSet<String>();
static final Logger logger = Logger.getLogger(MyClass.getName());
static final String[] nonEmptyArray = {"these", "can", "change"};
```

**Local variables** are never styled as constants, even when `final` and immutable.

### CamelCase Conversion Algorithm
1. Convert to plain ASCII, remove apostrophes ("Müller's" → "Muellers").
2. Split on spaces and remaining punctuation. Recommended: split words that already look camel-cased ("AdWords" → "ad words").
3. Lowercase everything (including acronyms), then uppercase the first letter of each word (of each word except the first for lowerCamelCase).
4. Join into a single identifier. Underscores may separate adjacent numbers (`guava33_4_6`).

| Prose form | Correct | Incorrect |
|-----------|---------|-----------|
| "XML HTTP request" | `XmlHttpRequest` | `XMLHTTPRequest` |
| "new customer ID" | `newCustomerId` | `newCustomerID` |
| "inner stopwatch" | `innerStopwatch` | `innerStopWatch` |
| "supports IPv6 on iOS?" | `supportsIpv6OnIos` | `supportsIPv6OnIOS` |
| "Turn on 2SV" | `turnOn2sv` | `turnOn2Sv` |

`YoutubeImporter` is acceptable but not recommended (`YouTubeImporter`). Ambiguously hyphenated words allow both forms (`checkNonempty`, `checkNonEmpty`).

---

## Indentation

- **+2 spaces** per block level, for code and comments. **Never tabs.**
- Continuation lines: at least **+4 spaces** from the original line.
- Multiple continuation lines use the same indentation if and only if they begin with syntactically parallel elements.

---

## Line Length

- **100 characters** maximum. Each Unicode code point counts as one character.
- Exceptions: `package` and `import` statements; lines where the limit cannot be obeyed (a long URL in Javadoc); text block contents; shell command lines in comments; rare very long identifiers.

### Line-Wrapping Rules
- Break at **higher syntactic levels** when possible.
- Non-assignment operators: break **before** the symbol. This also applies to `.`, `::`, `&` in type bounds, and `|` in catch blocks.
- Assignment operators (and the `:` of an enhanced `for`): break typically **after** the symbol, but either way is acceptable.
- Method/constructor/record name stays attached to `(`.
- Comma stays attached to preceding token.
- Never break next to the `->` of a lambda or switch rule, except right after it when a single unbraced expression follows.

```java
Predicate<String> predicate = str ->
    longExpressionInvolving(str);
```

---

## Braces (K&R Style)

- Braces are **always required** for `if`, `else`, `for`, `do`, `while` — even for empty or single-statement bodies. Other optional braces (lambdas) stay optional.
- No line break **before** `{`. Line break **after** `{` and **before** `}`.
- Line break after `}` only if it ends a statement or the body of a method, constructor, or named class — not before `else`, `catch`, or a comma.
- Empty blocks: `{}` is fine, but **not** in multi-block statements (`if/else`, `try/catch/finally`).

```java
// Correct
if (condition) {
  doSomething();
} else {
  doOther();
}

void doNothing() {}

// Wrong — missing braces
if (condition)
  doSomething();

// Wrong — concise empty block in a multi-block statement
try {
  doSomething();
} catch (Exception e) {}
```

---

## Imports

- **No wildcard imports**, static or not (`import java.util.*` is forbidden).
- **No module imports** (`import module java.base;`).
- Static imports are NOT used for static nested classes.
- Not line-wrapped (column limit does not apply to imports).
- Order:
  1. All static imports in one group
  2. All non-static imports in one group
- One blank line between the two groups; **no other blank lines** between imports.
- Within each group, imported names in ASCII sort order.

---

## Blank Lines (Vertical Whitespace)

- Exactly **one blank line** between consecutive class members (fields, constructors, methods, nested classes, static/instance initializers).
- Optional blank line between consecutive fields (for logical grouping).
- One blank line between source file sections (license, package, imports, class declaration).
- A blank line before the first or after the last member is neither encouraged nor discouraged.
- Multiple consecutive blank lines are permitted but never required or encouraged.

---

## Horizontal Whitespace

**Required single spaces:**
- Between a keyword (`if`, `for`, `catch`) and a following `(`.
- Between `}` and a following keyword (`else`, `catch`).
- Before `{`, except `@SomeAnnotation({a, b})` and `{{"foo"}}`.
- On both sides of binary and ternary operators, `&` in type bounds, `|` in multi-catch, `:` in enhanced for, and `->` in lambdas and switch rules.
- After `,`, `:`, `;`, and the `)` of a cast.
- Before `//` and between `//` and comment text (multiple spaces allowed).
- Between the type and identifier of a declaration: `List<String> list`.

**Prohibited spaces:**
- No space around `::` (method reference) or `.` (field/method access).

**Optional:** spaces just inside array-initializer braces: `new int[] {5, 6}` and `new int[] { 5, 6 }` are both valid.

**Horizontal alignment** (extra spaces to line tokens up with previous lines) is **permitted but never required**. Do not flag it. Do not flag lines that were left unaligned after an edit either.

---

## Statements

- **One statement per line.**
- **One variable per declaration** (`int a; int b;` not `int a, b;`).
  - Exception: multiple variables allowed in `for` loop header.
- Declare local variables **close to their first use**, not at block start.
- Typically initialize variables at declaration.
- **Grouping parentheses are recommended**. Omit them only when no reader could misread the code without them.

---

## Modifiers Ordering

```
public protected private abstract default static final sealed non-sealed
transient volatile synchronized native strictfp
```

Modifiers on `requires` module directives: `transitive static`.

---

## Text Blocks

- The opening `"""` is **always on a new line**. That line follows normal indentation, or starts at the left margin.
- The closing `"""` is on a new line with the same indentation as the opening, and may be followed by more code.
- Each content line is indented at least as much as the opening and closing `"""`.
- Contents may exceed the 100-character column limit.

```java
String sql =
    """
    SELECT id, name
    FROM users
    WHERE active = true
    """;
```

---

## Unnamed Variables (`_`)

- `_` is allowed wherever applicable (Java 22+).
- Use for unused parameters, catch parameters, or lambda parameters.

```java
Predicate<String> alwaysTrue = _ -> true;
try {
  return handleNumericResponse(Integer.parseInt(response));
} catch (NumberFormatException _) {
  // it's not numeric; that's fine, just continue
}
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

- Class/package/module annotations: immediately after documentation block, **one per line**, no extra indentation.
- Method/constructor annotations: same; a single parameterless annotation may share the first signature line: `@Override public int hashCode() {`.
- Field annotations: multiple may appear on the same line: `@Partial @Mock DataLoader loader;`.
- Parameter and local variable annotations: no specific rules.
- **Type-use annotations** (meta-annotated with `@Target(ElementType.TYPE_USE)`): appear immediately before the annotated type: `public @Nullable Person find(String name);`.

---

## Enum Classes

- Line break after the comma between constants is optional; blank lines between constants are allowed.
- Simple enums with no methods and no documentation on constants may be formatted like an array initializer: `private enum Suit { CLUBS, HEARTS, SPADES, DIAMONDS }`.
- Enums with methods follow class formatting rules.

---

## Switch Statements & Expressions

- Switch labels indented **+2** from `switch`.
- Old-style (`:`): line break after each label's colon; statements indented a further +2.
- Old-style fall-through: each statement group ends abruptly (`break`, `continue`, `return`, throw) or is marked with a comment such as `// fall through`. Not needed after the last group or between consecutive labels.
- New-style (`->`): a rule may sit on one line if it fits the column limit. A non-empty block requires a line break after `{`. Continuation lines indent +4.
- **Every switch must be exhaustive**, even when the language does not require it: add `default` (possibly empty) or cover all enum values.
- **Switch expressions must be new-style.**

```java
switch (number) {
  case 0, 1 -> handleZeroOrOne();
  case 2 ->
      handleTwoWithAnExtremelyLongMethodCallThatWouldNotFitOnTheSameLine();
  default -> {
    logger.atInfo().log("Surprising number %s", number);
    handleSurprisingNumber(number);
  }
}
```

---

## Comments & Javadoc

### Implementation Comments
- Block comments are indented like the surrounding code, in `/* ... */` or `// ...` style. Continuation lines of `/* */` start with `*` aligned with the `*` above.
- **No boxes** drawn with asterisks or other characters.
- `TODO` format: `// TODO: crbug.com/12345678 - Explanation`. The link is ideally a bug. Do not name a person or team as the context (`// TODO: @username - ...`).

### Javadoc Format
- Both **Markdown Javadoc** (`///`) and traditional Javadoc (`/** ... */`) are acceptable.
- Single-line form `/** Short text. */` only when the whole block fits on one line and has no block tags.
- Traditional: a line with only `*` separates paragraphs and precedes block tags. Each paragraph after the first starts with `<p>` immediately before the first word, no space after. Markdown: a blank `///` line separates paragraphs, no `<p>`.
- Block tag order: `@param`, `@return`, `@throws`, `@deprecated`. These **never** have an empty description. Continuation lines: +4 or more from the `@` (traditional), exactly +2 (Markdown).

### Summary Fragment
- A noun phrase or verb phrase, **not a complete sentence**, but capitalized and punctuated like one.
- Correct: `Returns the customer ID.` or `{@return the customer ID}`.
- Wrong: `@return the customer ID.` as the whole Javadoc; `This method returns...`; `A {@code Foo} is a...`; an imperative sentence such as `Save the record.`

### Where Javadoc Is Required
- Every **visible** class, member, and record component: a public top-level class, and public or protected members of a visible class.
- Optional for simple, obvious members such as `getFoo()` when there is truly nothing more to say than "the foo". Not optional when a reader may not know what a term means.
- Not always present on methods that override a supertype method.
- A comment that describes the overall purpose of a class or member is written as Javadoc, not as an implementation comment.

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

- Always use `@Override` when legal, including interface implementations and explicit record accessors (except when the parent method is `@Deprecated`).
- Qualify static member access with **class name**, not instance: `Foo.staticMethod()`, not `foo.staticMethod()`.
- Do not override `Object.finalize`.
- Caught exceptions are not ignored: log, rethrow (for example as `AssertionError`), or explain in a comment why no action is correct.
