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
- `__double_underscore__` names (reserved by Python)
- Names ending with type information (e.g., don't use `id_to_name_dict`)
- Never use `self` or `cls` as receiver names for regular methods (those are reserved)

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

- Imports always on separate lines. Exception: `from typing import X, Y` is allowed.
- Import **entire modules**, not individual names. Exception: `from typing import ...` and `from collections.abc import ...`.
- **No relative imports** — always use full package paths.
- Order (each group separated by a blank line):
  1. `from __future__ import ...`
  2. Python standard library
  3. Third-party libraries
  4. Local/repository sub-packages
- Sort **lexicographically** within each group (case-insensitive).

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

- `X | None` instead of `Optional[X]`.
- Use abstract container types: `collections.abc.Sequence` over `list`.
- Import types from `typing` and `collections.abc` directly.
- Use `TYPE_CHECKING` block for annotation-only imports.
- Private TypeVar: `_T = TypeVar("_T")`.
