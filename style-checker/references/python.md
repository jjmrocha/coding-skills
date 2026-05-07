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
- Loop counters: `i`, `j`, `k`
- Exception identifier in `except` clause: `e`
- File handle: `f`
- Private TypeVar with no constraints

**Never** use single-character names in other contexts.

### Prohibited Naming Patterns
- Dashes in module/file names (use underscores: `my_module.py` not `my-module.py`)
- `__double_underscore__` names (reserved by Python; beyond `__init__`, `__str__`, etc.)
- Names ending with type information (e.g., don't use `id_to_name_dict`)
- Offensive terms or abbreviations unfamiliar outside the project

### Required Receiver Names
- `self` is **required** as the first parameter of instance methods.
- `cls` is **required** as the first parameter of class methods.
- These names are reserved and must not be used for other identifiers.

### Acronyms
Treat as whole words in `CapWords`: `HttpServer`, `XmlParser` (not `HTTPServer`, `XMLParser`)

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
- Exceptions: long import lines, URLs in comments, string literals that can't be split, `pylint` disable comments.
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

## Imports

- `from __future__ import` statements must appear first (before any other imports).
- One import per line. Exception: `from typing import X, Y` and `from collections.abc import X, Y` are allowed.
- Import **entire modules**, not individual names. Exception: `typing`, `collections.abc`, and `typing_extensions` modules.
- **No relative imports** — always use full package paths.
- **No wildcard imports** (`from module import *` is forbidden).
- Sort order (each group separated by a blank line):
  1. `from __future__ import ...`
  2. Python standard library
  3. Third-party libraries
  4. Local/repository sub-packages
- Sort **lexicographically** within each group (case-insensitive).

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
# Wrong — importing individual names from non-typing modules
from os import path
```

---

## Strings

- Choose `'` or `"` and be **consistent within the file**.
- Use the opposite quote to avoid escaping: `"don't"` or `'say "hello"'`.
- **Docstrings**: always use `"""` triple double-quotes.
- Multi-line strings: prefer `"""` over `'''`.
- String formatting preference: f-strings > `%` > `.format()` > concatenation.

```python
# Preferred
name = f"Hello, {user.name}!"

# Docstring always uses """
def func():
    """Summary line."""
```

---

### Trailing Commas

- Recommended when the closing bracket does not appear on the same line as the final element.
- Hints auto-formatters to produce one-item-per-line formatting.

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
- **No** whitespace before `,`, `;`, or `:`.
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

```python
# Acceptable
double = lambda x: x * 2

# Prefer instead of map+lambda
result = [x * 2 for x in items]
```

### Comprehensions & Generator Expressions
- Allowed for **simple cases** where intent is clear.
- **No multiple `for` clauses** or deeply nested filters — those belong in `for` loops.
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

- Use **sparingly**; not required around tuples (except single-element tuples or empty tuples).
- Not required in `return` or `if` statements unless clarifying grouping or splitting lines.
- Acceptable for line continuation or to clarify the tuple vs. expression boundary.

```python
# Unnecessary parentheses (don't flag as violation, just note preference)
return foo
if x:

# Necessary — 1-tuple
return (value,)
```

---

## Comments & Docstrings

- All public modules, classes, functions, and methods **require docstrings**.
- Docstring first line: summary (≤80 chars). Blank line, then detailed description.
- Google-style docstring sections:

```python
def func(x, y):
    """Summary line (imperative mood).

    Args:
        x: Description of x.
        y: Description of y.

    Returns:
        Description of return value.

    Raises:
        ValueError: If x is negative.
    """
```

- Module docstring: required; include usage examples.
- Class docstring: document class-level attributes.
- Block comments: indented to same level as code, then `# ` + text.
- Inline comments: two spaces before `#`, then one space after.
- Comments explain **why**, not what. No obvious descriptions.
- `TODO` format: `# TODO: crbug.com/123456 - Description`

---

## Type Annotations

- `X | None` instead of `Optional[X]` (Python 3.10+).
- Use abstract container types: `collections.abc.Sequence` over `list`.
- Prefer built-in generics: `list[T]` over `typing.List[T]`.
- Import types from `typing` and `collections.abc` directly.
- Use `TYPE_CHECKING` block for annotation-only imports that would cause runtime cycles.
- Private TypeVar: `_T = TypeVar("_T")`.
- **Do not annotate** `self` or `cls` (unless using the `Self` type).
- **Do not annotate** `__init__` return type.
- Use `from __future__ import annotations` or quoted forward references for self-referencing types.

## Logging

- Use **pattern-string formatting** with `%`-placeholders, not f-strings:

```python
# Correct — deferred formatting
logger.info("Found %d items in %s", count, path)

# Wrong — eager evaluation
logger.info(f"Found {count} items in {path}")
```

