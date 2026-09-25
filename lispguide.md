# Google Common Lisp Style Guide


## Introduction

This guide is not a Common Lisp tutorial. Rather, it recommends formatting,
structure, and stylistic choices for Common Lisp code. Maintainers of existing
code should balance these recommendations with the benefit of maintaining
consistency within existing code.

We welcome constructive feedback on how to improve this guide. If you find
mistakes in this document, you may file bugs in the
[GitHub issue tracker](https://github.com/google/styleguide/issues). Please put
"[Lisp]" in the issue title since the repository contains Style Guides for
several languages.


### References

-   For a guide to effective Lisp programming at Google, see
    [The Google Lisp Guide to Effective Programming](lispprogrammingguide.md).

-   For basic information about the language, please consult
    [Practical Common Lisp](https://www.gigamonkeys.com/book/).

-   For a language reference, please consult the
    [Common Lisp HyperSpec](https://www.lispworks.com/documentation/HyperSpec/Front/index.htm).

-   For more detailed style guidance, take (with a pinch of salt) a look at
    [Peter Norvig and Kent Pitman's style guide](https://www.cs.umd.edu/~nau/cmsc421/norvig-lisp-style.pdf).

## Existing Code

-   Fix old code as you go.
-   Don't do mass style fixes without warning.

A lot of Lisp code was written before these guidelines existed. You should fix
violations as you encounter them in the course of your normal coding. Only do so
when such fixes are easy to implement and do not greatly increase the size of
the change. In these cases, consider splitting the style fix into a separate
change.

You must not fix violations en masse without warning other developers and
coordinating with them, so as not to make the merging of large branches more
difficult than it already is.

## Formatting

### Punctuation, Spelling and Grammar

-   Use correct spelling in your comments and code.
-   Use proper grammar in your comments and documentation.

Pay attention to punctuation, spelling and grammar; it is easier to read
well-written comments than badly written ones.

Comments should be as readable as narrative text, with proper capitalization and
punctuation. In many cases, complete sentences are more readable than sentence
fragments. Shorter comments, such as comments at the end of a line of code, can
sometimes be less formal, but you should be consistent with your style.

### Line length

-   Format source code so that no line is longer than 100 characters.

Some line length restriction is better than none at all. While old text
terminals used to make 80 columns the standard, these days, allowing 100 columns
seems better, since good style encourages the use of descriptive variables and
function names.

### Form length

-   Prefer small and focused top-level forms.

Long top-level forms (such as functions and macros) are sometimes appropriate,
so no hard limit is placed on their length. If a function or macro exceeds about
40 lines, consider whether it can be broken up without harming the structure of
the program.

Even if your long form works perfectly now, someone modifying it in a few months
may add new behavior. This could result in bugs that are hard to find. Keeping
your forms short and simple makes it easier for other people to read and modify
your code.

Do not be intimidated by modifying existing code. If working with an overly long
function proves to be difficult -- errors are hard to debug, or a piece of it is
required in several different contexts -- consider breaking up the function into
smaller and more manageable pieces.

### Indentation

-   Use spaces, not tabs, to indent code.
-   Binding data of a binding form should be:
    -   indented four spaces when on a new line or
    -   aligned with the first binding data form otherwise.
-   Bodies of a binding form should be:
    -   indented two spaces when on a new line or
    -   aligned with the first form in the body otherwise.
-   Parameters of a function call should be
    -   aligned with the call itself when on a new line or
    -   aligned with the first parameter otherwise.
-   Special parameters in function and macro declarations (`&key`, `&optional`,
    ...) should be:
    -   aligned with the special parameter declaration when on a new line or
    -   aligned with the first special parameter otherwise.
-   Prefer fitting all parameters to a function:
    -   on a single line when possible, or
    -   one parameter per line otherwise.
-   Arguments to a loop form (loop keywords), and their arguments in turn should
    be:
    -   indented two spaces when the first argument is on a new line or
    -   aligned with the first argument otherwise.

Common Lisp indentation in Emacs is provided by the cl-indent library. The
latest version of cl-indent is packaged with
[SLIME](https://www.common-lisp.net/project/slime/) (under
contrib/slime-cl-indent.el). After installing SLIME, set up Emacs to load SLIME
automatically using
[these instructions](https://www.common-lisp.net/project/slime/doc/html/Loading-Contribs.html),
adding slime-indentation to the list of contrib libraries to be loaded in the
call to slime-setup.

Ideally, use the default indentation settings provided by SLIME. If necessary,
customize indentation parameters to maintain a consistent indentation style
throughout an existing project. Parameters can be customized using
the :variables setting in define-common-lisp-style. Indentation of specific
forms can be customized using the :indentation setting of
define-common-lisp-style. This is particularly useful when creating forms that
behave like macros or special operators that are indented differently than
standard function calls (e.g. defun, labels, or let). Add a
[hook](https://www.gnu.org/software/emacs/manual/html_node/emacs/Hooks.html) to
'lisp-mode-hook that calls common-lisp-set-style to set the appropriate style
automatically.


You should not include copyright information in individual source code files. An
exception is made for files meant to be disseminated as standalone.


### Vertical white space

-   Include one blank line between all top-level forms
    -   This may be omitted for simple (one-line), closely related forms.

You should include one blank line between top-level forms, such as function
definitions. Exceptionally, blank lines can be omitted between simple, closely
related defining forms of the same kind, such as a group of related type
declarations or constant definitions.

```lisp
(defconstant +mix32+ #x12b9b0a1 "pi, an arbitrary number")
(defconstant +mix64+ #x2b992ddfa23249d6 "more digits of pi")

(defconstant +golden-ratio32+ #x9e3779b9 "the golden ratio")
(defconstant +golden-ratio64+ #xe08c1d668b756f82 "more digits of the golden ratio")

(defmacro incf32 (x y)
  "Like INCF, but for integers modulo 2**32"
  `(setf ,x (logand (+ ,x ,y) #xffffffff)))
(defmacro incf64 (x y)
  "Like INCF, but for integers modulo 2**64"
  `(setf ,x (logand (+ ,x ,y) #xffffffffffffffff)))
```

Blank lines can be used to separate parts of a complicated function. Generally,
however, you should break a large function into smaller ones instead of trying
to make it more readable by adding vertical space. If you can't, you should
document with a `;;` comment what each of the separated parts of the function
does.

### Horizontal white space

-   Don't insert spaces after an opening parenthesis or before a closing
    parenthesis.
-   Insert a single space between function and macro parameters.
-   Don't use whitespace to horizontally align forms.
-   Don't have dangling parentheses except when closing a top-level `eval-when`
    form.

You must not include horizontal whitespace after an open parenthesis or before a
close parenthesis.

You must not place right parentheses by themselves on a line. A set of
consecutive trailing parentheses must appear on the same line.

```lisp
;; These parentheses pull more attention, hurting readability. This also isn't
;; conventional Lisp style.
    ( defun factorial ( limit )
      ( let (( product 1 ))
        ( loop for i from 1 upto limit
              do (setf product ( * product i ) ) )
        product
      )
    )
```

```lisp
;; This is easier to read, and avoids a hanging-braces style that is not
;; conventionally used by Lisp programmers.
(defun factorial (limit)
  (let ((product 1))
    (loop for i from 1 upto limit
          do (setf product (* product i)))
    product))
```

You should use only one space between forms.

You should not use spaces to vertically align forms in the middle of consecutive
lines. An exception is made when the code possesses an important yet otherwise
not visible symmetry that you want to emphasize.

```lisp
;; The cost of maintaining this sort of formatting and the inconsistent
;; horizontal spacing outweighs the readability benefit of vertical alignment.
(let* ((low    1)
       (high   2)
       (sum    (+ (* low low) (* high high))))
  ...)
```

```lisp
;; Consistent horizontal spacing is preferred.
(let* ((low 1)
       (high 2)
       (sum (+ (* low low) (* high high))))
  ...))
```

You must align nested forms if they occur across more than one line.

```lisp
;; Hard to visually grasp how deeply each form is nested.
(defun munge (a b c)
(* (+ a b)
c))
```

```lisp
;; Indentation helps the reader parse the nesting of forms.
(defun munge (a b c)
  (* (+ a b)
     c))
```

An exception to the rule against lonely parentheses is made for an `eval-when`
form around several definitions; in this case, include a comment `; eval-when`
after the closing parenthesis.

## Documentation

### Docstrings

-   Use docstrings whenever the language permits it.
-   Use docstrings for all top-level functions, types, classes, variables, and
    macros.
-   Document how to use a function, including its parameters, return values, and
    side effects, not how the code works.
-   When a specialization of a generic breaks the contract specified in the
    docstring, document that specialization. This must be avoided.

Unless some bit of code is painfully self-explanatory, document it with a
documentation string (also known as docstring).

Documentation strings are destined to be read by the programmers who use your
code. They can be extracted from functions, types, classes, variables and
macros, and displayed by programming tools, such as IDEs, or by REPL queries
such as `(describe 'foo)`; web-based documentation or other reference works can
be created based on them. Documentation strings are thus the perfect locus to
document your API. They should describe how to use the code (including what
pitfalls to avoid), as opposed to how the code works (and where more work is
needed), which is what you'll put in comments.

Supply a documentation string when defining top-level functions, types, classes,
variables and macros. Generally, add a documentation string wherever the
language allows.

For functions, the docstring should describe the function's contract: what the
function does, what the arguments mean, what values are returned, what
conditions the function can signal. It should be expressed at the appropriate
level of abstraction, explaining the intended meaning rather than, say, just the
syntax. In documentation strings, use uppercase for the names of Lisp symbols,
such as function arguments. For example, "The value of LENGTH must be an
integer."

```lisp
(defun small-prime-number-p (n)
  "True if N, an integer, is a prime number."
  ...)

(defgeneric clear-table (table)
  (:documentation
    "Like clrhash, empties TABLE of all associations, and returns TABLE."))
```

A long docstring may usefully begin with a short, single-sentence summary,
followed by the larger body of the docstring.

When the name of a type is used, the symbol may be quoted by surrounding it with
a back quote at the beginning and a single quote at the end. Emacs will
highlight the type, and the highlighting serves as a cue to the reader that M-.
will lead to the symbol's definition.

```lisp
(defun bag-tag-expected-itinerary (bag-tag)
  "Return a list of `legacy-pnr-pax-segment' objects representing
  the expected itinerary of the `bag-tag' object, BAG-TAG."
  ...)
```

Every method of a generic function should be independently documented when the
specialization affects what the method does, beyond what is described in its
generic function's docstring.

### Non-Obvious Code

-   When making a non-obvious bug fix, add a comment explaining the reason for
    the change and referencing the bug number.
-   When writing complicated code, add a comment explaining the need for the
    complication and what the code is doing.
-   When additional work needs to be done with code, include a TODO.
-   Take special care to document any declaration and use of Domain-Specific
    Languages (DSLs) in your code.

When you fix a bug, consider whether what the fixed code does is obviously
correct or not; if not, you must add a comment explaining the reason for the
code in terms of fixing the bug. Adding the bug number, if any, is also
recommended.

Comments are explanations to the future maintainers of the code. Even if you're
the only person who will ever see and touch the code, even if you're either
immortal and never going to quit, or unconcerned with what happens after you
leave (and have your code self-destruct in such an eventuality), you may find it
useful to comment your code. Indeed, by the time you revisit your code, weeks,
months or years later, you will find yourself a different person from the one
who wrote it, and you will be grateful to that previous self for making the code
readable.

You must comment anything complicated so that the next developer can understand
what's going on. (Again, the "hit by a truck" principle.)

Also use comments as a way to guide those who read the code, so they know what
to find where.

For code that uses obscure forms to accomplish a task, you must include a
comment stating the purpose of the form and the task it accomplishes.

For comments requiring special attention, such as incomplete code, TODO items,
questions, breakage, and danger, include a TODO comment indicating the type of
problem, its nature, and any notes on how it may be addressed.

Ideally a TODO comment should reference a bug number:

```lisp
;; TODO(b/1234567): use circular lists for fizzbuzz
```

However, it may also be a username or email address:

```lisp
;; TODO(zippy@foo.com): Refactor to provide a better API.
```

The main purpose is to provide a way to find out more information by looking up
the bug or the person. (Usually you should put your own username.)

Be specific when indicating times or software releases in a TODO comment and use
[YYYY-MM-DD](https://www.w3.org/TR/NOTE-datetime) format for dates to make
automated processing of such dates easier:

```lisp
;;--- TODO(brown): Remove this code after release 1.7 or before 2012-11-30.
```

You should design your DSL to be easy to read and understand by people familiar
with the domain.

You must properly document all your DSL.

Sometimes, your DSL is designed for terseness. In that case, it is important to
document what each program does, if it's not painfully obvious from the context.

Notably, when you use regular expressions (e.g. with the `CL-PPCRE` package),
you MUST ALWAYS put in a comment (usually a two-semicolon comment on the
previous line) explaining, at least basically, what the regular expression does,
or what the purpose of using it is. The comment need not spell out every bit of
the syntax, but it should be possible for someone to follow the logic of the
code without actually parsing the regular expression.

### Comment semicolons

-   Use three semicolons for top-level form comments.
-   Use two semicolons for comments inside top-level forms.
-   Use one semicolon for comments at the end of a line of code.
-   Include a space between the semicolons and text of the comment.

You should use three semicolons to begin comments that apply to the file or the
top-level forms.

Inside a top-level form, you should use two semicolons to begin a comment if it
appears between lines.

You should use one semicolon if it is a parenthetical remark and occurs at the
end of a line. You should use spaces to separate the comment from the code it
refers to so the comment stands out. You should try to vertically align
consecutive related end-of-line comments.

```lisp
;;; File-level comments or comments for large sections of code.

;;; Divisibility
;;; Comments that describe a group of definitions.

(defun divisorp (d n)
  (zerop (mod n d)))

(defun proper-divisors (n)
  ...)

(defun divisors (n)
  (cons n (proper-divisors n)))

;;; Prime numbers

(defun small-prime-number-p (n)
  (cond ((or (< n 2))
         nil)
        ((= n 2)   ; parenthetical remark here
         t)        ; continuation of the remark
        ((divisorp 2 n)
         nil)  ; different remark
        ;; Comment that applies to a section of code.
        (t
         (loop for i from 3 upto (sqrt n) by 2
               never (divisorp i n)))))
```

You should include a space between the semicolon and the text of the comment.

## Naming

### Symbol guidelines

-   Use all lowercase.
-   Use hyphens to separate words.
-   Follow the rules for
    [punctuation, spelling, and grammar](#punctuation-spelling-and-grammar).
-   Name symbols based on their intent, not their content. Exceptions for common
    suffixes, such as `-P` and `-V` may be made, but prefer other ways of
    conveying type information (including declarations and type-specific
    accessor functions) in most situations.
-   Function names, variable names, and filenames should be descriptive; eschew
    abbreviation.
-   Variables with limited scope may be abbreviated freely.

Use lower case for all symbols. Consistently using lower case makes searching
for symbol names easier and is more readable.

Note that Common Lisp is case-converting, and that the `symbol-name` of your
symbols will be upper case. Because of this case-converting, attempts to
distinguish symbols by case are defeated, and only result in confusion. While it
is possible to escape characters in symbols to force lower case, you should not
use this capability unless this is somehow necessary to inter-operate with
third-party software.

Place hyphens between all the words in a symbol. If you can't easily say an
identifier out loud, it is probably badly named.

You must not use `"/"` or `"."` instead of `"-"` unless you have a
well-documented overarching reason to, and permission from other hackers who
review your proposal.

```lisp
;; Bad
(defvar *default-contextname* "main")  ; Words run together
(defvar *maximum-widget-cnt* 200)      ; Abbreviation to save two characters
```

```lisp
;; Better
(defvar *default-context-name* "main") ; Words separated by dashes
(defvar *maximum-widget-count* 200)    ; Uses full words
```

There are [conventions](https://www.cliki.net/Naming+conventions) in Common Lisp
for the use of punctuation in symbols. You should not use punctuation in symbols
outside these conventions.

Give as descriptive a name as possible, within reason. Do not worry about saving
horizontal space as it is far more important to make your code immediately
understandable by a new reader.

Do not use abbreviations that are ambiguous for symbols with a wide scope; such
as `defvar`s or `defun`s. For abbreviations that are unfamiliar to readers
outside your project, domain-specific abbreviations, centrally document these
abbreviations. For symbols of limited scope, such as those bound within a
function, abbreviate freely.

```lisp
(defvar *n*)               ; Meaningless.
(defvar *nerr*)            ; Ambiguous abbreviation.
(defvar *n-comp-conns*)    ; Ambiguous abbreviation.
(defvar *wgc-connections*) ; Only your group knows what this stands for.
(defvar *pc-reader*)       ; Lots of things can be abbreviated "pc".
(defvar *cstmr-id*)        ; Deletes internal letters.
```

```lisp
(defvar *price-count-reader*)  ; No abbreviation.
(defvar *num-errors*);         ; "num" is a widespread convention.
(defvar *num-dns-connections*) ; Most people know what "DNS" stands for.
```

You should name a variable according to the high-level concept that it
represents, not according to the low-level implementation details of how the
concept is represented.

Thus, you should avoid embedding data structure or aggregate type names, such as
`list`, `array`, or `hash-table` inside variable names, unless you're writing a
generic algorithm that applies to arbitrary lists, arrays, hash-tables, etc. In
that case it's perfectly OK to name a variable `list` or `array`.

Indeed, you should be introducing new abstract data types with `defclass` or
`deftype`, whenever a new kind of intent appears for objects in your protocols.
Functions that manipulate such objects generically may then use variables the
name of which reflect that abstract type.

For example, if a variable's value is always a row (or is either a row or
`nil`), it's good to call it `row` or `first-row` or something like that. It is
alright if `row` has been `deftype`'d to `string` — precisely because you have
abstracted the detail away, and the remaining salient point is that it is a row.
You should not name the variable `string` in this context, except possibly in
low-level functions that specifically manipulate the innards of rows to provide
the suitable abstraction.

Be consistent. If a variable is named `row` in one function, and its value is
being passed to a second function, then call it `row` rather than, say, `value`
(this was a real case).

### Global variables and constants

-   Global constants should start and end with a plus character.
-   Global variables should start and end with an asterisk character.

The names of global constants should start and end with plus characters.

Global variable names should start and end with asterisks (also known in this
context as earmuffs).

In some projects, parameters that are not meant to be usually modified or bound
under normal circumstances (but may be during experimentation or exceptional
situations) should start (but do not end) with a dollar sign. If such a
convention exists within your project, you should follow it consistently.
Otherwise, you should avoid naming variables like this.

Common Lisp does not have global lexical variables, so a naming convention is
used to ensure that globals, which are dynamically bound, never have names that
overlap with local variables. It is possible to fake global lexical variables
with a differently named global variable and a `define-symbol-macro`. You should
not use this trick, unless you first publish a library that abstracts it away.

```lisp
(defconstant +hash-results+ #xbd49d10d10cbee50)
(defvar *maximum-search-depth* 100)
```

### Predicate names

-   For single-word predicate names, use a trailing `"p"`.
-   For multi-word predicate names, use a trailing `"-p"`.

You should name functions returning a generalized-Boolean value with a trailing
`"p"` or `"-p"`, to indicate that they are Boolean predicates. The value of
`nil` means "false", while any other value means "true". The returned value
should not have any other meaning beyond expressing the truth of the predicate.
Generally, you should use `"p"` when the rest of the function name is one word
and `"-p"` when it is more than one word.

A rationale for this convention is given in
[the CLtL2 chapter on predicates](https://www.cs.cmu.edu/Groups/AI/html/cltl/clm/node69.html).

Functions that return meaningful values beyond the truth value, for example
`cl:member`, should not be named with a `-p` or `p` suffix even if their return
value can be used as a
[generalized boolean](https://www.lispworks.com/documentation/HyperSpec/Body/26_glo_g.htm#generalized_boolean).

The suggested convention for naming Boolean variables is to suffix their names
equally with "-p" or "p" if there is no other convenient name that would express
their Boolean type.

### Omit library prefixes

-   Don't include a library or package name as a prefix within the name of
    symbols.

When naming a symbol (external or internal) in a package, you should not include
the package name as a prefix within the name of the symbol. Naming a symbol this
way makes it awkward to use from a client package accessing the symbol by
qualifying it with a package prefix, where the package name then appears twice
(once as a package prefix, another time as a prefix within the symbol name).

```lisp
(in-package #:varint)
(defun varint-length64 () ... )

(in-package #:client-code)
(defconst +padding+ (varint:varint-length64 +end-token+))  ; varint is repeated
```

```lisp
(in-package #:varint)
(defun length64 () ... )

(in-package #:client-code)
(defconst +padding+ (varint:length64 +end-token+))  ; reads nicely with package
```

An exception to the above rule is to include a prefix for the names of variables
that would otherwise be expected to clash with variables in packages that use
the current one. For instance, `ASDF` exports a variable `*asdf-verbose*` that
controls the verbosity of `ASDF` only, rather than of the entire Lisp program.

Symbols that correspond to standard, idiomatic Lisp expressions and would
contain the package name or a part of it in a non-prefix position are still to
be written with that package name or part. This includes the following idiomatic
Lisp expressions as example:

```lisp
;; Definition of the FOOBAR concept.
(foobar:define-foobar ...)
;; Iterate over elements of FOOBAR.
(foobar:do-foobar ...)
;; Establish a lexical scope dealing with some aspect of FOOBAR.
(foobar:with-frobed-foobar ...)
;; Constructors.
(foobar:make-foobar ...)
(foobar:new-foobar ...)
```

<a id="package-names"></a>
### Package names

-   Design package names to be usable as prefixes for symbols.
-   Usually, the last package name part will end up as an alias in other code.

Follow consistent conventions when choosing a package name. For packages that
are intended for wide use and may be exposed outside of your organization a good
rule of thumb is to use `<org>.<library>.<unit>`. For example, for a package
that contains generic utilities for writing macros found in the ACME company's
"core" library, use `acme.core.macro`. The use of the dot (.) as a separator
allows for tools to reason about hierarchical package structures and
organization. If a component of the package name is a compound noun use a hyphen
(-) to separate the words. For example, `ace.container.hash-table`. As with
other Lisp names, use lowercase, even for well-known abbreviations like "http".


Package prefixes should fit the names of the symbols those packages export. For
example, if you have an abstraction called `fifo`, and it is in a package of the
first type you'd have functions named things like `fifo-add-to` and
`fifo-clear-all`. If you design a package name to be used as a prefix, you'd
have names like `add-to` and `clear-all`, because the callers would be saying:

```lisp
(fifo:add-to ...)
(fifo:clear-all ...)
```

The below shows a redundant and arguably "ugly" symbol naming schema.

```lisp
(fifo:fifo-clear-all ...)
```

Prefer singular names for packages rather than plural. For example calls to the
function `ace.core.string:prefixp` will look like the following:

```lisp
(string:prefixp ...)
```

The above reads better than:

```lisp
(strings:prefixp ...)
```

### File names

-   Use hyphens for names of Lisp and related sources.
-   Use the ".lisp" file name extension. Use "-ci.cc" for C stubs.

The names of files should use hyphens (-) instead of underscores (\_).

The file names and directory structure should match package names, as much as
possible. When using a one package per file strategy, the part of a package name
following the last dot (.) should be the file name that contains that package.
e.g. the file ".../core/string.lisp" contains the package `ace.core.string`.

Lisp file names should end with ".lisp".

Source code files that contain C stubs for foreign function interface should end
with the "-ci.cc" suffix.

## Code structure and organization

### Packages

-   Use packages, preferring one-package-per-file design.

Lisp packages are used to demarcate namespaces. Usually, each system has its own
namespace. A package has a set of external symbols, which provide the interface
for the package's facilities to be used elsewhere.

The internal symbols of a package should never be referred to from other
packages. That is, you should never have to use the double-colon `::` construct
(e.g. `quake::hidden-function`). If you need to use double-colons to write real
production code, something is wrong and needs to be fixed.

As an exception, unit tests may use the internals of the package being tested.

The `::` construct is also useful for very temporary hacks, and at the REPL. But
if the symbol really is part of the externally-visible definition of the
package, export it.

At times it's necessary to expose some internals in order to allow for multiple
implementations of an API. Rather than exporting those internal symbols, create
a second package to export those symbols. The first package is for your normal
users to use, and the second is for the implementation and its extenders to use.

-   Design packages to be used via a package qualifier, not via `:use`.

If you add a new library package, e.g. `time`, it should be designed to be used
via a package prefix, `time:`, rather than by adding `:use time` to the using
package definitions. Correspondingly, try to avoid exporting symbols that repeat
the package name when possible. (`time:now` vs `time:current-time`.) Of course
avoiding all repetition isn't possible. For example, you might export a
`time:time` type and that's fine.

An exception can be made for internal implementation packages and for "core"
packages that are well-known and widely used. The choice of the type of package
will determine the names of most of the external symbols in that package.

-   Prefer `:import-from` over `:use`.

When defining a package and accessing symbols from another package that was
designed to be used without a package prefix, prefer the `:import-from`
directive over the `:use` directive. `:import-from` makes the dependencies more
explicit. However, if *many* symbols are being imported then `:use` may be
preferable.

-   Do not use package nicknames.

Package nicknames MUST NOT be used. Package nicknames tend to be a shorter
version of the long package name, usually abbreviated as an acronym.

```lisp
(defpackage :regression-test
  (:nicknames :rtest #-foo :rt))
```

This practice pollutes the universal space of Lisp package names and most likely
will be the source of name conflicts. Also, different users may choose to use
different nicknames throughout their code, thus reducing readability and the
ability to process the code with automatic tools that are agnostic to Lisp
package naming schemes.


-   Favor the one package per file design principle, instead of sharing a
    package across multiple files in a library.

    -   It reduces the number of concepts that need to be reasoned about when
        organizing the code. A file, package, namespace, unit ... all have a one
        to one correspondence.
    -   It directly documents the structure of the file/unit/package with
        explicit dependencies in the package definition. This is beneficial for
        the human readers and for automatic tools that can easily derive system
        and build information from the dependencies.
    -   It enforces a hierarchical, non-cyclic dependency between units of code.
        It is difficult to load and compile two such files with defined packages
        if they depend on each other in a circular fashion. This improves the
        software architecture and design.


-   Do not shadow `common-lisp` symbols.

Your package must not shadow (and thus effectively redefine) symbols that are
part of the Common Lisp language. That is, symbols in the `common-lisp`
(nickname `cl`) package. There are certain exceptions, but they should be very
well-justified and extremely rare:

-   If you are explicitly replacing a Common Lisp symbol by a safer or more
    fully featured version.
-   If you are defining a package not meant to be "used", and have a good reason
    to export a symbol that clashes with Common Lisp, such as `log:error` and
    `log:warn` and so on.

### CLOS

-   New uses of CLOS are disallowed; new print-object methods are allowed

## Language usage guidelines

### Mostly Functional Style

-   Use side-effects only when they result in better/clearer code:

Lisp is best used as a "mostly functional" language.

Avoid modifying local variables, try rebinding instead.

Avoid creating objects and then SETFing their slots. Prefer to set the slots
during initialization.

Make classes as immutable as possible, that is, avoid giving slots setter
functions if at all possible. (The slots can still be set via `with-slots`.)

Using a mostly functional style makes it much easier to write concurrent code
that is thread-safe. It also makes it easier to test the code. It often makes it
easier to reason about the code, because keeping track of program state in your
head is hard.

### Special variables

-   Use
    [special variables](https://www.lispworks.com/documentation/HyperSpec/Body/d_specia.htm#special)
    (such as those defined by
    [`defvar`](https://www.lispworks.com/documentation/HyperSpec/Body/m_defpar.htm#defvar))
    sparingly.

Use special (dynamically bound) variables sparingly, and only in cases where it
won't surprise the person reading the code, and where it offers significant
benefits.

Indeed, each special variable constitutes state. Developers have to mentally
track the state of all relevant variables when trying to understand what the
code does and how it does it; tests have to be written and run with all relevant
combinations; to isolate some activity, care has to be taken to locally bind all
relevant variables, including those of indirectly used modules. They can hide
precious information from being printed in a backtrace. Not only is there
overhead associated with each new variable, but interactions between variables
can make the code exponentially more complex as the number of such variables
increases. The benefits have to match the costs.

Note though that a special variable is not a global variable in the sense of a
global variable in, say, BASIC or C. As special variables can be dynamically
bound to a local value, they are much more powerful than global value cells
where all users necessarily interfere with each other.

Good candidates for such special variables are items for which "the current" can
be naturally used as prefix, such as "the current database connection" or "the
current business data source". They are singletons as far as the rest of the
code is concerned, and often passing them as an explicit argument does not add
anything to the readability or maintainability of the source code in question.

They can make it easier to write code that can be refactored. If you have a
request processing chain, with a number of layers that all operate upon a
"current" request, passing the request object explicitly to every function
requires that every function in the chain have a request argument. Factoring out
code into new functions often requires that these functions also have this
argument, which clutters the code with boilerplate.

Treat special variables as though they are per-thread variables. Do not provide
a default top-level binding unless there is a default value that is valid for
all threads. Each thread of control that needs the variable should bind it
explicitly. With this, any incorrect use of the variable will result in an
"unbound variable" error, and each thread will see its own value for the
variable. Variables with a default global value should usually be locally
re-bound at thread creation time.

### Assignment

-   Within a package, be consistent with package-level assignment forms.

There are several styles for dealing with assignment and side-effects; whichever
a given package is using, keep using the same consistently when hacking said
package. Pick a style that makes sense when starting a new package.

Regarding multiple assignment in a single form, there are two schools: the first
style groups as many assignments as possible into a single `setf` or `psetf`
form thus minimizing the number of forms with side-effects:

```lisp
(setf foo bar
      baz quux)
```

the second style splits assignments into as many individual `setf` (or `setq`,
see below) forms as possible, to maximize the chances of locating forms that
modify a kind of place by grepping for `(setf (foo ...`:

```lisp
(setf foo bar)
(setf baz quux)
```

A grep pattern must actually contain as many place-modifying forms as you may
use in your programs, which may make this rationale either convincing or moot
depending on the rest of the style of your code. Follow the convention used in
the package you are hacking. We recommend the first convention for new packages.

Regarding `setf` and `setq`, there are two schools: the first regards `setq` as
an archaic implementation detail, and avoids it entirely in favor of `setf`; the
second regards `setf` as an additional layer of complexity, and avoids it in
favor of `setq` whenever possible (i.e. whenever the assigned place is a
variable or symbol-macro). Follow the convention used in the package you are
hacking. We recommend the first convention for new packages.

In the spirit of a mostly pure functional style, which makes testing and
maintenance easier, we invite you to consider how to do things with the fewest
assignments.

### Assertions and Conditions


Code must not call `signal`. Use `error` instead.

Do not use `throw` and `catch` when the `restart` facility could be used
instead.

Do not use `restart` when `handler-bind` could be used instead.

Do not generically handle all conditions, e.g. type `t`, or use `ignore-errors`.
Instead, let unknown conditions propagate to the standard ultimate handler for
processing.

There are a few places where handling all conditions is appropriate, but they
are rare. The problem is that handling all conditions can mask program bugs. If
you need to handle "all conditions", you MUST handle only `error`, *not* `t` and
not `serious-condition`.

`(error (make-condition 'foo-error ...))` is equivalent to `(error 'foo-error
...)` — code must use the shorter form.

Do not signal conditions from inside the cleanup form of `unwind-protect` or
otherwise exit non-locally from cleanup handlers outside of the handler e.g.
`invoke-restart`.

Do not clean up by resignaling. If you do that, and the condition is not
handled, the stack trace will halt at the point of the resignal, hiding the
rest. And the rest is the part we really care about!

```lisp
(handler-case
  (catch 'ticket-at
    (etd-process-blocks))
  (error (c)
    (reset-parser-values)
      (error c)))  ; The origin of this error has been lost.
```

```lisp
(unwind-protect
  (catch 'ticket-at
    (etd-process-blocks))
  (reset-parser-values))  ; The error passes through but cleanup still happens
```

Do not return a condition object as one of a set of multiple values. Instead,
signal the condition to denote an unusual outcome.

Signal a condition to denote an unusual outcome, rather than relying on a
special return type.

### Type Checking and Declarations

-   Use `(declare (type ...))`:
    -   For the contracts of non-API functions only, and
    -   To perform optimization on low-level internal functions.
-   Use `check-type`:
    -   On special variables used as implicit arguments,
    -   On the contracts of API functions, and
    -   Where it may be useful in detecting input bugs.

If your function is using a special variable as an implicit argument, it's good
to put in a `check-type` for the special variable, for two reasons: to clue in
the person reading the code that this variable is being used implicitly as an
argument, and also to help detect bugs.

Using `(declare (type ...))` is the least-desirable mechanism to use because, as
Scott McKay puts it:

> The fact is, `(declare (type ...))` does different things depending on the
> compiler settings of speed, safety, etc. In some compilers, when speed is
> greater than safety, `(declare (type ...))` will tell the compiler "please
> assume that these variables have these types" *without* generating any
> type-checks. That is, if some variable has the value `1432` in it, and you
> declare it to be of type `string`, the compiler might just go ahead and use it
> as though it's a string.
>
> Moral: don't use `(declare (type ...))` to declare the contract of any API
> functions, it's not the right thing. Sure, use it for "helper" functions, but
> not API functions.

Use appropriate declarations in internal low-level functions where these
declarations are used for optimization. When you do, however, see our
recommendations for [Unsafe Operations](lispprogrammingguide.md#unsafe-operations).

## Meta-language guidelines

### Macros

-   Use macros to clearly express a repeated pattern.
-   Don't write a macro when a (possibly inlined) function would do.
-   Avoid writing overly complicated macros:
    -   Macro forms should only process syntax.
    -   Minimize macroexpanded code, delegating logic to an implementation
        function where appropriate (*call-with style*)
-   Macros should generally be hygienic, binding only symbols provided by the
    caller or generated by `gensym`.
-   Clearly document unhygienic aspects and side-effects of macros.
-   Only evaluate parameters to a macro once.
-   For macros with a `body` form, even if they have no parameters, include an
    empty `()` to allow for future enhancement without breaking callers.
-   Don't use regular macros to improve performance, use inlining.
-   Use compiler macros to improve performance as needed.
-   Avoid macros that define other macros. If you must use them, document
    carefully.
-   Obtain developer consensus before writing a reader macro.
-   Never let a reader macro leak out of the system using it.

Macros make your code clearer by providing syntactic abstraction. However, this
comes at a price in syntactic complexity, and macroexpanded forms are not as
easy to unit-test and debug as functions.

Never use a macro where a function will do. That is, if the semantics of what
you are writing conforms to the semantics of a function, write it as a function
rather than a macro. This advice also applies to local macros defined with
`macrolet`; use `flet` or `labels` instead where possible.

Reuse existing macros where possible. Only write complex macros when the gain in
expressiveness justifies the effort.

Complex macros should use
[*call-with style*](http://random-state.net/log/3390120648.html), where as much
logic as possible is delegated to a (possibly declared inline) auxiliary
function. Macro `&body` arguments are typically spliced into the body of a
lambda expression passed to the auxiliary function. Implementation function
names should follow the convention of prefixing the outer name with `%`. e.g. a
macro `foo` could pass a body lambda and other parameters to the function
`%foo`.

Symbols bound by a macro should generally either be provided by the caller or
generated with `gensym`. Since `gensym` generates fresh symbols, those symbols
can't appear in other forms passed by the caller. This prevents symbols from
being unexpectedly shadowed when the macroexpanded code is executed
([*variable capture*](https://www.bookshelf.jp/texi/onlisp/onlisp_10.html)); a
macro that upholds this property is referred to as *hygienic*. Pass a string as
the optional parameter for `gensym` to provide the generated symbol a
human-readable name. The `alexandria:with-gensyms` macro provides a convenient
way to generate such symbols.

If a macro must bind other symbols (e.g. global variables) during the execution
of caller-provided forms, that aspect of its interface must be clearly
documented. Side effects of forms in a macroexpansion that are not passed by the
caller should also be clearly documented.

If a macro call contains a form to be used in the macroexpanded code, that form
should be expanded only once, and evaluated only the number of times that would
be expected by the caller. Expanding code more than once (especially `&body`
forms) results in less readable macroexpansions and larger binary sizes.
`alexandria:once-only` provides a convenient way to evaluate a user-provided
form and bind it to a freshly-generated symbol. Using `call-with` style makes it
easier to uphold this property, since forms can be evaluated once in the call to
the auxiliary function.

If a form needs to be evaluated in multiple branches of the macroexpanded code,
it can be spliced into a local function definition instead, with each branch
calling that function. In that case, the local function should be given a unique
gensym name with `flet` and declared dynamic-extent (if applicable).

When you write a macro with a body, such as a `with-xxx` macro, even if there
aren't any parameters, you should leave space for them anyway. For example, if
you define `with-lights-on`, do not structure it like this:

```lisp
(defmacro with-lights-on (&body b)
  ...)

;; Example call
(with-lights-on
  ...)
```

Instead, add an empty arguments list before the body argument:

```lisp
;; Macro lambda list has empty parens before body argument
(defmacro with-lights-on (() &body b)
  ...)

;; Call has empty arguments list before body forms
(with-lights-on ()
  ...)
```

That way, you can later add optional or keyword parameters without having to
change all the uses of the macro:

```lisp
(defmacro with-lights-on ((&keyword install-new-bulbs-p) &body b)
  ...)

;; Calls that don't use the optional parameter don't need update
(with-lights-on ()
  ...)

;; Other calls can use the new parameter
(with-lights-on (:install-new-bulbs-p t)
  ...)
```

You must not transform a function into a macro for performance reasons. If
profiling shows that you have a performance problem with code being part of a
function body instead of expanded inline, document the need and profiling
results appropriately, and `(declaim (inline <function-name>))`.

You can also use a compiler-macro as a way to speed up function execution by
specifying a source-to-source transformation. Beware that it interferes with
tracing the optimized function.

When you write a macro-defining macro (a macro that generates macros), document
and comment it particularly clearly, since these are harder to understand.

You must not install new reader macros without a consensus among the developers
of your system. Reader macros must not leak out of the system that uses them to
clients of that system or other systems used in the same project. You must use
software such as `cl-syntax` or `named-readtables` to control how reader macros
are used. Clients should be able to choose whether or not to use the same reader
macros as you do: your system must be usable even to clients who do not use
these reader macros.

### Read-time evaluation

-   Avoid using the `#.` reader macro:
    -   Prefer using `eval-when` and `defconstant`.
-   Avoid read-time side-effects.

The `#.` standard read-macro will read one object, evaluate the object, and have
the reader return the resulting value.

You must not use it where other idioms will do, such as using `eval-when` to
evaluate side-effects at compile-time, using a regular macro to return an
expression computed at compile-time, using `load-time-value` to compute it at
load-time.

Read-time evaluation is often used as a quick way to get something evaluated at
compile time (actually "read time" but it amounts to the same thing). If you use
this, the evaluation MUST NOT have any side effects and MUST NOT depend on any
variable global state. The `#.` should be treated as a way to force
"constant-folding" that a sufficiently-clever compiler could have figure out all
by itself, when the compiler isn't sufficiently-clever and the difference
matters.

Another use of `#.` is to expand the equivalent of macros in places that are
neither expressions nor (quasi)quotations, such as lambda-lists. However, if you
find yourself using it a lot, it might be time to instead define macros to
replace your consumers of lambda-lists with something that recognizes an
extension.

Whenever you are going to use `#.`, you should consider using `defconstant` and
its variants, possibly in an `eval-when`, to give the value a name explaining
what it means.

### EVAL

-   Never use `eval` at runtime in production code.

Places where it is actually appropriate to use `eval` are so few and far between
that you must consult with your reviewers; it's easily misused.

If your code manipulates symbols at runtime and needs to get the value of a
symbol, use `symbol-value`, not `eval`.

Often, what you really need is to write a macro, not to use `eval`.

You may be tempted to use `eval` as a shortcut to evaluating expressions in a
safe subset of the language. But it often requires more scrutiny to properly
check and sanitize all possible inputs to such use of `eval` than to build a
special-purpose evaluator. You must not use `eval` in this way at runtime.

Places where it is OK to use `eval` are:

-   The implementation of an interactive development tool.
-   The build infrastructure.
-   Backdoors that are part of testing frameworks. (You MUST NOT have such
    backdoors in production code.)
-   Macros that fold constants at compile-time.
-   Macros that register definitions to meta-data structures; the registration
    form is sometimes evaluated at compile-time as well as included in the
    macro-expansion, so it is immediately available to other macros.

Note that in the latter case, if the macro isn't going to be used at the
top-level, it might not be possible to make these definitions available as part
of the expansion. The same phenomenon may happen in a `deftype` expansion, or in
helper functions used by macros. In these cases, you may actually have to use
`asdf-finalizers:eval-at-toplevel` in your macro. It will not only `EVAL` your
definitions at macro-expansion time for immediate availability, it will also
save the form aside, for inclusion in a `(asdf-finalizers:final-forms)` that you
need to include at the end of the file being compiled (or before the form is
needed). This way, the side-effects are present when loading the fasl without
having compiled it as well as while compiling it; in either case, the form is
made available at load-time. `asdf-finalizers` ensures that the form is present,
by throwing an error if you omit it.

### INTERN and UNINTERN

-   Never use `intern` or `unintern` at runtime.

You must not use `intern` at runtime. Not only does it cons, it either creates a
permanent symbol that won't be collected or gives access to internal symbols.
This creates opportunities for memory leaks, denial of service attacks,
unauthorized access to internals, clashes with other symbols.

You must not `intern` a string just to compare it to a keyword; use `string=` or
`string-equal`.

```lisp
(member (intern str :keyword) $keys)  ; intern has undesired side-effects
```

```lisp
  (member str $keys :test #'string-equal)
;; Compares without interning
```

Note: string-equal uses the `symbol-name` for comparison when given a symbol.

You must not use `unintern` at runtime. It can break code that relies on dynamic
binding. It makes things harder to debug. You must not dynamically intern any
new symbol, and therefore you need not dynamically unintern anything.

You may of course use `intern` at compile-time, in the implementation of some
macros. Even so, it is usually more appropriate to use abstractions on top of
it, such as `alexandria:symbolicate` or `alexandria:format-symbol` to create the
symbols you need.

## Data Representation

### Using NIL

-   Use `nil` to represent false or an unspecified value that cannot be `nil`.
-   Use a symbol to represent the absence of a value or an unspecified value
    that can be `nil`.

`nil` can have several different interpretations:

-   "False." In this case, use `nil`. You should test for false `nil` using the
    operator `not` or using the predicate function `null`.
-   "Empty-list." In this case, use `nil`. You should use `endp` to test for the
    empty list when the argument is known to be a proper list, or with `null`
    otherwise.
-   A statement about some value being unspecified. In this case, you may use
    `nil` if there is no risk of ambiguity anywhere in your code; otherwise you
    should use an explicit, descriptive symbol.
-   A statement about some value being known not to exist. In this case, you
    should use an explicit, descriptive symbol instead of `nil`.

You must not introduce ambiguity in your data representations that will cause
headaches for whoever has to debug code. If there is any risk of ambiguity, you
should use an explicit, descriptive symbol or keyword for each case, instead of
using `nil` for either. If you do use `nil`, you must make sure that the
distinction is well documented.

In many contexts, instead of representing "I don't know" as a particular value,
you should instead use multiple values, one for the value that is known if any,
and one to denote whether the value was known or found.

When working with database classes, keep in mind that `nil` need not always map
to `null` (and vice-versa)! The needs of the database may differ from the needs
of the Lisp.

### Lists

-   Use lists only for containers of elements of a like type.
-   Use lists only for sequential access.
-   Use lists for literal constants that will be transformed into data
    structures at compile- or load-time.
-   Prefer proper lists to improper lists
-   Use `first`, `second`, ... and `rest` to access a proper list.
-   Use `car` and `cdr` to access a improper list.
-   Avoid using lists as sets, except for very small sets.

Even though back in 1958, LISP was short for "LISt Processing", its successor
Common Lisp has been a modern programming language with modern data structures
since the 1980s. You must use the proper data structures in your programs.

You must not abuse the built-in (single-linked) `list` data structure where it
is not appropriate, even though Common Lisp makes it especially easy to use it.

You should avoid using a list as anything besides a container of elements of
like type.

You must only use lists when their performance characteristics is appropriate
for the algorithm at hand: sequential iteration over the entire contents of the
list.

An exception where it is appropriate to use lists is when it is known in advance
that the size of the list will remain very short (say, fewer than 16 elements).

List data structures are often (but not always) appropriate for macros and
functions used by macros at compile-time: indeed, not only is source code passed
as lists in Common Lisp, but the macro-expansion and compilation processes will
typically walk over the entire source code, sequentially, once. (Note that
advanced macro systems don't directly use lists, but instead use abstract syntax
objects that track source code location and scope; however there is no such
advanced macro system in Common Lisp at this time.)

Another exception where it is appropriate to use lists is for introducing
literal constants that will be transformed into more appropriate data structures
at compile-time or load-time. It is a good to have a function with a relatively
short name to build your program's data structures from such literals.

In the many cases when lists are not the appropriate data structure, various
libraries such as [cl-containers](https://cliki.net/cl-containers) or
[lisp-interface-library](https://cliki.net/lisp-interface-library) provide
plenty of different data structures that should fulfill all the basic needs of
your programs. If the existing libraries are not satisfactory, see the notes
about [Using Libraries](lispprogrammingguide.md#using-libraries).

For cases where a list is the correct data structure, prefer proper lists to
improper lists. Use improper lists only for lists with limited scope where
performance is critical.

For proper lists: Use `first` to access the first element of a list, `second` to
access the second element, etc. Use `rest` to access the tail of a list. Use
`endp` to test for the end of the list.

For improper lists: Use `car` to access the first element of a list. Use `cdr`
to access the tail of a list. Use `consp` to test for the end of the list.

Exceptionally, you may use `cdadr` and other variants on lists when manually
destructuring them, instead of using a combination of several list accessor
functions. In this context, using `car` and `cdr` instead of `first` and `rest`
also makes sense. However, keep in mind that it might be more appropriate in
such cases to use higher-level constructs such as `destructuring-bind` or
`optima:match`.

This should be rare outside of alists, since you should be using structures and
classes where they apply, and data structure libraries when you want trees.

Using lists as representations of sets is a bad idea unless you know the lists
will be small, because accessors are *O(n)* instead of *O(log n)*. For
arbitrarily big sets, use balanced binary trees, for instance using
`lisp-interface-library`.

```lisp
(member foo (union list-1 list-2))  ; Slow O(n) best-case and creates a new list
```

```lisp
(or (member foo list-1) (member foo list-2))  ; O(n) average-case
```

Indeed, `union` not only conses unnecessarily, but it can be *O(n\^2)* on some
implementations, and is rather slow even when it's *O(n)*.

### Arrays

-   Use arrays for homogeneous sets accessed non-sequentially.
-   Use arrays where random access matters.

`elt` has *O(n)* behavior when used on lists. If you are to use random element
access on an object, use arrays and `aref` instead.

The exception is for code outside the critical path where the list is known to
be small anyway.

### Structures and Classes

-   Use structures or classes for groups of heterogeneous types.
-   Use structures or classes for returning multiple values that will not be
    deconstructed immediately.

You must not use a list as a method of passing multiple separate values of
different types in and out of function calls. Sometimes it is convenient to use
a list as a little ad hoc structure, i.e. "the first element of the list is a
FOO, and the second is a BAR", but this should be used minimally since it is
difficult to remember the little convention. You must only use a list that way
when destructuring the list of arguments from a function, or creating a list of
arguments to which to `apply` a function.

The proper way to pass around an object comprising several values of
heterogeneous types is to use a structure as defined by `defstruct` or
`defclass`.

You should use multiple values only when your function returns a small number of
values that are meant to be used immediately by the caller, rather than passed
together as arguments to further functions.

### Pairs

-   Use pairs rarely, and only when representing exactly two values of
    homogeneous types that are closely related.
-   Use `car` and `cdr` for pairs.
-   Use `null` and `nil` with pairs.

When a cons cell is being used to store a pair of related objects, use `car` and
`cdr`. Use `null` to test for `nil` in this context.

## Proper Forms

You must follow the proper usage regarding well-known functions, macros and
special forms.

### Defining Functions

-   Avoid using `&aux` and `&allow-other-keys`.
-   Avoid using `&optional` and `&key` arguments together.
-   Avoid excessive nesting of binding forms in a function
    -   Break the function apart instead.
    -   Consider using a `nest` macro.

You should avoid using `&allow-other-keys`, since it blurs the contract of a
function. Almost any real function (generic or not) allows a certain fixed set
of keywords, as far as its caller is concerned, and those are part of its
contract. If you are implementing a method of a generic function, and it does
not need to know the values of some of the keyword arguments, you should
explicitly `(declare (ignore ...))` all the arguments that you are not using.
You must not use `&allow-other-keys` unless you explicitly want to disable
checking of allowed keys for all methods when invoking the generic function on
arguments that match this particular method. Note that the contract of a generic
function belongs in the `defgeneric`, not in the `defmethod` which is basically
an "implementation detail" of the generic function as far as the caller of the
generic is concerned.

A case where `&allow-other-keys` is appropriate is when you write a wrapper
function to other some other functions that may vary (within the computation or
during development), and pass around a plist as a `&REST` argument.

You should avoid using `&aux` arguments.

You should avoid having both `&optional` and `&key` arguments because the
keyword arguments can't be used when only some of the optional arguments are
specified. You must not have non-`nil` defaults to your `&optional` arguments
when your function has both `&optional` and `&key` arguments.

For maximum portability of a library, it is good form that `defmethod`
definitions should `(declare (ignorable ...))` all the required arguments that
they are not using. Indeed, some implementations will issue a warning if you
`(declare (ignore ...))` those arguments, whereas other implementations will
issue a warning if you fail to `(declare (ignore ...))` them. `(declare
(ignorable ...))` works on all implementations.

You should avoid excessive nesting of binding forms inside a function. If your
function ends up with massive nesting, you should probably break it up into
several functions or macros. If it is really a single conceptual unit, consider
using a macro such as `fare-utils:nest` to at least reduce the amount of
indentation required. It is bad form to use `nest` in typical short functions
with 4 or fewer levels of nesting, but also bad form not to use it in the
exceptional long functions with 10 or more levels of nesting. Use your judgment
and consult your reviewers.

### \#'FUN vs. 'FUN

-   Refer to a function as `#'FUN` rather than `'FUN`, unless:
    -   Accessing global function bindings or
    -   Dynamic linking is desired.

The former, which reads as `(function fun)`, refers to the function object, and
is lexically scoped. The latter, which reads as `(quote fun)`, refers to the
symbol, which when called uses the global `fdefinition` of the symbol.

When using functions that take a functional argument (e.g., `mapcar`, `apply`,
`:test` and `:key` arguments), you should use the `#'` to refer to the function,
not just single quote.

An exception is when you explicitly want dynamic linking, because you anticipate
that the global function binding will be updated.

Another exception is when you explicitly want to access a global function
binding, and avoid a possible shadowing lexical binding. This shouldn't happen
often, as it is usually a bad idea to shadow a function when you will want to
use the shadowed function; just use a different name for the lexical function.

You must use `(lambda ...)` without the function-quote `#'` notation. Unlike the
case of `#'symbol` vs `'symbol`, there is no change in meaning. The shorter
macro form expands into the function-quote form, thus, making the longer
notation unnecessary.

### Conditional Expressions

-   Use `when` and `unless` when there is one alternative.
-   Use `if` when there are two alternatives.
-   Don't use `if` when one of the clauses would be a `progn`, prefer one of the
    forms below.
-   Prefer `cond`, `case`, or its variants to nested `if` statements.
-   Prefer `and` and `or` when:
    -   They lead to more concise code.
    -   There are no side effects outside of an optional `error` as the last
        clause of an `or`.
-   Prefer `ecase` and `etypecase` to `case` and `typecase`.
-   Don't use `ccase` or `ctypecase`.
-   See also the [Pitfalls](lispprogrammingguide.md#case-and-ecase) section for
    common pitfalls when using `case` and `ecase`.

Use `when` and `unless` when there is only one alternative. Use `if` when there
are two alternatives and `cond` when there are several.

However, don't use `progn` for an `if` clause — use `cond`, `when`, or `unless`.

Note that in Common Lisp, `when` and `unless` return `nil` when the condition is
not met. You may take advantage of it. Nevertheless, you may use an `if` to
explicitly return `nil` if you have a specific reason to insist on the return
value. You may similarly include a fall-through clause `(t nil)` as the last in
your COND, or `(otherwise nil)` as the last in your CASE, to insist on the fact
that the value returned by the conditional matters and that such a case is going
to be used. You should omit the fall-through clause when the conditional is used
for side-effects.

You should prefer `and` and `or` when it leads to more concise code than using
`if`, `cond`, `when` or `unless`, and there are no side-effects involved. You
may also use an `error` as a side-effect in the final clause of an `or`.

You should use `ecase` and `etypecase` in preference to `case` and `typecase`.
It is better to catch erroneous values early.

```lisp
(case x ; Bad: silently returns NIL on mismatch
  ((bar) :bar)
  ((baz) :baz))
```

```lisp
(ecase x ; Better: will error on mismatch
  ((bar) :bar)
  ((baz) :baz))
```

You should not use `ccase` or `ctypecase` at all. At least, you should not use
them in server processes, unless you have quite robust error handling
infrastructure and make sure not to leak sensitive data this way. These are
meant for interactive use, and can cause interesting damage if they cause data
or control to leak to attackers.

### Comparison Operators

-   Use `eq` and `eql` appropriately, prefer `eql` for non-performance-critical
    code, all other things being equal.
-   Use `:START` and `:END` arguments to `string=` or `string-equal` instead of
    using `subseq`.
-   Use `zerop`, `plusp`, or `minusp` instead of comparing to `0` or `0.0`.
-   See also [Comparison Operators](lispprogrammingguide.md#comparison-operators) in
    the programming guide for proper usage.

When choosing between `eq` and `eql`, you should use `eql` unless you are
writing performance-critical low-level code. `eql` reduces the opportunity for a
class of embarrassing errors (i.e. if numbers or characters are ever compared).
There may be a tiny performance cost relative to `eq`, although under SBCL, it
often compiles away entirely. `eq` is equivalent to `eql` and type declarations,
and use of it for optimization should be treated just like any such
[unsafe operations](lispprogrammingguide.md#unsafe-operations).

Also, you should use `:start` and `:end` arguments to `string=` or
`string-equal` instead of using `subseq`; e.g. `(string-equal (subseq s1 2 6)
s2)` should instead be `(string-equal s1 s2 :start1 2 :end1 6)` This is
preferable because it is clearer and does not cons.

You should use `zerop`, `plusp`, or `minusp`, instead of comparing a value to
`0` or `0.0`.

### Iteration

-   Prefer the `dolist` or `dotimes` forms to `loop` in simple cases.
-   Prefer `with` within a `loop` to a `let` binding:
    -   Unless the `let` makes the code clearer.
    -   `let` may also be used to avoid a `finally (return ...)` form.
-   Do not set iteration variables in the body of an iteration macro.
-   Generally, prefer unadorned symbols for `loop` keywords unless for
    consistency or in macro-expansions.

You should simpler forms such as `dolist` or `dotimes` instead of `loop` in
simple cases when you're not going to use any of the `loop` facilities such as
bindings, collection or block return.

Use the `with` clause of `loop` when it will avoid a level of nesting with
`let`. You may use `let` if it makes it clearer to return one of bound variables
after the `loop`, rather than use a clumsy `finally (return ...)` form.

In the body of a `dotimes`, do not set the iteration variable.

Most systems use unadorned symbols in the current package as `loop` keywords
instead of `:keywords` from the `keyword` package. Prefer this approach, except
when:

*   That does not match the convention used in surrounding code.
*   The `loop` form is generated by a macro, and using unadorned keywords would
    result in a less-readable macro-expansion.

### I/O

-   Use logging tools, don't write directly to `*standard-output*` or
    `*error-output*`.
-   Don't use `print-object` for production interfaces.
-   Don't use multiple `write-` forms where a single `format` could be used.
-   Prefer `write-char` for single characters.
-   Prefer `princ-to-string` to `(format nil "~A" value)`.
-   Use `~<NEWLINE>` or `~@<NEWLINE>` in format strings to meet editor line
    length limits.
-   Use `"~:@(~A~)"` or `"~(~A~)"` to change the case of a format control
    parameter.

When writing a server, code must not send output to the standard streams such as
`*standard-output*` or `*error-output*`. Instead, code must use the proper
logging framework to output messages for debugging. We are running as a server,
so there is no console!

Code must not use `print-object` to communicate with a user — `print-object` is
for debugging purposes only. Modifying any `print-object` method must not break
any public interfaces.

You should not use a sequence of `write-xxx` where a single `format` string
could be used. Using format allows you to parameterize the format control string
in the future if the need arises.

You should use `write-char` to emit a character rather than `write-string` to
emit a single-character string.

You should not use `(format nil "~A" value)`; you should use `princ-to-string`
instead.

You should use `~<Newline>` or `~@<Newline>` in format strings to keep them from
wrapping in 100-column editor windows, or to indent sections or clauses to make
them more readable.

You should not use `string-upcase` or `string-downcase` on format control
parameters; instead, it should use `"~:@(~A~)"` or `"~(~A~)"`.
