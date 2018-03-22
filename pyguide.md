<!--
AUTHORS:
Prefer only GitHub-flavored Markdown in external text.
See README.md for details.
-->

# Google Python Style Guide


<a id="background"></a>
## 1 Background

Python is the main dynamic language used at Google. This style guide is a list
of *dos and don'ts* for Python programs.

To help you format code correctly, we've created a [settings file for
Vim](google_python_style.vim). For Emacs, the default settings should be fine.

Many teams use the [yapf](https://github.com/google/yapf/)
auto-formatter to avoid arguing over formatting.


<a id="s2-python-language-rules"></a>
<a id="python-language-rules"></a>
## 2 Python Language Rules

<a id="s2.1-lint"></a>
<a id="lint"></a>
### 2.1 Lint

Run `pylint` over your code.

<a id="s2.1.1-definition"></a>
#### 2.1.1 Definition

`pylint` is a tool for finding bugs and style problems in Python source
code. It finds problems that are typically caught by a compiler for less dynamic
languages like C and C++. Because of the dynamic nature of Python, some
warnings may be incorrect; however, spurious warnings should be fairly
infrequent.

<a id="s2.1.2-pros"></a>
#### 2.1.2 Pros

Catches easy-to-miss errors like typos, using-vars-before-assignment, etc.

<a id="s2.1.3-cons"></a>
#### 2.1.3 Cons

`pylint` isn't perfect. To take advantage of it, we'll need to sometimes: a)
Write around it b) Suppress its warnings or c) Improve it.

<a id="s2.1.4-decision"></a>
#### 2.1.4 Decision

Make sure you run `pylint` on your code.


Suppress warnings if they are inappropriate so that other issues are not hidden.
To suppress warnings, you can set a line-level comment:

```python {.good}
dict = 'something awful'  # Bad Idea... pylint: disable=redefined-builtin
```

`pylint` warnings are each identified by symbolic name (`empty-docstring`)
Google-specific warnings start with `g-`.

If the reason for the suppression is not clear from the symbolic name, add an
explanation.

Suppressing in this way has the advantage that we can easily search for
suppressions and revisit them.

You can get a list of `pylint` warnings by doing:

```shell
pylint --list-msgs
```

To get more information on a particular message, use:

```shell
pylint --help-msg=C6409
```

Prefer `pylint: disable` to the deprecated older form `pylint: disable-msg`.

Unused argument warnings can be suppressed by deleting the variables at the
beginning of the function. Always include a comment explaining why you are
deleting it. "Unused." is sufficient. For example:

```python {.good}
def viking_cafe_order(spam, beans, eggs=None):
    del beans, eggs  # Unused by vikings.
    return spam + spam + spam
```

Other common forms of suppressing this warning include using '`_`' as the
identifier for the unused argument, prefixing the argument name with
'`unused_`', or assigning them to '`_`'. These forms are allowed but no longer
encouraged. The first two break callers that pass arguments by name, while the
latter does not enforce that the arguments are actually unused.

<a id="s2.2-imports"></a>
<a id="imports"></a>
### 2.2 Imports

Use `import`s for packages and modules only, not for individual classes or
functions.

<a id="s2.2.1-definition"></a>
#### 2.2.1 Definition

Reusability mechanism for sharing code from one module to another.

<a id="s2.2.2-pros"></a>
#### 2.2.2 Pros

The namespace management convention is simple. The source of each identifier is
indicated in a consistent way; `x.Obj` says that object `Obj` is defined in
module `x`.

<a id="s2.2.3-cons"></a>
#### 2.2.3 Cons

Module names can still collide. Some module names are inconveniently long.

<a id="s2.2.4-decision"></a>
#### 2.2.4 Decision

* Use `import x` for importing packages and modules.
* Use `from x import y` where `x` is the package prefix and `y` is the module
name with no prefix.
* Use `from x import y as z` if two modules named `y` are to be imported or if
`y` is an inconveniently long name.
* Use `import y as z` only when `z` is a standard abbreviation (e.g., `np` for
`numpy`).

For example the module `sound.effects.echo` may be imported as follows:

```python {.good}
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

Do not use relative names in imports. Even if the module is in the same package,
use the full package name. This helps prevent unintentionally importing a
package twice.

Note that there is an explicit exemption for imports from the [typing
module](#typing-imports).

<a id="s2.3-packages"></a>
<a id="packages"></a>
### 2.3 Packages

Import each module using the full pathname location of the module.

<a id="s2.3.1-pros"></a>
#### 2.3.1 Pros

Avoids conflicts in module names. Makes it easier to find modules.

<a id="S2.3.2-cons"></a>
#### 2.3.2 Cons

Makes it harder to deploy code because you have to replicate the package
hierarchy.

<a id="s2.3.3-decision"></a>
#### 2.3.3 Decision

All new code should import each module by its full package name.

Imports should be as follows:

```python {.good}
# Reference in code with complete name.
import absl.flags

# Reference in code with just module name (preferred).
from absl import flags
```

<a id="s2.4-exceptions"></a>
<a id="exceptions"></a>
### 2.4 Exceptions

Exceptions are allowed but must be used carefully.

<a id="s2.4.1-definition"></a>
#### 2.4.1 Definition

Exceptions are a means of breaking out of the normal flow of control of a code
block to handle errors or other exceptional conditions.

<a id="s2.4.2-pros"></a>
#### 2.4.2 Pros

The control flow of normal operation code is not cluttered by error-handling
code. It also allows the control flow to skip multiple frames when a certain
condition occurs, e.g., returning from N nested functions in one step instead of
having to carry-through error codes.

<a id="s2.4.3-cons"></a>
#### 2.4.3 Cons

May cause the control flow to be confusing. Easy to miss error cases when making
library calls.

<a id="s2.4.4-decision"></a>
#### 2.4.4 Decision

Exceptions must follow certain conditions:

-   Raise exceptions like this: `raise MyError('Error message')` or `raise
    MyError()`. Do not use the two-argument form (`raise MyError, 'Error
    message'`).

-   Make use of built-in exception classes when it makes sense. For example,
    raise a `ValueError` if you were passed a negative number but were expecting
    a positive one. Do not use `assert` statements for validating argument
    values of a public API. `assert` is used to ensure internal correctness, not
    to enforce correct usage nor to indicate that some unexpected event
    occurred. If an exception is desired in the latter cases, use a raise
    statement. For example:

    
    ```python {.good}
    Yes:
      def ConnectToNextPort(self, minimum):
        """Connects to the next available port.  Returns the new minimum port."""
        if minimum <= 1024:
          raise ValueError('Minimum port must be greater than 1024.')
        port = self._FindNextOpenPort(minimum)
        if not port:
          raise ConnectionError('Could not connect to service on %d or higher.' % (minimum,))
        assert port >= minimum, 'Unexpected port %d when minimum was %d.' % (port, minimum)
        return port
    ```

    ```python {.bad}
    No:
      def ConnectToNextPort(self, minimum):
        """Connects to the next available port.  Returns the new minimum port."""
        assert minimum > 1024, 'Minimum port must be greater than 1024.'
        port = self._FindNextOpenPort(minimum)
        assert port is not None
        return port
    ```

-   Libraries or packages may define their own exceptions. When doing so they
    must inherit from an existing exception class. Exception names should end in
    `Error` and should not introduce stutter (`foo.FooError`).

-   Never use catch-all `except:` statements, or catch `Exception` or
    `StandardError`, unless you are re-raising the exception or in the outermost
    block in your thread (and printing an error message). Python is very
    tolerant in this regard and `except:` will really catch everything including
    misspelled names, sys.exit() calls, Ctrl+C interrupts, unittest failures and
    all kinds of other exceptions that you simply don't want to catch.

-   Minimize the amount of code in a `try`/`except` block. The larger the body
    of the `try`, the more likely that an exception will be raised by a line of
    code that you didn't expect to raise an exception. In those cases, the
    `try`/`except` block hides a real error.

-   Use the `finally` clause to execute code whether or not an exception is
    raised in the `try` block. This is often useful for cleanup, i.e., closing a
    file.

-   When capturing an exception, use `as` rather than a comma. For example:

    
    ```python {.good}
    try:
      raise Error
    except Error as error:
      pass
    ```

<a id="s2.5-global-variables"></a>
<a id="global-variables"></a>
### 2.5 Global variables

Avoid global variables.

<a id="s2.5.1-definition"></a>
#### 2.5.1 Definition

Variables that are declared at the module level or as class attributes.

<a id="s2.5.2-pros"></a>
#### 2.5.2 Pros

Occasionally useful.

<a id="s2.5.3-cons"></a>
#### 2.5.3 Cons

Has the potential to change module behavior during the import, because
assignments to global variables are done when the module is first imported.

<a id="s2.5.4-decision"></a>
#### 2.5.4 Decision

Avoid global variables.

