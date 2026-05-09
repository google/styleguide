# Google Python Style Guide — LLM-Optimized Compact Version

Machine-friendly reference for AI code assistants. See `pyguide.md` for full documentation.

## Language Rules

### Lint
- Run `pylint` with [pylintrc](https://google.github.io/styleguide/pylintrc)
- Suppress warnings only when inappropriate: `def foo():  # pylint: disable=invalid-name`
- Prefer `pylint: disable` over deprecated `pylint: disable-msg`

### Imports
- Use `import x` for packages/modules only
- Use `from x import y` where `x` is package prefix, `y` is module name
- Use `from x import y as z` for:
  - Conflicting `y` names
  - Too-generic names (e.g., `from storage.file_system import options as fs_options`)
  - Long names
- Use `import y as z` only for standard abbreviations (e.g., `numpy as np`)
- Use full package paths; never relative imports
- Exceptions: `typing`, `collections.abc`, `typing_extensions`, `six.moves`

### Packages
Import each module using full pathname. Example:
```python
import absl.flags              # or
from absl import flags
```

### Exceptions
- Use built-in exceptions; raise `ValueError` for API misuse
- Never use bare `except:` or catch `Exception`/`StandardError` unless re-raising or isolation needed
- Minimize code in `try` blocks
- Use `finally` for cleanup, not `__del__`
- Use `assert` only in tests, not application logic

### Mutable Global State
- Avoid mutable globals; use functions/classes to access
- Internal globals: prepend `_` (e.g., `_FOO = ...`)
- Constants: CAPS_WITH_UNDERSCORE (e.g., `MAX_SIZE = 100`)

### Nested Functions & Classes
- Fine when closing over local variables (not `self`/`cls`)
- Don't nest just to hide from module users; prefix with `_` instead

### Comprehensions & Generators
- Simple comprehensions OK; multiple `for` clauses not permitted
```python
[x for x in items if condition]  # OK
[x for x in items for y in other if x == y]  # NO
```
- Use generator expressions over `map()`/`filter()` with lambda

### Default Iterators
Use default iterators for built-in types:
```python
for key in dict: ...              # YES
for line in file: ...             # YES
for key in dict.keys(): ...       # NO
```

### Generators
- Use `yield` for memory efficiency
- Document with "Yields:" in docstring
- Wrap expensive resources with context managers (PEP-533)

### Lambda Functions
- Ok for one-liners only
- Prefer named functions for multi-line logic (60-80 char limit)
- Use `operator` module instead of lambda (e.g., `operator.mul` not `lambda x,y: x*y`)

### Conditional Expressions
```python
one_line = 'yes' if condition else 'no'  # OK
x = a if cond else b  # OK for simple cases
```

### Default Arguments
- Ok in most cases
- **Never** use mutable defaults: `[]`, `{}`, `time.time()`
```python
def foo(a, b=None):          # OK
    if b is None: b = []
def foo(a, b=[]):            # NO
```

### Properties
- Use `@property` for trivial computations only
- Avoid hiding complex operations or side effects
- Don't override in subclasses for computation

### True/False Evaluations
```python
if foo:                    # YES
if foo != []:              # NO
if not x and x is not None:  # Check None explicitly
if len(seq):               # NO; use: if seq:
```

### Lexical Scoping
OK to use. Beware of assignment gotchas in nested functions.

### Decorators
- Use judiciously for clear advantage
- Avoid `staticmethod`; write module-level functions instead
- Use `classmethod` only for named constructors or class-specific state
- Document whether it's a decorator
- Write unit tests for decorators

### Threading
- Don't rely on atomicity of built-in types
- Use `queue.Queue` for thread communication
- Use `threading` module and locks (prefer condition variables)

### Power Features
Avoid: metaclasses, bytecode manipulation, dynamic inheritance, `__del__`, custom `__getattr__`.
Exception: Standard library modules (`abc.ABCMeta`, `dataclasses`, `enum`) OK to use.

### Modern Python (__future__ imports)
Use `from __future__ import` for:
- `annotations` (for forward references)
- `generator_stop` (if supporting Python 3.5)
- Other features as appropriate

### Type Annotations
- Encouraged for public APIs
- Annotate complex or error-prone code
- Use pytype/mypy for type checking
- Include in docstrings if not in code

## Style Rules

### Semicolons
- Don't terminate lines with `;`
- Don't use `;` to put multiple statements on one line

### Line Length
- **80 character maximum**
- Exceptions: long imports, URLs, pathnames, long flags in comments
- Use implicit line joining (parentheses), not backslash
- Break at highest syntactic level

```python
# YES
foo_bar(self, width, height, color='black',
        design=None, emphasis=None)

# YES
if (width == 0 and height == 0 and
    color == 'red'):
    pass

# NO
if width == 0 and height == 0 and \
        color == 'red':
    pass
```

### Parentheses
Use sparingly in conditionals and returns:
```python
if foo: bar()  # YES
if (x): bar()  # NO
return foo     # YES
return (foo)   # NO
```

### Indentation
- **4 spaces** (never tabs)
- Implied continuation: align or 4-space hanging indent
```python
# Aligned with opening delimiter
foo = long_func(var_one, var_two,
                var_three, var_four)

# 4-space hanging indent
foo = long_func(
    var_one, var_two, var_three,
    var_four)
```

### Trailing Commas
Use after last element only if closing bracket on separate line (hints auto-formatter):
```python
# YES
items = [
    'a',
    'b',
    'c',
]

# NO
items = [
    'a',
    'b',
    'c',]
```

### Blank Lines
- 2 blank lines between top-level definitions
- 1 blank line between method definitions
- 1 blank line between docstring and first method
- No blank line after `def`

### Whitespace
- No space inside parentheses, brackets, braces: `spam(ham[1], {})`
- No space before comma/colon/semicolon; space after (except EOL)
- No space before `(` in function calls or indexing
- No trailing whitespace
- Surround binary operators with single space (`=`, `==`, `<`, `>`, comparison, boolean)
- **No** space around `=` in keyword arguments: `func(a=1)`, except with type annotation: `def foo(a: int = 0)`

```python
# YES
if x == 4: print(x, y)
x, y = y, x

# NO
if x == 4 : print(x , y)
dict ['key'] = list [index]
```

### Shebang
- Use `#!/usr/bin/env python3` (supports virtualenvs)
- Or `#!/usr/bin/python3` per PEP-394
- Only needed for executables, ignored on import

### Comments & Docstrings

**Docstrings** (always `"""`):
- Every public function, class, method
- One-line summary (≤80 chars), period/question/exclamation
- Blank line before rest if longer
- Module docstring at top

**Functions/Methods**:
```python
def fetch_rows(table_handle, keys, require_all=False):
    """One-line summary.

    Longer description if needed.

    Args:
        table_handle: Description.
        keys: Description.
        require_all: If True, [description].

    Returns:
        Description of return value.

    Raises:
        IOError: Description.
    """
```

**Classes**:
```python
class MyClass:
    """One-line summary.
    
    Longer description.
    
    Attributes:
        attr1: Description.
        attr2: Description.
    """
```

**Block/Inline Comments**:
- Explain *why*, not *what*
- Start 2+ spaces from code, `#` + space
- Capitalize, use proper grammar

### Strings
- Use f-strings, `%` operator, or `.format()`
- Don't concatenate with `+`; use `.join()` for loops
```python
# YES
x = f'name: {name}; score: {n}'
items = ['<tr>']
for name in items: items.append(f'<td>{name}</td>')
result = ''.join(items)

# NO
x = first + ', ' + second
for name in items:
    table += '<tr>' + name + '</tr>'  # Bad: quadratic
```

- Consistent quote style per file: use `'` or `"`, stick with it
- Multi-line strings: prefer `"""` over `'''`
- Use [textwrap.dedent()](https://docs.python.org/3/library/textwrap.html#textwrap.dedent) for indented strings

**Logging** (pattern-based):
```python
# YES: pattern string + args
logger.info('Version: %s', version)

# NO: f-string (prevents log aggregation)
logger.info(f'Version: {version}')
```

**Error Messages**:
- Match actual error condition
- Clearly identify interpolated pieces
- Support automated processing (grep-able)

### Files, Sockets, Resources
- Explicitly close or use context managers
- Prefer `with` statement:
```python
with open("file.txt") as f:
    for line in f: print(line)

import contextlib
with contextlib.closing(resource) as r:
    ...
```

### TODO Comments
```python
# TODO: crbug.com/192795 - Description of work.
```

### Imports Formatting
Groups (in order):
1. `from __future__ import ...`
2. Standard library
3. Third-party
4. Local repository
5. (Deprecated: same top-level subpackage)

Separate imports: `from x import y` per line, except `typing` and `collections.abc`:
```python
from collections.abc import Mapping, Sequence
from typing import Any, NewType
import os
import sys
from absl import flags
```

### Statements
One statement per line. Exception: `if test: action` OK if fits on one line:
```python
if foo: bar(foo)  # OK
```

### Getters & Setters
Use when getting/setting is complex or costly; otherwise make attribute public.
Follow naming: `get_foo()`, `set_foo()`.

### Naming

| Type | Public | Internal |
|------|--------|----------|
| Packages | `lower_with_under` | — |
| Modules | `lower_with_under` | `_lower_with_under` |
| Classes | `CapWords` | `_CapWords` |
| Functions | `lower_with_under()` | `_lower_with_under()` |
| Constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| Variables | `lower_with_under` | `_lower_with_under` |
| Parameters | `lower_with_under` | — |

**Avoid**:
- Single letters (except `i`, `j`, `k` for loops; `e` for exceptions; `f` for files; `_T` for TypeVars)
- Dashes in module names
- `__dunder__` names (reserved by Python)
- Type info in names: `id_to_name_dict` → `id_to_name`

**Math notation** exception: Use standard symbols if citing reference/paper with docstring link.

### Main
Always check `if __name__ == '__main__':` before executing:
```python
def main(argv):
    ...

if __name__ == '__main__':
    from absl import app
    app.run(main)
```

### Function Length
Prefer small, focused functions. No hard limit, but ~40 lines is guideline. If longer, consider breaking up.

## Type Annotations

### General Rules
- Annotate public APIs
- Don't annotate `self`, `cls`
- Don't annotate `__init__` return (`None` assumed)
- Use `Any` if type can't be expressed
- Annotate error-prone or hard-to-understand code

### Line Breaking
```python
def my_method(
    self,
    first_var: int,
    second_var: str,
) -> int:
    ...
```

### Forward Declarations
Use `from __future__ import annotations` or string quotes:
```python
from __future__ import annotations

class MyClass:
    def __init__(self, stack: Sequence[MyClass]) -> None: ...

# OR
class MyClass:
    def __init__(self, stack: Sequence['MyClass']) -> None: ...
```

### Default Values
Spaces around `=` only with type annotation:
```python
def func(a: int = 0): ...  # YES
def func(a: int=0): ...    # NO
def func(a=0): ...         # YES
```

### NoneType
Use explicit `X | None` or `Optional[X]`, not implicit:
```python
def modern(a: str | None) -> str: ...  # YES (Python 3.10+)
def union(a: Union[str, None]) -> str: ...  # YES
def implicit(a: str = None) -> str: ...  # NO
```

### Type Aliases
```python
from typing import TypeAlias
_MyType: TypeAlias = tuple[int, str]
PublicAlias: TypeAlias = Mapping[str, int]
```

### Ignoring Types
```python
x = foo()  # type: ignore
# pytype: disable=attribute-error
```

### Annotated Assignments
```python
a: Foo = SomeFunc()
```

### Tuples vs Lists
```python
a: list[int] = [1, 2, 3]           # Single type
b: tuple[int, ...] = (1, 2, 3)     # Variable-length
c: tuple[int, str, float] = (1, "2", 3.5)  # Fixed types
```

### Type Variables
```python
from typing import TypeVar, ParamSpec

_T = TypeVar("_T")  # Generic
_P = ParamSpec("_P")  # For callables
AddableType = TypeVar("AddableType", int, float, str)  # Constrained

def next(l: list[_T]) -> _T:
    return l.pop()
```

### String Types
Use `str` for text, `bytes` for binary. Use `AnyStr` if always same type.

### Imports for Typing
```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING
```

Use abstract types (`collections.abc.Sequence`) over concrete (`typing.List`):
```python
# YES
def transform(items: Sequence[int]) -> Sequence[int]: ...

# NO
def transform(items: List[int]) -> List[int]: ...
```

### Conditional Imports
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import expensive_module

def func(x: "expensive_module.Type") -> None: ...
```

### Circular Dependencies
Avoid via refactoring. If unavoidable, use `Any`:
```python
from typing import Any

some_mod = Any  # some_mod.py imports this
def foo(x: "some_mod.Type") -> None: ...
```

### Generics
Always specify type parameters:
```python
# YES
def get_names(ids: Sequence[int]) -> Mapping[int, str]: ...

# NO (interpreted as Any)
def get_names(ids: Sequence) -> Mapping: ...
```

## Summary
- Be consistent
- Follow local style conventions
- Prioritize readability
- Use tools (Black, Pyink, pylint, pytype) for enforcement
