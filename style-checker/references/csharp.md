# Google C# Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/csharpguide.html

Google's C# style follows Microsoft's naming guidelines, but its formatting follows Google Java and C++ style. Where Google and Microsoft defaults differ, **Google wins**: 2-space indentation, opening braces on the same line, a 100-column limit, and `_camelCase` for every non-public field, including `const` ones.

## Naming Conventions

| Identifier | Style | Example |
|-----------|-------|---------|
| Class, struct, enum, enum member, delegate, event | `PascalCase` | `OrderBook`, `Status.Open` |
| Method | `PascalCase` | `CalculateValue()` |
| Namespace | `PascalCase` | `Shop.Orders` |
| Public field, public property | `PascalCase` | `public int Count;` |
| Private, protected, internal, protected internal field **or property** | `_camelCase` | `_results`, `_someTable` |
| Local variable, parameter | `camelCase` | `resultValue`, `mulNumber` |
| Interface | `I` + `PascalCase` | `IMyInterface` |
| File and directory names | `PascalCase` | `MyFile.cs` |

### Naming Rules
- **Modifiers do not change naming.** `const`, `static`, and `readonly` follow the same rule as any other field of that visibility:
  - `private const int _bar = 100;` is correct. `private const int Bar` and `private const int BAR` are wrong.
  - `public static int NumTimesCalled` is correct (public, so PascalCase).
- An acronym is one word: `MyRpc`, `ParseJson`, not `MyRPC`, `ParseJSON`.
- No Hungarian or `m_` prefixes (`m_total` is wrong; use `_total`).
- The file name matches the main class where possible (`MyClass.cs`). Prefer one core class per file. Report extra types in a file as Low.

---

## Organization

### `using` Directives
- At the **top of the file, before any namespace**, never inside a namespace.
- `System` imports first, then all others in alphabetical order.

```csharp
using System;
using System.Collections.Generic;
using Newtonsoft.Json;
```

### Modifier Order
```
public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async
```
`static public` is wrong; write `public static`.

### Class Member Order
Groups, in order:
1. Nested classes, enums, delegates, and events
2. Static, const, and readonly fields
3. Fields and properties
4. Constructors and finalizers
5. Methods

Within each group: public, internal, protected internal, protected, private. Group interface implementations together where possible.

---

## Whitespace and Formatting

- **2 spaces** per indentation level. **No tabs.**
- **Namespace contents are indented** one level (unlike Google C++).
- Column limit: **100**.
- **No line break before an opening brace** (`public class Foo {`). Allman style (brace on its own line) is wrong.
- **No line break between `}` and `else`**: `} else {`.
- **Braces are used even when optional**, for every `if`, `else`, `for`, `foreach`, `while`.
- Empty blocks may be concise: `void DoNothing() {}`.
- At most **one statement per line** and **one assignment per statement** (`a = b = 0;` is wrong).
- A space after `if`, `for`, `while`, `foreach`, `switch`, and after commas.
- **No space after `(` or before `)`**: `Foo(text)`, not `Foo( text )`.
- No space between a unary operator and its operand; one space on each side of every other operator.

### Line Wrapping
- Continuation lines are indented **4 spaces**.
- Line breaks inside braces (collection initializers, object initializers, lambda bodies) are not continuations: their contents are indented **2 spaces**.
- Wrapped arguments of a call or definition align with the first argument. If that does not fit, put all arguments on the next line with a 4-space indent.
- A multi-line lambda's closing brace aligns with the first character of the line that holds the opening brace. A lambda that starts after a continuation break has its whole body indented.

```csharp
namespace MyNamespace {
  public class MyClass {
    private const int _bar = 100;
    private int[] _someTable = {
      2, 3, 4,
    };

    public int CalculateValue(int mulNumber) {
      var resultValue = Foo * mulNumber;
      if (resultValue < 0) {
        _results.NumNegativeResults++;
      } else if (resultValue > 0) {
        _results.NumPositiveResults++;
      }
      return resultValue;
    }

    void AnotherLongFunctionName(
        int longArgumentName, int longArgumentName2) {}
  }
}
```

---

## Attributes

- An attribute goes on **its own line above** the field, property, or method: `[Obsolete] public void Reset()` on one line is wrong.
- **One attribute per line**: `[Serializable, Obsolete]` is wrong; write `[Serializable]` and `[Obsolete]` on separate lines.

---

## Coding Guidelines

### Constants and Fields
- Anything that can be `const` is `const`; otherwise consider `readonly`.
- Prefer named constants to magic numbers.
- **Field initializers are encouraged**, including initializing to a default value.

### Properties and Expression Bodies
- Single-line read-only properties: prefer an expression body: `int SomeProperty => _someProperty;`.
- Everything else uses `{ get; set; }`.
- Expression-bodied methods only for single statements, such as forwarding or throwing: `void M() => throw new NotImplementedException();`.

### `var`
- **Encouraged** when the type is obvious (`var apple = new Apple();`, `var request = Factory.Create<HttpRequest>();`) or for transient values passed straight to another method.
- **Discouraged** with basic types (`var success = true;`), with compiler-resolved numeric types (`var number = 12 * ReturnsFloat();`), and when the reader benefits from seeing the type (`var listOfItems = GetList();`). Report as Low.

### Parameters
- Use `out` for extra results that are not inputs. **`out` parameters come after all other parameters.**
- Use `ref` rarely, only when an input must be mutated or replaced. Not as an optimization for structs, and not to pass a container to be modified.
- Non-obvious arguments: prefer named constants, an `enum` instead of a `bool`, an options class, or named arguments (`completionDelegate: null`).

### Delegates and Events
- Call a delegate with `Invoke()` and the null-conditional operator: `SomeDelegate?.Invoke();`, not `SomeDelegate();`.

### Other Guidance (Report as Low)
- Almost always use a class; use a struct only for small, short-lived value-like types.
- A non-trivial or reused lambda should be a named method.
- Use extension methods only when the original source is unavailable or cannot be changed, and only for core features.
- Prefer single-line LINQ and imperative code over long LINQ chains. Prefer method syntax (`list.Where(...)`) over SQL-style keywords. Avoid `ForEach(...)` for more than one statement.
- Prefer `List<>` over arrays for public variables, properties, and return types; arrays for fixed sizes and multidimensional data.
- Parameters: declare the most restrictive type needed (`IReadOnlyCollection`). Returned containers that pass ownership: prefer `IList` over `List`.
- Prefer a named class over `Tuple<>` as a return type. Do not alias long type names with `using`.
- Object initializer syntax only for plain data types, not for types with constructors. Multi-line initializers are indented one block level.
- Namespaces are at most 2 levels deep. Do not force folder layout to match namespaces.
- For struct results, prefer a `bool` success value with an `out` struct over nullable structs.
- To remove items while iterating, use `RemoveAll(predicate)`, or build a new container.

---

## Comments

- Every non-obvious class has a comment saying what it is for and how to use it.
- Almost every method has a comment before it, written with an implied subject of "This method": **"Opens the file."**, not "Open the file.". Omit it only for simple, obvious methods such as accessors.
- Mention inputs and outputs (argument names in backticks), whether arguments are retained or may be null, and performance implications.
- Overrides document only what differs. Constructor comments that only say "creates this object" are not useful.
- Class members with invariants not clear from type and name are commented.
- Tricky code blocks have a comment before them.