While they are technically variables, module-level constants are permitted and
encouraged. For example: `MAX_HOLY_HANDGRENADE_COUNT = 3`. Constants must be
named using all caps with underscores. See [Naming](#s3.16-naming) below.

If needed, globals should be declared at the module level and made internal to
the module by prepending an `_` to the name. External access must be done
through public module-level functions. See [Naming](#s3.16-naming) below.

<a id="s2.6-nested"></a>
<a id="nested"></a>
### 2.6 Nested/Local/Inner Classes and Functions

Nested local functions or classes are fine when used to close over a local
variable. Inner classes are fine.

<a id="s2.6.1-definition"></a>
#### 2.6.1 Definition

A class can be defined inside of a method, function, or class. A function can be
defined inside a method or function. Nested functions have read-only access to
variables defined in enclosing scopes.

<a id="s2.6.2-pros"></a>
#### 2.6.2 Pros

Allows definition of utility classes and functions that are only used inside of
a very limited scope. Very
[ADT](http://www.google.com/url?sa=D&q=http://en.wikipedia.org/wiki/Abstract_data_type)-y.

<a id="s2.6.3-cons"></a>
#### 2.6.3 Cons

Instances of nested or local classes cannot be pickled. Nested functions and
classes cannot be directly tested. Nesting can make your outer function longer
and less readable.

<a id="s2.6.4-decision"></a>
#### 2.6.4 Decision

They are fine with some caveats: Avoid nested functions or classes except when
closing over a local value for easier future comprehension. Do not nest a
function just to hide it from users of a module. Instead, prefix its name with
an \_ at the module level so that it can still be accessed by tests.

<a id="list-comprehensions"></a>
<a id="s2.7-list_comprehensions"></a>
<a id="list_comprehensions"></a>
### 2.7 Comprehensions & Generator Expressions

Okay to use for simple cases.

<a id="s2.7.1-definition"></a>
#### 2.7.1 Definition

List, Dict, and Set comprehensions as well as generator expressions provide a
concise and efficient way to create container types and iterators without
resorting to the use of traditional loops, `map()`, `filter()`, or `lambda`.

<a id="s2.7.2-pros"></a>
#### 2.7.2 Pros

Simple comprehensions can be clearer and simpler than other dict, list, or set
creation techniques. Generator expressions can be very efficient, since they
avoid the creation of a list entirely.

<a id="s2.7.3-cons"></a>
#### 2.7.3 Cons

Complicated comprehensions or generator expressions can be hard to read.

<a id="s2.7.4-decision"></a>
#### 2.7.4 Decision

Okay to use for simple cases. Each portion must fit on one line: mapping
expression, `for` clause, filter expression. Multiple `for` clauses or filter
expressions are not permitted. Use loops instead when things get more
complicated.

```python {.good}
Yes:
  result = []
  for x in range(10):
      for y in range(5):
          if x * y > 10:
              result.append((x, y))

  for x in xrange(5):
      for y in xrange(5):
          if x != y:
              for z in xrange(5):
                  if y != z:
                      yield (x, y, z)

  return ((x, complicated_transform(x))
          for x in long_generator_function(parameter)
          if x is not None)

  squares = [x * x for x in range(10)]

  eat(jelly_bean for jelly_bean in jelly_beans
      if jelly_bean.color == 'black')
```

```python {.bad}
No:
  result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

  return ((x, y, z)
          for x in xrange(5)
          for y in xrange(5)
          if x != y
          for z in xrange(5)
          if y != z)
```

<a id="s2.8-default-iterators-and-operators"></a>
<a id="default-iterators-and-operators"></a>
### 2.8 Default Iterators and Operators

Use default iterators and operators for types that support them, like lists,
dictionaries, and files.

<a id="s2.8.1-definition"></a>
#### 2.8.1 Definition

Container types, like dictionaries and lists, define default iterators and
membership test operators ("in" and "not in").

<a id="s2.8.2-pros"></a>
#### 2.8.2 Pros

The default iterators and operators are simple and efficient. They express the
operation directly, without extra method calls. A function that uses default
operators is generic. It can be used with any type that supports the operation.

<a id="s2.8.3-cons"></a>
#### 2.8.3 Cons

You can't tell the type of objects by reading the method names (e.g. has\_key()
means a dictionary). This is also an advantage.

<a id="s2.8.4-decision"></a>
#### 2.8.4 Decision

Use default iterators and operators for types that support them, like lists,
dictionaries, and files. The built-in types define iterator methods, too. Prefer
these methods to methods that return lists, except that you should not mutate a
container while iterating over it.

```python {.good}
Yes:  for key in adict: ...
      if key not in adict: ...
      if obj in alist: ...
      for line in afile: ...
      for k, v in dict.iteritems(): ...
```

```python {.bad}
No:   for key in adict.keys(): ...
      if not adict.has_key(key): ...
      for line in afile.readlines(): ...
```

<a id="s2.9-generators"></a>
<a id="generators"></a>
### 2.9 Generators

Use generators as needed.

<a id="s2.9.1-definition"></a>
#### 2.9.1 Definition

A generator function returns an iterator that yields a value each time it
executes a yield statement. After it yields a value, the runtime state of the
generator function is suspended until the next value is needed.

<a id="s2.9.2-pros"></a>
#### 2.9.2 Pros

Simpler code, because the state of local variables and control flow are
preserved for each call. A generator uses less memory than a function that
creates an entire list of values at once.

<a id="s2.9.3-cons"></a>
#### 2.9.3 Cons

None.

<a id="s2.9.4-decision"></a>
#### 2.9.4 Decision

Fine. Use "Yields:" rather than "Returns:" in the docstring for generator
functions.

<a id="s2.10-lambda-functions"></a>
<a id="lambda-functions"></a>
### 2.10 Lambda Functions

Okay for one-liners.

<a id="s2.10.1-definition"></a>
#### 2.10.1 Definition

Lambdas define anonymous functions in an expression, as opposed to a statement.
They are often used to define callbacks or operators for higher-order functions
like `map()` and `filter()`.

<a id="s2.10.2-pros"></a>
#### 2.10.2 Pros

Convenient.

<a id="s2.10.3-cons"></a>
#### 2.10.3 Cons

Harder to read and debug than local functions. The lack of names means stack
traces are more difficult to understand. Expressiveness is limited because the
function may only contain an expression.

<a id="s2.10.4-decision"></a>
#### 2.10.4 Decision

Okay to use them for one-liners. If the code inside the lambda function is any
longer than 60-80 chars, it's probably better to define it as a regular (nested)
function.

For common operations like multiplication, use the functions from the `operator`
module instead of lambda functions. For example, prefer `operator.mul` to
`lambda x, y: x * y`.

<a id="s2.11-conditional-expressions"></a>
<a id="conditional-expressions"></a>
### 2.11 Conditional Expressions

Okay for one-liners.

<a id="s2.11.1-definition"></a>
#### 2.11.1 Definition

Conditional expressions (sometimes called a “ternary operator”) are mechanisms
that provide a shorter syntax for if statements. For example:
`x = 1 if cond else 2`.

<a id="s2.11.2-pros"></a>
#### 2.11.2 Pros

Shorter and more convenient than an if statement.

<a id="s2.11.3-cons"></a>
#### 2.11.3 Cons

May be harder to read than an if statement. The condition may be difficult to
locate if the expression is long.

<a id="s2.11.4-decision"></a>
#### 2.11.4 Decision

Okay to use for one-liners. In other cases prefer to use a complete if
statement.

<a id="s2.12-default-argument-values"></a>
<a id="default-argument-values"></a>
### 2.12 Default Argument Values

Okay in most cases.

<a id="s2.12.1-definition"></a>
#### 2.12.1 Definition

You can specify values for variables at the end of a function's parameter list,
e.g., `def foo(a, b=0):`.  If `foo` is called with only one argument,
`b` is set to 0. If it is called with two arguments, `b` has the value of the
second argument.

<a id="s2.12.2-pros"></a>
#### 2.12.2 Pros

Often you have a function that uses lots of default values, but-rarely-you want
to override the defaults. Default argument values provide an easy way to do
this, without having to define lots of functions for the rare exceptions. Also,
Python does not support overloaded methods/functions and default arguments are
an easy way of "faking" the overloading behavior.

<a id="s2.12.3-cons"></a>
#### 2.12.3 Cons

Default arguments are evaluated once at module load time. This may cause
problems if the argument is a mutable object such as a list or a dictionary. If
the function modifies the object (e.g., by appending an item to a list), the
default value is modified.

<a id="s2.12.4-decision"></a>
#### 2.12.4 Decision

Okay to use with the following caveat:

Do not use mutable objects as default values in the function or method
definition.

```python {.good}
Yes: def foo(a, b=None):
         if b is None:
             b = []
Yes: def foo(a, b: Optional[Sequence] = None):
         if b is None:
             b = []
```

```python {.bad}
No:  def foo(a, b=[]):
         ...
No:  def foo(a, b=time.time()):  # The time the module was loaded???
         ...
No:  def foo(a, b=FLAGS.my_thing):  # sys.argv has not yet been parsed...
         ...
```

<a id="s2.13-properties"></a>
<a id="properties"></a>
### 2.13 Properties

Use properties for accessing or setting data where you would normally have used
simple, lightweight accessor or setter methods.

<a id="s2.13.1-definition"></a>
#### 2.13.1 Definition

A way to wrap method calls for getting and setting an attribute as a standard
attribute access when the computation is lightweight.

<a id="s2.13.2-pros"></a>
#### 2.13.2 Pros

Readability is increased by eliminating explicit get and set method calls for
simple attribute access. Allows calculations to be lazy. Considered the Pythonic
way to maintain the interface of a class. In terms of performance, allowing
properties bypasses needing trivial accessor methods when a direct variable
access is reasonable. This also allows accessor methods to be added in the
future without breaking the interface.

<a id="s2.13.3-cons"></a>
#### 2.13.3 Cons

Must inherit from `object` in Python 2. Can hide side-effects much like operator
overloading. Can be confusing for subclasses.

<a id="s2.13.4-decision"></a>
#### 2.13.4 Decision

Use properties in new code to access or set data where you would normally have
used simple, lightweight accessor or setter methods. Properties should be
created with the `@property` [decorator](#s2.17-function-and-method-decorators).

Inheritance with properties can be non-obvious if the property itself is not
overridden. Thus one must make sure that accessor methods are called indirectly
to ensure methods overridden in subclasses are called by the property (using the
Template Method DP).

```python {.good}
Yes: import math

     class Square(object):
         """A square with two properties: a writable area and a read-only perimeter.

         To use:
         >>> sq = Square(3)
         >>> sq.area
         9
         >>> sq.perimeter
         12
         >>> sq.area = 16
         >>> sq.side
         4
         >>> sq.perimeter
         16
         """

         def __init__(self, side):
             self.side = side

         @property
         def area(self):
             """Gets or sets the area of the square."""
             return self._get_area()

         @area.setter
         def area(self, area):
             return self._set_area(area)

         def _get_area(self):
             """Indirect accessor to calculate the 'area' property."""
             return self.side ** 2

         def _set_area(self, area):
             """Indirect setter to set the 'area' property."""
             self.side = math.sqrt(area)

         @property
         def perimeter(self):
             return self.side * 4
```

<a id="s2.14-truefalse-evaluations"></a>
<a id="truefalse-evaluations"></a>
### 2.14 True/False evaluations

Use the "implicit" false if at all possible.

<a id="s2.14.1-definition"></a>
#### 2.14.1 Definition

Python evaluates certain values as `False` when in a boolean context. A quick
"rule of thumb" is that all "empty" values are considered false, so
`0, None, [], {}, ''` all evaluate as false in a boolean context.

<a id="s2.14.2-pros"></a>
#### 2.14.2 Pros

Conditions using Python booleans are easier to read and less error-prone. In
most cases, they're also faster.

<a id="s2.14.3-cons"></a>
#### 2.14.3 Cons

May look strange to C/C++ developers.

<a id="s2.14.4-decision"></a>
#### 2.14.4 Decision

Use the "implicit" false if at all possible, e.g., `if foo:` rather than
`if foo != []:`. There are a few caveats that you should keep in mind though:

-   Never use `==` or `!=` to compare singletons like `None`. Use `is` or
    `is not`.

-   Beware of writing `if x:` when you really mean `if x is not None:`-e.g.,
    when testing whether a variable or argument that defaults to `None` was set
    to some other value. The other value might be a value that's false in a
    boolean context!

-   Never compare a boolean variable to `False` using `==`. Use `if not x:`
    instead. If you need to distinguish `False` from `None` then chain the
    expressions, such as `if not x and x is not None:`.

-   For sequences (strings, lists, tuples), use the fact that empty sequences
    are false, so `if seq:` and `if not seq:` are preferable to `if len(seq):`
    and `if not len(seq):` respectively.

-   When handling integers, implicit false may involve more risk than benefit
    (i.e., accidentally handling `None` as 0). You may compare a value which is
    known to be an integer (and is not the result of `len()`) against the
    integer 0.

    ```python {.good}
    Yes: if not users:
             print('no users')

         if foo == 0:
             self.handle_zero()

         if i % 10 == 0:
             self.handle_multiple_of_ten()

         def f(x=None):
             if x is None:
                 x = []
    ```

    ```python {.bad}
    No:  if len(users) == 0:
             print('no users')

         if foo is not None and not foo:
             self.handle_zero()

         if not i % 10:
             self.handle_multiple_of_ten()

         def f(x=None):
             x = x or []
    ```

-   Note that `'0'` (i.e., `0` as string) evaluates to true.

<a id="s2.15-deprecated-language-features"></a>
<a id="deprecated-language-features"></a>
### 2.15 Deprecated Language Features

Use string methods instead of the `string` module where possible. Use function
call syntax instead of `apply`. Use list comprehensions and `for` loops instead
of `filter` and `map` when the function argument would have been an inlined
lambda anyway. Use `for` loops instead of `reduce`.

<a id="s2.15.1-definition"></a>
#### 2.15.1 Definition

Current versions of Python provide alternative constructs that people find
generally preferable.

<a id="s2.15.2-decision"></a>
#### 2.15.2 Decision

We do not use any Python version which does not support these features, so there
is no reason not to use the new styles.

```python {.good}
Yes: words = foo.split(':')

     [x[1] for x in my_list if x[2] == 5]

     map(math.sqrt, data)    # Ok. No inlined lambda expression.

     fn(*args, **kwargs)
```

```python {.bad}
No:  words = string.split(foo, ':')

     map(lambda x: x[1], filter(lambda x: x[2] == 5, my_list))

     apply(fn, args, kwargs)
```

<a id="s2.16-lexical-scoping"></a>
<a id="lexical-scoping"></a>
### 2.16 Lexical Scoping

Okay to use.

<a id="s2.16.1-definition"></a>
#### 2.16.1 Definition

A nested Python function can refer to variables defined in enclosing functions,
but can not assign to them. Variable bindings are resolved using lexical
scoping, that is, based on the static program text. Any assignment to a name in
a block will cause Python to treat all references to that name as a local
variable, even if the use precedes the assignment. If a global declaration
occurs, the name is treated as a global variable.

An example of the use of this feature is:

```python {.good}
def get_adder(summand1):
    """Returns a function that adds numbers to a given number."""
    def adder(summand2):
        return summand1 + summand2

    return adder
```

<a id="s2.16.2-pros"></a>
#### 2.16.2 Pros

Often results in clearer, more elegant code. Especially comforting to
experienced Lisp and Scheme (and Haskell and ML and ...) programmers.

<a id="s2.16.3-cons"></a>
#### 2.16.3 Cons

Can lead to confusing bugs. Such as this example based on
[PEP-0227](http://www.google.com/url?sa=D&q=http://www.python.org/dev/peps/pep-0227/):

```python {.bad}
i = 4
def foo(x):
    def bar():
        print(i, end='')
    # ...
    # A bunch of code here
    # ...
    for i in x:  # Ah, i *is* local to foo, so this is what bar sees
        print(i, end='')
    bar()
```

So `foo([1, 2, 3])` will print `1 2 3 3`, not `1 2 3
4`.

<a id="s2.16.4-decision"></a>
#### 2.16.4 Decision

Okay to use.

<a id="s2.17-function-and-method-decorators"></a>
<a id="function-and-method-decorators"></a>
### 2.17 Function and Method Decorators

Use decorators judiciously when there is a clear advantage. Avoid
`@staticmethod` and limit use of `@classmethod`.

<a id="s2.17.1-definition"></a>
#### 2.17.1 Definition

[Decorators for Functions and
Methods](https://docs.python.org/2/whatsnew/2.4.html#pep-318-decorators-for-functions-and-methods)
(a.k.a "the `@` notation"). One common decorator is `@property`, used for
converting ordinary methods into dynamically computed attributes. However, the
decorator syntax allows for user-defined decorators as well. Specifically, for
some function `my_decorator`, this:

```python {.good}
class C(object):
    @my_decorator
    def method(self):
        # method body ...
```

is equivalent to:

```python {.good}
class C(object):
    def Methodmethod(self):
        # method body ...
    Methodmethod = MyDecoratormy_decorator(Methodmethod)
```

<a id="s2.17.2-pros"></a>
#### 2.17.2 Pros

Elegantly specifies some transformation on a method; the transformation might
eliminate some repetitive code, enforce invariants, etc.

<a id="s2.17.3-cons"></a>
#### 2.17.3 Cons

Decorators can perform arbitrary operations on a function's arguments or return
values, resulting in surprising implicit behavior. Additionally, decorators
execute at import time. Failures in decorator code are pretty much impossible to
recover from.

<a id="s2.17.4-decision"></a>
#### 2.17.4 Decision

Use decorators judiciously when there is a clear advantage. Decorators should
follow the same import and naming guidelines as functions. Decorator pydoc
should clearly state that the function is a decorator. Write unit tests for
decorators.

Avoid external dependencies in the decorator itself (e.g. don't rely on files,
sockets, database connections, etc.), since they might not be available when the
decorator runs (at import time, perhaps from `pydoc` or other tools). A
decorator that is called with valid parameters should (as much as possible) be
guaranteed to succeed in all cases.

Decorators are a special case of "top level code" - see [main](#s3.17-main) for
more discussion.

Never use `@staticmethod` unless forced to in order to integrate with an API
defined in an existing library. Write a module level function instead.

Use `@classmethod` only when writing a named constructor or a class-specific
routine that modifies necessary global state such as a process-wide cache.

<a id="s2.18-threading"></a>
<a id="threading"></a>
### 2.18 Threading

Do not rely on the atomicity of built-in types.

While Python's built-in data types such as dictionaries appear to have atomic
operations, there are corner cases where they aren't atomic (e.g. if `__hash__`
or `__eq__` are implemented as Python methods) and their atomicity should not be
relied upon. Neither should you rely on atomic variable assignment (since this
in turn depends on dictionaries).

Use the Queue module's `Queue` data type as the preferred way to communicate
data between threads. Otherwise, use the threading module and its locking
primitives. Learn about the proper use of condition variables so you can use
`threading.Condition` instead of using lower-level locks.

<a id="s2.19-power-features"></a>
<a id="power-features"></a>
### 2.19 Power Features

Avoid these features.

<a id="s2.19.1-definition"></a>
#### 2.19.1 Definition

Python is an extremely flexible language and gives you many fancy features such
as custom metaclasses, access to bytecode, on-the-fly compilation, dynamic
inheritance, object reparenting, import hacks, reflection, modification of
system internals, etc.

<a id="s2.19.2-pros"></a>
#### 2.19.2 Pros

These are powerful language features. They can make your code more compact.

<a id="s2.19.3-cons"></a>
#### 2.19.3 Cons

It's very tempting to use these "cool" features when they're not absolutely
necessary. It's harder to read, understand, and debug code that's using unusual
features underneath. It doesn't seem that way at first (to the original author),
but when revisiting the code, it tends to be more difficult than code that is
longer but is straightforward.

<a id="s2.19.4-decision"></a>
#### 2.19.4 Decision

Avoid these features in your code.

Standard library modules and classes that internally use these features are okay
to use (for example, `abc.ABCMeta`, `collections.namedtuple`, and `enum`).

<a id="s2.20-modern-python"></a>
<a id="modern-python"></a>
### 2.20 Modern Python: Python 3 and from \_\_future\_\_ imports {#modern-python}

Python 3 is here. While not every project is ready to use it yet, all code should be written with an eye towards the future.

<a id="s2.20.1-definition"></a>
#### 2.20.1 Definition

Python 3 is a significant change in the Python language. While existing code is
often written with 2.7 in mind there are some simple things to do to make code
more explicit about its intentions and thus better prepared for use under Python
3 without modification.

<a id="s2.20.2-pros"></a>
#### 2.20.2 Pros

Code written with Python 3 in mind is more explicit and easier to get running
under Python 3 once all of the dependencies of your project are ready.

<a id="s2.20.3-cons"></a>
#### 2.20.3 Cons

Some people find the additional boilerplate to be ugly. Others say "but I don't
use that feature in this file" and want to clean-up. Please don't. It is better
to always have the future imports in all files so that they are not forgotten
during later edits when someone starts using such a feature.

<a id="s2.20.4-decision"></a>
#### 2.20.4 Decision

##### from \_\_future\_\_ imports

Use of `from __future__ import` statements is encouraged. All new code should
contain the following and existing code should be updated to be compatible when
possible:

```python {.good}
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
```

If you are not already familiar with those, read up on each here: [absolute
imports](https://www.python.org/dev/peps/pep-0328/), [new `/` division
behavior](https://www.python.org/dev/peps/pep-0238/), and [the print
function](https://www.python.org/dev/peps/pep-3105/).

There are other `from __future__` import statements. Use them as you see fit. We
do not include `unicode_literals` in our recommendations as it is not a clear
win due to implicit default codec conversion consequences it introduces in many
places within Python 2.7. Most code is better off with explicit use of `b''` and
`u''` bytes and unicode string literals as necessary.

##### The six, future, or past libraries.

When your project needs to actively support use under both Python 2 and 3, use
of these libraries is encouraged as you see fit. They exist to make your code
cleaner and life easier.

<a name="s2.21-typed-code"></a>
<a name="typed-code"></a>
### 2.21 Type Annotated Code

You can annotate Python 3 code with type hints according to
[PEP-484](https://www.python.org/dev/peps/pep-0484/), and type-check the code at
build time with a type checking tool like
[pytype](https://github.com/google/pytype).


Type annotations can be in the source or in a [stub pyi
file](https://www.python.org/dev/peps/pep-0484/#stub-files). Whenever possible,
annotations should be in the source. Use pyi files for third-party or extension
modules.


<a id="s2.21.1-definition"></a>
#### 2.21.1 Definition

Type annotations (or "type hints") are for function or method arguments and
return values:

```python {.good}
def func(a: int) -> List[int]:
```

You can also declare the type of a variable using a special comment:

```python {.good}
a = SomeFunc()  # type: SomeType
```

<a id="s2.21.2-pros"></a>
#### 2.21.2 Pros

Type annotations improve the readability and maintainability of your code. The
type checker will convert many runtime errors to build-time errors, and reduce
your ability to use [Power Features](#power-features).

<a id="s2.21.3-cons"></a>
#### 2.21.3 Cons

You will have to keep the type declarations up to date. You might see type errors that you think are valid code. Use of a [type checker](https://github.com/google/pytype)
may reduce your ability to use [Power Features](#power-features).

<a id="s2.21.4-decision"></a>
#### 2.21.4 Decision

This highly depends on the complexity of your project. Give it a try.


<a id="s3-python-style-rules"></a>
<a id="python-style-rules"></a>
## 3 Python Style Rules

<a id="s3.1-semicolons"></a>
<a id="semicolons"></a>
### 3.1 Semicolons

Do not terminate your lines with semi-colons and do not use semi-colons to put
two statements on the same line.

<a id="s3.2-line-length"></a>
<a id="line-length"></a>
### 3.2 Line length

Maximum line length is *80 characters*.

Exceptions:

-   Long import statements.
-   URLs, pathnames, or long flags in comments.
-   Long string module level constants not containing whitespace that would be
    inconvenient to split across lines such as URLs or pathnames.
-   Pylint disable comments. (e.g.: `# pylint: disable=invalid-name`)

Do not use backslash line continuation except for `with` statements requiring
three or more context managers.

Make use of Python's [implicit line joining inside parentheses, brackets and
braces](http://docs.python.org/reference/lexical_analysis.html#implicit-line-joining).
If necessary, you can add an extra pair of parentheses around an expression.

```python {.good}
Yes: foo_bar(self, width, height, color='black', design=None, x='foo',
             emphasis=None, highlight=0)

     if (width == 0 and height == 0 and
         color == 'red' and emphasis == 'strong'):
```

When a literal string won't fit on a single line, use parentheses for implicit
line joining.

```python {.good}
x = ('This will build a very long long '
     'long long long long long long string')
```

Within comments, put long URLs on their own line if necessary.

```python {.good}
Yes:  # See details at
      # http://www.example.com/us/developer/documentation/api/content/v2.0/csv_file_name_extension_full_specification.html
```

```python {.bad}
No:  # See details at
     # http://www.example.com/us/developer/documentation/api/content/\
     # v2.0/csv_file_name_extension_full_specification.html
```

It is permissible to use backslash continuation when defining a `with` statement
whose expressions span three or more lines. For two lines of expressions, use a
nested `with` statement:

```python {.good}
Yes:  with very_long_first_expression_function() as spam, \
           very_long_second_expression_function() as beans, \
           third_thing() as eggs:
          place_order(eggs, beans, spam, beans)
```

```python {.bad}
No:  with VeryLongFirstExpressionFunction() as spam, \
          VeryLongSecondExpressionFunction() as beans:
       PlaceOrder(eggs, beans, spam, beans)
```

```python {.good}
Yes:  with very_long_first_expression_function() as spam:
          with very_long_second_expression_function() as beans:
              place_order(beans, spam)
```

Make note of the indentation of the elements in the line continuation examples
above; see the [indentation](#s3.4-indentation) section for explanation.

<a id="s3.3-parentheses"></a>
<a id="parentheses"></a>
### 3.3 Parentheses

Use parentheses sparingly.

It is fine, though not required, to use parentheses around tuples. Do not use
them in return statements or conditional statements unless using parentheses for
implied line continuation or to indicate a tuple.

```python {.good}
Yes: if foo:
         bar()
     while x:
         x = bar()
     if x and y:
         bar()
     if not x:
         bar()
     # For a 1 item tuple the ()s are more visually obvious than the comma.
     onesie = (foo,)
     return foo
     return spam, beans
     return (spam, beans)
     for (x, y) in dict.items(): ...
```

```python {.bad}
No:  if (x):
         bar()
     if not(x):
         bar()
     return (foo)
```


<a id="s3.4-indentation"></a>
<a id="indentation"></a>
### 3.4 Indentation

Indent your code blocks with *4 spaces*.

Never use tabs or mix tabs and spaces. In cases of implied line continuation,
you should align wrapped elements either vertically, as per the examples in the
[line length](#s3.2-line-length) section; or using a hanging indent of 4 spaces,
in which case there should be nothing after the open parenthesis or bracket on
the first line.

```python {.good}
Yes:   # Aligned with opening delimiter
       foo = long_function_name(var_one, var_two,
                                var_three, var_four)
       meal = (spam,
               beans)

       # Aligned with opening delimiter in a dictionary
       foo = {
           long_dictionary_key: value1 +
                                value2,
           ...
       }

       # 4-space hanging indent; nothing on first line
       foo = long_function_name(
           var_one, var_two, var_three,
           var_four)
       meal = (
           spam,
           beans)

       # 4-space hanging indent in a dictionary
       foo = {
           long_dictionary_key:
               long_dictionary_value,
           ...
       }
```

```python {.bad}
No:    # Stuff on first line forbidden
       foo = long_function_name(var_one, var_two,
           var_three, var_four)
       meal = (spam,
           beans)

       # 2-space hanging indent forbidden
       foo = long_function_name(
         var_one, var_two, var_three,
         var_four)

       # No hanging indent in a dictionary
       foo = {
           long_dictionary_key:
           long_dictionary_value,
           ...
       }
```

<a id="s3.5-blank-lines"></a>
<a id="blank-lines"></a>
### 3.5 Blank Lines

Two blank lines between top-level definitions, one blank line between method
definitions.

Two blank lines between top-level definitions, be they function or class
definitions. One blank line between method definitions and between the `class`
line and the first method. Use single blank lines as you judge appropriate
within functions or methods.

<a id="s3.6-whitespace"></a>
<a id="whitespace"></a>
### 3.6 Whitespace

Follow standard typographic rules for the use of spaces around punctuation.

No whitespace inside parentheses, brackets or braces.

```python {.good}
Yes: spam(ham[1], {eggs: 2}, [])
```

```python {.bad}
No:  spam( ham[ 1 ], { eggs: 2 }, [ ] )
```

No whitespace before a comma, semicolon, or colon. Do use whitespace after a
comma, semicolon, or colon except at the end of the line.

```python {.good}
Yes: if x == 4:
         print(x, y)
     x, y = y, x
```

```python {.bad}
No:  if x == 4 :
         print(x , y)
     x , y = y , x
```

No whitespace before the open paren/bracket that starts an argument list,
indexing or slicing.

```python {.good}
Yes: spam(1)
```

```python {.bad}
No:  spam (1)
```


```python {.good}
Yes: dict['key'] = list[index]
```

```python {.bad}
No:  dict ['key'] = list [index]
```

Surround binary operators with a single space on either side for assignment
(`=`), comparisons (`==, <, >, !=, <>, <=, >=, in, not in, is, is not`), and
Booleans (`and, or, not`). Use your better judgment for the insertion of spaces
around arithmetic operators but always be consistent about whitespace on either
side of a binary operator.

```python {.good}
Yes: x == 1
```

```python {.bad}
No:  x<1
```

Never use spaces around the '=' sign when passing keyword arguments.
Only use spaces around the '=' sign defining a default parameter value
[when a type annotation is present](#typing-default-values),
do not use spaces around '=' for default parameter values otherwise.

```python {.good}
Yes: def complex(real, imag=0.0): return Magic(r=real, i=imag)
Yes: def complex(real, imag: float = 0.0): return Magic(r=real, i=imag)
```

```python {.bad}
No:  def complex(real, imag = 0.0): return Magic(r = real, i = imag)
No:  def complex(real, imag: float=0.0): return Magic(r = real, i = imag)
```

Don't use spaces to vertically align tokens on consecutive lines, since it
becomes a maintenance burden (applies to `:`, `#`, `=`, etc.):

```python {.good}
Yes:
  foo = 1000  # comment
  long_name = 2  # comment that should not be aligned

  dictionary = {
      'foo': 1,
      'long_name': 2,
  }
```

```python {.bad}
No:
  foo       = 1000  # comment
  long_name = 2     # comment that should not be aligned

  dictionary = {
      'foo'      : 1,
      'long_name': 2,
  }
```


<a id="Python_Interpreter"></a>
<a id="s3.7-shebang-line"></a>
<a id="shebang-line"></a>
### 3.7 Shebang Line

Most `.py` files do not need to start with a `#!` line. Start the main file of a
program with
`#!/usr/bin/python` with an optional single digit `2` or `3` suffix per
[PEP-394](https://www.google.com/url?sa=D&q=http://www.python.org/dev/peps/pep-0394/).

This line is used by the kernel to find the Python interpreter, but is ignored
by Python when importing modules. It is only necessary on a file that will be
executed directly.

<a id="s3.8-comments"></a>
<a id="comments"></a>
### 3.8 Comments and Docstrings

Be sure to use the right style for module, function, method docstrings and
in-line comments.

<a id="s3.8.1-comments-in-doc-strings"></a>
<a id="comments-in-doc-strings"></a>
#### 3.8.1 Docstrings

Python uses docstrings for commenting code. A doc string is a string that is the
first statement in a package, module, class or function. These strings can be
extracted automatically through the `__doc__` member of the object and are used
by `pydoc`.
(Try running `pydoc` on your module to see how it looks.) Always use the three
double-quote `"""` format for docstrings (per [PEP
257](https://www.google.com/url?sa=D&q=http://www.python.org/dev/peps/pep-0257/)).
A docstring should be organized as a summary line (one physical line) terminated
by a period, question mark, or exclamation point, followed by a blank line,
followed by the rest of the docstring starting at the same cursor position as
the first quote of the first line. There are more formatting guidelines for
docstrings below.

<a id="s3.8.2-comments-in-modules"></a>
<a id="comments-in-modules"></a>
#### 3.8.2 Modules

Every file should contain license boilerplate. Choose the appropriate
boilerplate for the license used by the project (for example, Apache 2.0, BSD,
LGPL, GPL)

<a id="s3.8.3-functions-and-methods"></a>
<a id="functions-and-methods"></a>
#### 3.8.3 Functions and Methods

As used in this section "function" applies to methods, functions, and
generators.

A function must have a docstring, unless it meets all of the following criteria:

-   not externally visible
-   very short
-   obvious

A docstring should give enough information to write a call to the function
without reading the function's code. The docstring should be descriptive
(`"""Fetches rows from a Bigtable."""`) rather than imperative
(`"""Fetch rows from a Bigtable."""`). A docstring should describe the
function's calling syntax and its semantics, not its implementation. For tricky
code, comments alongside the code are more appropriate than using docstrings.

A method that overrides a method from a base class may have a simple docstring
sending the reader to its overridden method's docstring, such as
`"""See base class."""`. The rationale is that there is no need to repeat in
many places documentation that is already present in the base method's
docstring. However, if the overriding method's behavior is substantially
different than that of the overridden method or details need to be provided
about it (e.g., documenting additional side-effects), a docstring is required on
the overriding method, with at least those differences.

Certain aspects of a function should be documented in special sections, listed
below. Each section begins with a heading line, which ends with a colon.
Sections should be indented two spaces, except for the heading.

*Args:*
: List each parameter by name. A description should follow the name, and be
: separated by a colon and a space. If the description is too long to fit on a
: single 80-character line, use a hanging indent of 2 or 4 spaces (be
: consistent with the rest of the file).<br/> 
: The description should include required type(s) if the code does not contain
: a corresponding type annotation.<br/>
: If a function accepts `*foo` (variable length argument lists) and/or `**bar`
: (arbitrary keyword arguments), they should be listed as `*foo` and `**bar`.

*Returns:* (or *Yields:* for generators)
: Describe the type and semantics of the return value. If the function only
: returns None, this section is not required. It may also be omitted if the
: docstring starts with Returns (or Yields) (e.g.
: `"""Returns row from Bigtable as a tuple of strings."""`) and the opening
: sentence is sufficient to describe return value.

*Raises:*
: List all exceptions that are relevant to the interface.

```python {.good}
def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
```

<a id="s3.8.4-comments-in-classes"></a>
<a id="comments-in-classes"></a>
#### 3.8.4 Classes

Classes should have a docstring below the class definition describing the class.
If your class has public attributes, they should be documented here in an
Attributes section and follow the same formatting as a function's Args section.

```python {.good}
class SampleClass(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""
```

<a id="comments-in-block-and-inline"></a>
<a id="s3.8.5-comments-in-block-and-inline"></a>
#### 3.8.5 Block and Inline Comments

The final place to have comments is in tricky parts of the code. If you're going
to have to explain it at the next [code
review](http://en.wikipedia.org/wiki/Code_review), you should comment it
now. Complicated operations get a few lines of comments before the operations
commence. Non-obvious ones get comments at the end of the line.

```python {.good}
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

To improve legibility, these comments should be at least 2 spaces away from the
code.

On the other hand, never describe the code. Assume the person reading the code
knows Python (though not what you're trying to do) better than you do.

```python {.bad}
# BAD COMMENT: Now go through the b array and make sure whenever i occurs
# the next element is i+1
```

<!-- The next section is copied from the C++ style guide. -->
<a id="s3.8.6-punctuation-spelling-and-grammar"></a>
<a id="punctuation-spelling-and-grammar"></a>
#### 3.8.6 Punctuation, Spelling and Grammar

Pay attention to punctuation, spelling, and grammar; it is easier to read
well-written comments than badly written ones.

Comments should be as readable as narrative text, with proper capitalization and
punctuation. In many cases, complete sentences are more readable than sentence
fragments. Shorter comments, such as comments at the end of a line of code, can
sometimes be less formal, but you should be consistent with your style.

Although it can be frustrating to have a code reviewer point out that you are
using a comma when you should be using a semicolon, it is very important that
source code maintain a high level of clarity and readability. Proper
punctuation, spelling, and grammar help with that goal.

<a id="s3.9-classes"></a>
<a id="classes"></a>
### 3.9 Classes

If a class inherits from no other base classes, explicitly inherit from
`object`. This also applies to nested classes.

```python {.good}
Yes: class SampleClass(object):
         pass


     class OuterClass(object):

         class InnerClass(object):
             pass


     class ChildClass(ParentClass):
         """Explicitly inherits from another class already."""

```

```python {.bad}
No: class SampleClass:
        pass


    class OuterClass:

        class InnerClass:
            pass
```

Inheriting from `object` is needed to make properties work properly in Python 2,
and can protect your code from some potential incompatibility with Python 3. It
also defines special methods that implement the default semantics of objects
including `__new__`, `__init__`, `__delattr__`, `__getattribute__`,
`__setattr__`, `__hash__`, `__repr__`, and `__str__`.

<a id="s3.10-strings"></a>
<a id="strings"></a>
### 3.10 Strings

Use the `format` method or the `%` operator for formatting strings, even when
the parameters are all strings. Use your best judgement to decide between `+`
and `%` (or `format`) though.

```python {.good}
Yes: x = a + b
     x = '%s, %s!' % (imperative, expletive)
     x = '{}, {}'.format(first, second)
     x = 'name: %s; score: %d' % (name, n)
     x = 'name: {}; score: {}'.format(name, n)
     x = f'name: {name}; score: {n}'  # Python 3.6+
```

```python {.bad}
No: x = '%s%s' % (a, b)  # use + in this case
    x = '{}{}'.format(a, b)  # use + in this case
    x = first + ', ' + second
    x = 'name: ' + name + '; score: ' + str(n)
```

Avoid using the `+` and `+=` operators to accumulate a string within a loop.
Since strings are immutable, this creates unnecessary temporary objects and
results in quadratic rather than linear running time. Instead, add each
substring to a list and `''.join` the list after the loop terminates (or, write
each substring to a `io.BytesIO` buffer).

```python {.good}
Yes: items = ['<table>']
     for last_name, first_name in employee_list:
         items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
     items.append('</table>')
     employee_table = ''.join(items)
```

```python {.bad}
No: employee_table = '<table>'
    for last_name, first_name in employee_list:
        employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
    employee_table += '</table>'
```

Be consistent with your choice of string quote character within a file. Pick `'`
or `"` and stick with it. It is okay to use the other quote character on a
string to avoid the need to `\\` escape within the string. `gpylint` enforces
this.

```python {.good}
Yes:
  Python('Why are you hiding your eyes?')
  Gollum("I'm scared of lint errors.")
  Narrator('"Good!" thought a happy Python reviewer.')
```

```python {.bad}
No:
  Python("Why are you hiding your eyes?")
  Gollum('The lint. It burns. It burns us.')
  Gollum("Always the great lint. Watching. Watching.")
```

Prefer `"""` for multi-line strings rather than `'''`. Projects may choose to
use `'''` for all non-docstring multi-line strings if and only if they also use
`'` for regular strings. Docstrings must use `"""` regardless. Note that it is
often cleaner to use implicit line joining since multi-line strings do not flow
with the indentation of the rest of the program:

```python {.good}
  Yes:
  print("This is much nicer.\n"
        "Do it this way.\n")
```

```python {.bad}
  No:
    print("""This is pretty ugly.
Don't do this.
""")
```

<a id="s3.11-files-and-sockets"></a>
<a id="files-and-sockets"></a>
### 3.11 Files and Sockets

Explicitly close files and sockets when done with them.

Leaving files, sockets or other file-like objects open unnecessarily has many
downsides, including:

-   They may consume limited system resources, such as file descriptors. Code
    that deals with many such objects may exhaust those resources unnecessarily
    if they're not returned to the system promptly after use.
-   Holding files open may prevent other actions being performed on them, such
    as moves or deletion.
-   Files and sockets that are shared throughout a program may inadvertently be
    read from or written to after logically being closed. If they are actually
    closed, attempts to read or write from them will throw exceptions, making
    the problem known sooner.

Furthermore, while files and sockets are automatically closed when the file
object is destructed, tying the life-time of the file object to the state of the
file is poor practice, for several reasons:

-   There are no guarantees as to when the runtime will actually run the file's
    destructor. Different Python implementations use different memory management
    techniques, such as delayed Garbage Collection, which may increase the
    object's lifetime arbitrarily and indefinitely.
-   Unexpected references to the file may keep it around longer than intended
    (e.g. in tracebacks of exceptions, inside globals, etc).

The preferred way to manage files is using the ["with"
statement](http://docs.python.org/reference/compound_stmts.html#the-with-statement):

```python {.good}
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)
```

For file-like objects that do not support the "with" statement, use
`contextlib.closing()`:

```python {.good}
import contextlib

with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
    for line in front_page:
        print(line)
```

<a id="s3.12-todo-comments"></a>
<a id="todo-comments"></a>
### 3.12 TODO Comments

Use `TODO` comments for code that is temporary, a short-term solution, or
good-enough but not perfect.

`TODO`s should include the string `TODO` in all caps, followed by the
name, e-mail address, or other identifier
of the person or issue with the best context about the problem referenced by the
`TODO`, in parentheses. A comment explaining what there is to do is required.
The main purpose is to have a consistent `TODO` format that can be searched to
find out how to get more details upon request. A `TODO` is not a commitment that
the person referenced will fix the problem. Thus when you create a `TODO`, it is almost always your name that is given.

```python {.good}
# TODO(kl@gmail.com): Use a "*" here for string repetition.
# TODO(Zeke) Change this to use relations.
```

If your `TODO` is of the form "At a future date do something" make sure that you
either include a very specific date ("Fix by November 2009") or a very specific
event ("Remove this code when all clients can handle XML responses.").

<a id="s3.13-imports-formatting"></a>
<a id="imports-formatting"></a>
### 3.13 Imports formatting

Imports should be on separate lines.

E.g.:

```python {.good}
Yes: import os
     import sys
```

```python {.bad}
No:  import os, sys
```

Imports are always put at the top of the file, just after any module comments
and docstrings and before module globals and constants. Imports should be
grouped with the order being most generic to least generic:

1.  Python standard library imports. For example:

    ```python {.good}
    import sys
    ```

2.  [third-party](https://pypi.python.org/pypi)
    module or package imports. For example:

    
    ```python {.good}
    import tensorflow as tf
    ```

3.  Code repository
    sub-package imports. For example:

    
    ```python {.good}
    from otherproject.ai import mind
    ```

4.  application-specific imports that are part of the same
    top level
    sub-package as this file. For example:

    
    ```python {.good}
    from myproject.backend.hgwells import time_machine
    ```

Within each grouping, imports should be sorted lexicographically, ignoring case,
according to each module's full package path. Code may optionally place a blank
line between import sections.

```python {.good}
import collections
import Queue
import sys

import argcomplete
import BeautifulSoup
import cryptography
import tensorflow as tf

from otherproject.ai import body
from otherproject.ai import mind
from otherproject.ai import soul

from myproject.backend.hgwells import time_machine
from myproject.backend.state_machine import main_loop
```


<a id="s3.14-statements"></a>
<a id="statements"></a>
### 3.14 Statements

Generally only one statement per line.

However, you may put the result of a test on the same line as the test only if
the entire statement fits on one line. In particular, you can never do so with
`try`/`except` since the `try` and `except` can't both fit on the same line, and
you can only do so with an `if` if there is no `else`.

```python {.good}
Yes:

  if foo: bar(foo)
```

```python {.bad}
No:

  if foo: bar(foo)
  else:   baz(foo)

  try:               bar(foo)
  except ValueError: baz(foo)

  try:
      bar(foo)
  except ValueError: baz(foo)
```

<a id="s3.15-access-control"></a>
<a id="access-control"></a>
### 3.15 Access Control

If an accessor function would be trivial you should use public variables instead
of accessor functions to avoid the extra cost of function calls in Python. When
more functionality is added you can use `property` to keep the syntax
consistent.

On the other hand, if access is more complex, or the cost of accessing the
variable is significant, you should use function calls (following the
[Naming](#s3.16-naming) guidelines) such as `get_foo()` and
`set_foo()`. If the past behavior allowed access through a property, do not
bind the new accessor functions to the property. Any code still attempting to
access the variable by the old method should break visibly so they are made
aware of the change in complexity.

<a id="s3.16-naming"></a>
<a id="naming"></a>
### 3.16 Naming

`module_name`,
`package_name`,
`ClassName`,
`method_name`,
`ExceptionName`,
`function_name`,
`GLOBAL_CONSTANT_NAME`,
`global_var_name`,
`instance_var_name`,
`function_parameter_name`,
`local_var_name`.

Function names, variable names, and filenames should be descriptive; eschew
abbreviation. In particular, do not use abbreviations that are ambiguous or
unfamiliar to readers outside your project, and do not abbreviate by deleting
letters within a word.

Always use a `.py` filename extension. Never use dashes.

<a id="s3.16.1-names-to-avoid"></a>
<a id="names-to-avoid"></a>
#### 3.16.1 Names to Avoid

-   single character names except for counters or iterators. You may use "e" as
    an exception identifier in try/except statements.
-   dashes (`-`) in any package/module name
-   `__double_leading_and_trailing_underscore__` names (reserved by Python)

<a id="s3.16.2-naming-conventions"></a>
<a id="naming-conventions"></a>
#### 3.16.2 Naming Convention

-   "Internal" means internal to a module or protected or private within a
    class.

-   Prepending a single underscore (`_`) has some support for protecting module
    variables and functions (not included with `from module import *`). While
    prepending a double underscore (`__` aka "dunder") to an instance variable
    or method effectively makes the variable or method private to its class
    (using name mangling) we discourage its use as it impacts readability and
    testability and isn't *really* private.

-   Place related classes and top-level functions together in a
    module.
    Unlike Java, there is no need to limit yourself to one class per module.

-   Use CapWords for class names, but lower\_with\_under.py for module names.
    Although there are some old modules named CapWords.py, this is now
    discouraged because it's confusing when the module happens to be named after
    a class. ("wait -- did I write `import StringIO` or
    `from StringIO import StringIO`?")

-   Underscores may appear in *unittest* method names starting with `test` to
    separate logical components of the name, even if those components use
    CapWords. One possible pattern is `test<MethodUnderTest>_<state>`; for
    example `testPop_EmptyStack` is okay. There is no One Correct Way to name
    test methods.

<a id="s3.16.3-file-naming"></a>
<a id="file-naming"></a>
#### 3.16.3 File Naming {#s3.16.3-file-naming}

Python filenames must have a `.py` extension and must not contain dashes (`-`).
This allows them to be imported and unittested. If you want an executable to be
accessible without the extension, use a symbolic link or a simple bash wrapper
containing `exec "$0.py" "$@"`.

<a id="s3.16.4-guidelines-derived-from-guidos-recommendations"></a>
<a id="guidelines-derived-from-guidos-recommendations"></a>
#### 3.16.4 Guidelines derived from Guido's Recommendations

<table rules="all" border="1" summary="Guidelines from Guido's Recommendations"
       cellspacing="2" cellpadding="2">

  <tr>
    <th>Type</th>
    <th>Public</th>
    <th>Internal</th>
  </tr>

  <tr>
    <td>Packages</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Modules</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>Classes</td>
    <td><code>CapWords</code></td>
    <td><code>_CapWords</code></td>
  </tr>

  <tr>
    <td>Exceptions</td>
    <td><code>CapWords</code></td>
    <td></td>
  </tr>

    <tr>
    <td>Functions</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code></td>
  </tr>

  <tr>
    <td>Global/Class Constants</td>
    <td><code>CAPS_WITH_UNDER</code></td>
    <td><code>_CAPS_WITH_UNDER</code></td>
  </tr>

  <tr>
    <td>Global/Class Variables</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>Instance Variables</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code> (protected)</td>
  </tr>

    <tr>
    <td>Method Names</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code> (protected)</td>
  </tr>

  <tr>
    <td>Function/Method Parameters</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Local Variables</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

</table>

While Python supports making things private by using a leading double underscore
`__` (aka. "dunder") prefix on a name their use is discouraged. Prefer the use
of a single underscore. They are much easier to type, read, and to access from
small unittests. Lint warnings take care of invalid access to protected members.


<a id="s3.17-main"></a>
<a id="main"></a>
### 3.17 Main

Even a file meant to be used as an executable should be importable and a mere
import should not have the side effect of executing the program's main
functionality. The main functionality should be in a `main()` function.

In Python, `pydoc` as well as unit tests require modules to be importable. Your
code should always check `if __name__ == '__main__'` before executing your main
program so that the main program is not executed when the module is imported.

```python {.good}
def main():
    ...

if __name__ == '__main__':
    main()
```

All code at the top level will be executed when the module is imported. Be
careful not to call functions, create objects, or perform other operations that
should not be executed when the file is being `pydoc`ed.

<a id="s3.18-function-length"></a>
<a id="function-length"></a>
### 3.18 Function length

Prefer small and focused functions.

We recognize that long functions are sometimes appropriate, so no hard limit is
placed on function length. If a function exceeds about 40 lines, think about
whether it can be broken up without harming the structure of the program.

Even if your long function works perfectly now, someone modifying it in a few
months may add new behavior. This could result in bugs that are hard to find.
Keeping your functions short and simple makes it easier for other people to read
and modify your code.

You could find long and complicated functions when working with
some code. Do not be intimidated by modifying existing code: if working with such
a function proves to be difficult, you find that errors are hard to debug, or
you want to use a piece of it in several different contexts, consider breaking
up the function into smaller and more manageable pieces.

<a id="s3.19-type-annotations"></a>
<a id="type-annotations"></a>
### 3.19 Type Annotations

<a id="typing-general"></a>
<a id="s3.19.1-general"></a>
#### 3.19.1 General Rules

* Familiarize yourself with [PEP-484](https://www.python.org/dev/peps/pep-0484/).
* In methods, never annotate `self`, or `cls`.
* If any other variable or a returned type should not be expressed, use `Any`.
* You are not required to annotate all the functions in a module.
  -   At least annotate your public APIs.
  -   Use judgment to get to a good balance between safety and clarity on the
      one hand, and flexibility on the other.
  -   Annotate code that is prone to type-related errors (previous bugs or
      complexity).
  -   Annotate code that is hard to understand.
  -   Annotate code as it becomes stable from a types perspective. In many
      cases, you can annotate all the functions in mature code without losing
      too much flexibility.


<a id="s3.19.2-line-breaking"></a>
<a id="typing-line-breaking"></a>
#### 3.19.2 Line Breaking

Try to follow the existing [indentation](#indentation) rules. Always prefer
breaking between variables.

After annotating, many of the functions will become "one parameter per line".

```python {.good}
def my_method(self,
              first_var: int,
              second_var: Foo,
              third_var: Optional[Bar]) -> int:
  ...
```

However, if everything fits on the same line, go for it.

```python {.good}
def my_method(self, first_var: int) -> int:
  ...
```

If the combination of the function name, the last parameter, and the return type
is too long, indent by 4 in a new line.

```python {.good}
def my_method(
    self, first_var: int) -> Tuple[MyLongType1, MyLongType1]:
  ...
```

When the return type does not fit on the same line as the last parameter, the
preferred way is to indent the parameters by 4 on a new line and align the
closing parenthesis with the def.

```python {.good}
Yes:
def my_method(
    self, **kw_args: Optional[MyLongType]
) -> Dict[OtherLongType, MyLongType]:
  ...
```

`pylint` allows you to move the closing parenthesis to a new line and align
with the opening one, but this is less readable.

```python {.bad}
No:
def my_method(self,
              **kw_args: Optional[MyLongType]
             ) -> Dict[OtherLongType, MyLongType]:
  ...
```

As in the examples above, prefer not to break types. However, sometimes they are
too long to be on a single line (try to keep sub-types unbroken).

```python {.good}
def my_method(
    self,
    first_var: Tuple[List[MyLongType1],
                     List[MyLongType2]],
    second_var: List[Dict[
        MyLongType3, MyLongType4]]) -> None:
  ...
```

If a single name and type is too long, consider using an
[alias](#typing-aliases) for the type. The last resort is to break after the
colon and indent by 4.

```python {.good}
Yes:
def my_function(
    long_variable_name:
        long_module_name.LongTypeName,
) -> None:
  ...
```

```python {.bad}
No:
def my_function(
    long_variable_name: long_module_name.
        LongTypeName,
) -> None:
  ...
```

<a id="s3.19.3-forward-declarations"></a>
<a id="typing-forward-declarations"></a>
#### 3.19.3 Forward Declarations

If you need to use a class name from the same module that is not yet defined --
for example, if you need the class inside the class declaration, or if you use a
class that is defined below -- use a string for the class name.

```python {.good}
class MyClass(object):

  def __init__(self,
               stack: List["MyClass"]) -> None:
```

<a id="s3.19.4-default-values"></a>
<a id="typing-default-values"></a>
#### 3.19.4 Default Values

As per [PEP-008](https://www.python.org/dev/peps/pep-0008/#other-recommendations)
when combining an argument annotation with a default value, use spaces around
the = sign (but only for those arguments that have both an annotation and a
default).

```python {.good}
Yes:
def func(a: int = 0) -> int:
  ...
```
```python {.bad}
No:
def func(a:int=0) -> int:
  ...
```

<a id="s3.19.5-none-type"></a>
<a id="none-type"></a>
#### 3.19.5 NoneType

In the Python type system, `NoneType` is a "first class" type, and for typing
purposes, `None` is an alias for `NoneType`. If an argument can be `None`, it
has to be declared! You can use `Union`, but if there is only one other type,
`Optional` is a shortcut.

```python {.good}
Yes:
def func(a: Optional[str]) -> str:
  ...
```

```python {.bad}
No:
def func(a: Union[None, str]) -> str:
  ...
```

If the default value of an argument is `None`, marking the variable `Optional`
is optional.

```python {.good}
Yes:
def func(a: Optional[str] = None) -> str:
  ...
def func(a: str = None) -> str:
  ...
```

<a id="s3.19.6-aliases"></a>
<a id="typing-aliases"></a>
#### 3.19.6 Type Aliases

You can declare aliases of complex types. The name of an alias should be
CapWorded; try to describe the composed type and end with "Type" (or "Types" for
returned tuples). If the alias is used only in this module, it should be
\_Private.

For example, if the name of module together with the type is too long:

```python {.good}
SomeType = module_with_long_name.TypeWithLongName
```

Other examples are complex nested types and multiple return variables from a
function (as a tuple).

<a id="s3.19.7-ignore"></a>
<a id="typing-ignore"></a>
#### 3.19.7 Ignoring Types

You can disable type checking on a line with the special comment
`# type: ignore`.

`pytype` has a disable option for specific errors (similar to lint):

```python {.good}
# pytype: disable=attribute-error
```

<a id="s3.19.8-comments"></a>
<a id="typing-comments"></a>
#### 3.19.8 Typing internal variables

If an internal variable has a type that is hard or impossible to infer, you can
supply it as a special comment:

```python {.good}
a = SomeUndecoratedFunction()  # type: Foo
```
<a id="s3.19.9-tuples"></a>
<a id="typing-tuples"></a>
#### 3.19.9 Tuples vs Lists

Unlike Lists, which can only have a single type, Tuples can have either a single
repeated type or a set number of elements with different types. The latter is
commonly used as return type from a function.

```python {.good}
a = [1, 2, 3]  # type: List[int]
b = (1, 2, 3)  # type: Tuple[int, ...]
c = (1, "2", 3.5)  # type Tuple[int, str, float]
```

<a id="s3.19.10-type-var"></a>
<a id="typing-type-var"></a>
#### 3.19.10 TypeVar

The Python type system has
[generics](https://www.python.org/dev/peps/pep-0484/#generics). The factory
function `TypeVar` is a common way to use them.

Example:

```python {.good}
from typing import List, TypeVar
T = TypeVar("T")
...
def next(l: List[T]) -> T:
  return l.pop()
```

A TypeVar can be constrained:

```python {.good}
AddableType = TypeVar("AddableType", int, float, str)
def add(a: AddableType, b: AddableType) -> AddableType:
  return a + b
```

A common predefined type variable in the `typing` module is `AnyStr`. Use it for
arguments that can be `bytes` or `unicode`.

```python {.good}
AnyStr = TypeVar("AnyStr", bytes, unicode)
```
<a id="s3.19.11-strings"></a>
<a id="typing-strings"></a>
#### 3.19.11 Strings types

When annotating functions that take or return strings, avoid using `str`,
because it means different things in Python 2 and Python 3. In Python 2, `str`
is `bytes`; in Python 3, it is `unicode`. Whenever possible, it is best to be
explicit:

```python {.bad}
No:
def f(x: str) -> str:
  ...
```

For code that deals with byte arrays, use `bytes`.

```python {.good}
def f(x: bytes) -> bytes:
  ...
```

For code that processes Unicode data, use `Text`.

```python {.good}
from typing import Text
...
def f(x: Text) -> Text:
  ...
```

If the type can be either bytes or unicode, use `Union`.

```python {.good}
from typing import Text, Union
...
def f(x: Union[bytes, Text]) -> Union[bytes, Text]:
  ...
```

If all the string types of a function are always the same, for example if the
return type is the same as the argument type in the code above, use
[AnyStr](#typing-type-var).

Writing it like this will simplify the process of porting the code to Python 3.

<a id="s3.19.12-imports"></a>
<a id="typing-imports"></a>
#### 3.19.12 Imports For Typing

For classes from the `typing` module, always import the class itself. You are
explicitly allowed to import multiple specific classes on one line from the
`typing` module. Ex:

```python {.good}
from typing import Any, Dict, Optional
```

Given that this way of importing from `typing` adds items to the local
namespace, any names in `typing` should be treated similarly to keywords, and
not be defined in your Python code, typed or not. If there is a collision
between a type and an existing name in a module, import it using
`import x as y`.

```python {.good}
from typing import Any as AnyType
```

If the additional imports needed for type checking need to be avoided at
runtime, conditional imports may be used. This pattern is discouraged and
alternatives such as refactoring the code to allow top level imports should be
preferred. If this pattern is used at all, conditionally imported types need to
be referenced as strings `'sketch.Sketch'` rather than `sketch.Sketch`, to be
forward compatible with Python 3 where the annotation expressions are actually
evaluated. Imports that are needed only for type annotations can be placed
within an `if typing.TYPE_CHECKING:` block.

-   Only entities that are used solely for typing should be defined here; this
    includes aliases. Otherwise it will be a runtime error, as the module will
    not be imported at runtime.
-   The block should be right after all the normal imports.
-   There should be no empty lines in the typing imports list.
-   Sort this list as if it were a regular imports list, but put the import from
    the typing module at the end.
-   The `google3` module also has a `TYPE_CHECKING` constant. You can use that
    instead if you do you not want to import `typing` at runtime.


```python {.good}
import typing
...
if typing.TYPE_CHECKING:
  import types
  from MySQLdb import connections
  from google3.path.to.my.project import my_proto_pb2
  from typing import Any, Dict, Optional
```

<a id="s3.19.13-circular-deps"></a>
<a id="typing-circular-deps"></a>
#### 3.19.13 Circular Dependencies

Circular dependencies that are caused by typing are code smells. Such code is a
good candidate for refactoring. Although technically it is possible to keep
circular dependencies, the [build system](#typing-build-deps) will not let you
do so because each module has to depend on the other.

Replace modules that create circular dependency imports with `Any`. Set an
[alias](#typing-aliases) with a meaningful name, and use the real type name from
this module (any attribute of Any is Any). Alias definitions should be separated
from the last import by one line.

```python {.good}
from typing import Any

some_mod = Any  # some_mod.py imports this module.
...

def my_method(self, var: some_mod.SomeType) -> None:
  ...
```


## 4 Parting Words

*BE CONSISTENT*.

If you're editing code, take a few minutes to look at the code around you and
determine its style. If they use spaces around all their arithmetic operators,
you should too. If their comments have little boxes of hash marks around them,
make your comments have little boxes of hash marks around them too.

The point of having style guidelines is to have a common vocabulary of coding so
people can concentrate on what you're saying rather than on how you're saying
it. We present global style rules here so people know the vocabulary, but local
style is also important. If code you add to a file looks drastically different
from the existing code around it, it throws readers out of their rhythm when
they go to read it. Avoid this.

