# Google Python Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/pyguide.html

## Naming Conventions

| Identifier | Style | Example |
|-----------|-------|---------|
| Package | `lower_with_under` | `my_package` |
| Module/file | `lower_with_under` | `my_module.py` |
| Internal module | `_lower_with_under` | `_helpers.py` |
| Class (public) | `CapWords` | `MyClass` |
| Class (internal) | `_CapWords` | `_InternalHelper` |
| Exception | `CapWords` ending in `Error` | `ValueError`, `MyError` |
| Function/method (public) | `lower_with_under()` | `my_function()` |
| Function/method (internal) | `_lower_with_under()` | `_helper()` |
| Variable (global/class/instance) | `lower_with_under` | `my_variable` |
| Variable (protected) | `_lower_with_under` | `_protected` |
| Constant (public) | `CAPS_WITH_UNDER` | `MAX_SIZE` |
| Constant (internal) | `_CAPS_WITH_UNDER` | `_MAX_SIZE` |
| Parameter | `lower_with_under` | `my_param` |
| Local variable | `lower_with_under` | `count` |
| Type alias (public) | `CapWords` | `MyType` |
| Type alias (internal) | `_CapWords` | `_InternalType` |
| Type variable | Descriptive `CapWords` or short `T`/`KT`/`VT` | `AnyStr`, `T` |

### Single-Character Names
Allowed **only** for:
- Loop counters and iterators: `i`, `j`, `k`, `v`
- Exception identifier in `except` clause: `e`
- File handle in a `with` statement: `f`
- Private TypeVar or ParamSpec with no constraints: `_T`, `_P`
- Names that match established notation in a reference paper or algorithm

**Never** use single-character names in other contexts. A name's descriptiveness should grow with its scope: `i` is fine in a 5-line block, too vague across nested scopes.

### Prohibited Naming Patterns
- Dashes in module/file names (use underscores: `my_module.py` not `my-module.py`)
- `__double_underscore__` names (reserved by Python; beyond `__init__`, `__str__`, etc.)
- Names ending with type information (e.g., don't use `id_to_name_dict`)
- Offensive terms or abbreviations unfamiliar outside the project
- Abbreviations made by deleting letters within a word
- Leading double underscore (`__private`) for name mangling — discouraged; use a single underscore

### Required Receiver Names
- `self` is **required** as the first parameter of instance methods.
- `cls` is **required** as the first parameter of class methods.
- These names are reserved and must not be used for other identifiers.

### Acronyms
Follow PEP 8: in `CapWords`, capitalize every letter of an acronym: `HTTPServerError`, `XMLParser` (not `HttpServerError`). In `lower_with_under` names, acronyms are lowercase: `send_acronym_via_https`.

---

## Indentation

- **4 spaces** per level. **Never tabs.**
- Continuation lines: align with opening delimiter OR use 4-space hanging indent.
- Closing brackets: either aligned with first non-whitespace of last element, or with opening line.

```python
# Aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Hanging 4-space indent
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

---

## Line Length

- **80 characters** maximum.
- Exceptions: long import statements; URLs, pathnames, or long flags in comments; long module-level string constants without whitespace (URLs, pathnames); `pylint` disable comments.
- Docstring summary lines must always stay within 80 characters.
- Any other line may exceed 80 characters only when the Black or Pyink formatter cannot bring it under the limit.
- Prefer breaking at the highest syntactic level. Put a long URL in a comment on its own line rather than splitting it.
- **Never use backslash** for explicit line continuation — use implicit joining inside `()`, `[]`, or `{}`.

```python
# Correct — implicit joining
result = (some_long_variable + another_variable
          + third_variable)

# Wrong — backslash continuation
result = some_long_variable + another_variable \
         + third_variable
```

---

## Shebang

- A shebang line (`#!/usr/bin/env python3` or `#!/usr/bin/python3`) belongs **only** on the main executable file that is run directly — not on imported library modules.

---

## Imports

- `from __future__ import` statements must appear first (before any other imports).
- One import per line. Exception: `from typing import X, Y` and `from collections.abc import X, Y` are allowed.
- Use `import x` for packages and modules. Use `from x import y` only when `y` is a module and `x` is its package. Never import a class or function by name. Exception: symbols from `typing`, `collections.abc`, and `typing_extensions` are imported directly.
- **No relative imports** — always use full package paths.
- **No wildcard imports** (`from module import *` is forbidden).
- Imports go at the top of the file, after the module docstring and before globals and constants.
- Sort order (a blank line between groups is optional):
  1. `from __future__ import ...`
  2. Python standard library
  3. Third-party libraries
  4. Local/repository sub-packages
- Sort **lexicographically** within each group (case-insensitive), by the module's full package path (the `path` in `from path import ...`).

### Import Aliases (`as`)

Use `from x import y as z` when:
- Two modules named `y` exist, or
- `y` conflicts with a top-level or parameter name, or
- `y` is inconveniently long or too generic.

Use `import y as z` only when `z` is a standard abbreviation (e.g., `numpy as np`, `pandas as pd`).

```python
# Correct
import numpy as np
from os import path as os_path  # avoid shadowing

# Wrong — unnecessary aliasing
import mylongmodulename as m  # not standard
```

```python
# Correct
import os
import sys

import third_party_lib

from myproject import my_module

# Wrong — relative import
from . import module
# Wrong — importing a class by name instead of its module
from collections import OrderedDict
```

---

## Strings

- Choose `'` or `"` and be **consistent within the file**.
- Use the opposite quote to avoid escaping: `"don't"` or `'say "hello"'`.
- **Docstrings**: always use `"""` triple double-quotes.
- Multi-line strings: prefer `"""` over `'''`.
- Use an f-string, the `%` operator, or `.format()` to format strings. Google does not rank them. A single join with `+` is fine, but **do not format with `+`**.
- Do not accumulate a string with `+` or `+=` in a loop. Append to a list and `''.join()` it, or write to an `io.StringIO`.
- Multi-line strings do not follow code indentation. To avoid embedded leading spaces, use concatenated single-line strings or `textwrap.dedent()`.

```python
# Correct
name = f"Hello, {user.name}!"
pair = first + second  # a single join is fine

# Wrong — formatting with +
message = "name: " + name + "; score: " + str(n)

# Docstring always uses """
def func():
    """Summary line."""
```

---

### Trailing Commas

- Recommended only when the closing bracket does not appear on the same line as the final element, and for single-element tuples.
- Hints auto-formatters to produce one-item-per-line formatting.
- Wrong: a trailing comma followed by the closing bracket on the same line as the last element of a multi-line list (`    6,]`).

```python
# Correct — trailing comma triggers multi-line formatting
result = solve(
    x,
    y,
)
```

---

## Blank Lines

- **2 blank lines** between top-level definitions (functions, classes).
- **1 blank line** between method definitions inside a class.
- **1 blank line** after class docstring before first method.
- No blank line immediately after `def` line.

---

## Whitespace in Expressions

- **No** whitespace inside `()`, `[]`, `{}`: `spam(ham[1], {'eggs': 2})`.
- **No** whitespace before `,`, `;`, or `:`. **One space** after them, except at the end of a line.
- **No** whitespace before `(` in function calls or indexing: `spam(1)`, `list[0]`.
- **No** trailing whitespace.
- **No** vertical alignment of tokens across consecutive lines.
- **Space** around binary operators (`=`, `==`, `<`, `>`, `!=`, `in`, `not in`, `is`, `is not`, `and`, `or`, `not`).
- **Judgement call** for arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`, `@`): use your discretion, but be consistent within the file.
- **No space** around `=` for keyword arguments or default parameters — **unless** a type annotation is present:

```python
# No annotation → no spaces around =
def func(a=0, b=''):

# Type annotation → spaces around =
def func(a: int = 0, b: str = ''):
```

---

## Semicolons & Statements

- **No semicolons** at end of lines.
- **One statement per line.** Never two statements on the same line.
- Exception: `if foo: bar(foo)` may be written on one line only if the entire statement fits on one line and has no `else`.
- Never on one line for `try`/`except`.

---

## Lambdas & Comprehensions

### Lambdas
- Allowed **only for one-liners**; keep under 60–80 characters.
- Prefer generator expressions or list comprehensions over `map()` / `filter()` with lambda.
- If a lambda exceeds one line, refactor it into a named `def`.
- For common operations, use the `operator` module instead of a lambda: `operator.mul`, not `lambda x, y: x * y`.

```python
# Acceptable
double = lambda x: x * 2

# Prefer instead of map+lambda
result = [x * 2 for x in items]
```

### Comprehensions & Generator Expressions
- Allowed for **simple cases** where intent is clear.
- **No multiple `for` clauses** and no multiple filter expressions — those belong in `for` loops.
- Optimize for **readability** over conciseness.
- Generator expressions acceptable as single function arguments.

```python
# Acceptable — simple comprehension
squares = [x**2 for x in range(10)]

# Too complex — refactor to a loop
result = [f(x) for x in data if cond(x) for y in x.children if y.active]
```

---

## Parentheses

- Use **sparingly**. Parentheses around tuples are fine but not required.
- **Do not** use them in `return` statements or conditions (`if`, `while`, `not`), unless they wrap a line continuation or mark a tuple.

```python
# Correct
if x:
return foo
return (spam, beans)
onesie = (foo,)

# Wrong
if (x):
if not(x):
return (foo)
```

---

## Comments & Docstrings

- A function or method **requires a docstring** when it is part of the public API, has nontrivial size, or has non-obvious logic.
- No docstring is required on test modules, on `unittest.TestCase` subclasses, or on their `test_` methods. A docstring that only repeats the name should be omitted.
- A method decorated with `@override` needs no docstring unless it changes the base contract. Without `@override`, an overriding method needs one. `"""See base class."""` is not useful.
- Docstring first line: a summary of at most 80 characters that ends with a period, question mark, or exclamation point. Then a blank line, then the detailed description.
- The summary may be descriptive (`"""Fetches rows."""`) or imperative (`"""Fetch rows."""`), but one file must use one style. A `@property` docstring describes the value like an attribute: `"""The Bigtable path."""`, not `"""Returns the Bigtable path."""`.
- Section bodies (`Args:`, `Returns:` or `Yields:`, `Raises:`) use a hanging indent of 2 or 4 spaces, consistent within the file. `Returns:` may be omitted when the function returns only `None`, or when the summary starts with "Returns" and fully describes the value.
- Google-style docstring sections:

```python
def func(x, y):
    """Summary line ending with a period.

    Args:
        x: Description of x.
        y: Description of y.

    Returns:
        Description of return value.

    Raises:
        ValueError: If x is negative.
    """
```

- Every file starts with license boilerplate, then a module docstring describing its contents and usage. Usage examples are optional.
- Class docstring: the summary says what an instance represents (`"""The address of a cheese shop."""`), not `"""Class that describes..."""`. An exception says what it represents, not when it is raised. Public attributes, except properties, go in an `Attributes:` section.
- Block comments: indented to same level as code, then `# ` + text.
- Inline comments: two spaces before `#`, then one space after.
- Comments explain **why**, not what. No obvious descriptions.
- `TODO` format: `# TODO(crbug.com/123456): Description`. The parentheses hold a link to the context, ideally a bug. The old form `# TODO: crbug.com/123456 - Description` is discouraged in new code. Do not name a person or team as the context, as in `# TODO(@username): ...`.

---

## Type Annotations

- `X | None` is recommended in new code; `Optional[X]` is still allowed.
- A parameter that can be `None` must say so in its type. Wrong: `def f(a: str = None)`. Correct: `def f(a: str | None = None)`.
- Type aliases use `CapWords` (`_Private` when module-only) and are annotated with `TypeAlias`: `_LossAndGradient: TypeAlias = tuple[Tensor, Tensor]`.
- Names imported from `typing` or `collections.abc` are treated like keywords: do not define them in your code. On a collision, use `from typing import Any as AnyType`.
- Use abstract container types: `collections.abc.Sequence` over `list`.
- Prefer built-in generics: `list[T]` over `typing.List[T]`.
- Import types from `typing` and `collections.abc` directly.
- Use `TYPE_CHECKING` block for annotation-only imports that would cause runtime cycles.
- Private TypeVar: `_T = TypeVar("_T")`.
- Annotating `self`, `cls`, or the `__init__` return type is not necessary. Do not flag it when present. Use `Self` when the type matters.
- Not every function must be annotated. At least the public API should be.
- Use `from __future__ import annotations` or quoted forward references for self-referencing types.
- **Line-wrapping long annotated signatures**: prefer one parameter per line; a trailing comma after the last parameter pushes the return type onto its own line. Break between parameters, never between a parameter name and its type.

```python
def long_function_name(
    var_one: int,
    var_two: str,
) -> ReturnType:
    ...
```

## Logging

- Use **pattern-string formatting** with `%`-placeholders, not f-strings:

```python
# Correct — deferred formatting
logger.info("Found %d items in %s", count, path)

# Wrong — eager evaluation
logger.info(f"Found {count} items in {path}")
```

