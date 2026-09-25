# Google Common Lisp Effective Programming


## Introduction

This document is intended as a supplement to the
[Lisp Style Guide](lispguide.md). It is intended to cover things not related to
style, but that are important to new Lisp Programmers. The three main topics
covered include common optimization techniques, as well as common pitfalls for
new Lisp programmers.

## Optimization

### Using Libraries

-   Prefer using existing libraries to re-implementing.
-   You may re-implement a library when:

    -   there is a well-documented performance need, or
    -   you require specialized functionality that existing libraries do not
        provide.

-   You MUST NOT start a new library unless you established that none is already
    available that can be fixed or completed into becoming what you need. That's
    a rule against the NIH syndrome ("Not Invented Here"), which is particularly
    strong amongst Lisp hackers.

-   Whichever library, old or new, you pick, you MUST get permission to
    incorporate third-party code into the code base. You must discuss the use of
    such library in the appropriate mailing-list, and have your code reviewed by
    people knowledgeable in the domain and/or the Lisp library ecosystem (if
    any). Please be ready to argue why this particular solution makes sense as
    compared to other available libraries.

-   Some libraries are distributed under licenses not compatible with the
    software you're writing, and must not be considered available for use. Be
    aware of these issues, or consult with people who are.


### Avoid Allocation

-   Make sure objects are no longer reachable after they're no longer needed.
-   Don't `CONS` unnecessarily.

In a language with automatic storage management (such as Lisp or Java), the
colloquial phrase "memory leak" refers to situation where storage that is not
actually needed nevertheless does not get deallocated, because it is still
reachable.

You should be careful that when you create objects, you don't leave them
reachable after they are no longer needed!

Here's a particular trap-for-the-unwary in Common Lisp. If you make an array
with a fill pointer, and put objects in it, and then set the fill pointer back
to zero, those objects won't be garbage collected: the Common Lisp spec says
that it's still OK to refer to the array entries past the end of the fill
pointer. Note this also means that `VECTOR-POP` does not remove the element
returned from the underlying array's storage.

Don't cons (i.e., allocate) unnecessarily. Garbage collection is not magic.
Excessive allocation is usually a performance problem.

### Unsafe Operations

-   Don't define or use unsafe operations unless:
    -   The code has been profiled and there is a need for them.
    -   There is documentation indicating why it is safe to use them.

Common Lisp implementations often provide backdoors to compute some operations
faster in an unsafe way. For instance, some libraries provide arithmetic
operations that are designed to be used with fixnums only, and yield the correct
result faster if provided proper arguments. The downside is that the result of
such operations is incorrect in case of overflow, and can have undefined
behavior when called with anything but fixnums.

For instance, QPX, and QRes (in QUUX), define fixnum-optimized operators
prefixed with `I`, e.g. `I+`, `I-`, `I*`, `I=`, `I<`, `I>`, etc.

More generally, unsafe operations will yield the correct result faster than
would the equivalent safe operation if the arguments satisfy some invariant such
as being of the correct type and small enough; however if the arguments fail to
satisfy the required invariants, then the operation may have undefined behavior,
such as crashing the software, or, which is sometimes worse, silently giving
wrong answers. Depending on whether the software is piloting an aircraft or
other life-critical device, or whether it is accounting for large amounts money,
such undefined behavior can kill or bankrupt people. Yet proper speed can
sometimes make the difference between software that's unusably slow and software
that does its job, or between software that is a net loss and software that can
yield a profit.

You must not define or use unsafe operations without both profiling results
indicating the need for this optimization, and careful documentation explaining
why it is safe to use them. Unsafe operations should be restricted to internal
functions; you should carefully documented how unsafe it is to use these
functions with the wrong arguments. You should only use unsafe operations inside
functions internal to a package and you should document the use of the
declarations, since calling the functions with arguments of the wrong type can
lead to undefined behavior. Use `check-type` in functions exported from a
package to sanitize input arguments, so that internal functions are never passed
illegal values.

On some compilers, new unsafe operations can usually be defined by combining
type declarations with an `OPTIMIZE` declaration that has sufficiently high
`SPEED` and low `SAFETY`. In addition to providing more speed for production
code, such declarations may more helpful than `check-type` assertions for
finding bugs at compile-time, on compilers that have type inference. These
compilers may interpret those declarations as assertions if you switch to safer
and slower optimize settings; this is good to locate a dynamic error in your
code during development, but is not to be used for production code since it
defeats the purpose of declarations as a performance trick.


### DYNAMIC-EXTENT

-   Treat `DYNAMIC-EXTENT` as an unsafe operation, profile any code using it and
    document why it's safe.
-   Have confidence the underlying code won't change to falsify your
    assumptions/documentation.

`DYNAMIC-EXTENT` declarations are a particular case of
[unsafe operations](#unsafe-operations).

The purpose of a `DYNAMIC-EXTENT` declaration is to improve performance by
reducing garbage collection in cases where it appears to be obvious that an
object's lifetime is within the "dynamic extent" of a function. That means the
object is created at some point after the function is called, and the object is
always inaccessible after the function exits by any means.

By declaring a variable or a local function `DYNAMIC-EXTENT`, the programmer
*asserts* to Lisp that any object that is ever a value of that variable or the
closure that is the definition of the function has a lifetime within the dynamic
extent of the (innermost) function that declares the variable.

The Lisp implementation is then free to use that information to make the program
faster. Typically, Lisp implementations can take advantage of this knowledge to
stack-allocate:

-   The lists created to store `&REST` parameters.
-   Lists, vectors and structures allocated within a function.
-   Closures.

If the assertion is wrong, i.e. if the programmer's claim is not true, the
results can be *catastrophic*: Lisp can terminate any time after the function
returns, or it can hang forever, or — worst of all — it can produce incorrect
results without any runtime error!

Even if the assertion is correct, future changes to the function might introduce
a violation of the assertion. This increases the danger.

In most cases, such objects are ephemeral. Modern Lisp implementations use
generational garbage collectors, which are quite efficient under these
circumstances.

Therefore, `DYNAMIC-EXTENT` declarations should be used sparingly. You must only
use them if:

1.  There is some good reason to think that the overall effect on performance is
    noticeable, and
2.  It is absolutely clear that the assertion is true.
3.  It is quite unlikely that the code will be changed in ways that cause the
    declaration to become false.

Point (1) is a special case of the principle of avoiding premature optimization.
An optimization like this only matters if such objects are allocated at a very
high rate, e.g. "inside an inner loop".

Note that is relatively easy to ascertain that a function will not escape the
dynamic extent of the current call frame by analyzing where the function is
called and what other functions it is passed to; therefore, you should somewhat
wary of declaring a function `DYNAMIC-EXTENT`, but this is not a high-stress
declaration. On the other hand, it is much harder to ascertain that none of the
objects ever bound or assigned to that variable and none of their sub-objects
will escape the dynamic extent of the current call frame, and that they still
won't in any future modification of a function. Therefore, you should be
extremely wary of declaring a variable `DYNAMIC-EXTENT`.

It's usually hard to predict the effect of such optimization on performance.
When writing a function or macro that is part of a library of reusable code,
there's no a priori way to know how often the code will run. Ideally, tools
would be available to discover the availability and suitability of using such an
optimization based on running simulations and test cases, but in practice this
isn't as easy as it ought to be. It's a tradeoff. If you're very, very sure that
the assertion is true (that any object bound to the variable and any of its
sub-objects are only used within the dynamic extent of the specified scope), and
it's not obvious how much time will be saved and it's not easy to measure, then
it may be better to put in the declaration than to leave it out. (Ideally it
would be easier to make such measurements than it actually is.)

### REDUCE vs APPLY

-   Prefer using `REDUCE` to `APPLY` on a `CONS`ed up list.
-   Prefer apply for readability and performance reasons.

You should use `REDUCE` instead of `APPLY` and a consed-up list, where the
semantics of the first operator argument otherwise guarantees the same
semantics. Of course, you must use `APPLY` if it does what you want and `REDUCE`
doesn't. For instance:

```lisp
;; This copies the list
(apply #'+ (mapcar #'acc frobs))
```

```lisp
;; This does the same thing while avoiding the copy
(reduce #'+ frobs :key #'acc :initial-value 0)
```

This is preferable because it does not do extra consing, and does not risk going
beyond `CALL-ARGUMENTS-LIMIT` on implementations where that limit is small,
which could blow away the stack on long lists (we want to avoid gratuitous
non-portability in our code).

However, you must be careful not to use `REDUCE` in ways that needlessly
increase the complexity class of the computation. For instance, `(REDUCE 'STRCAT
...)` is *O(n\^2)* when an appropriate implementation is only *O(n)*. Moreover,
`(REDUCE 'APPEND ...)` is also *O(n\^2)* unless you specify `:FROM-END T`. In
such cases, you MUST NOT use `REDUCE`, and you MUST NOT use `(APPLY 'STRCAT
...)` or `(APPLY 'APPEND ...)` either. Instead you MUST use proper abstractions
from a suitable library (that you may have to contribute to) that properly
handles those cases without burdening users with implementation details. See for
instance `UIOP:REDUCE/STRCAT`.


### NCONC and MAPCAN

-   Don't use `NCONC` or `MAPCAN`.
    -   Also don't use the `NCONC` feature of a loop.
    -   Prefer `APPEND` instead, or better data structures.
    -   Make an exception for low-level performance-cricitcal code.

You should almost never use `NCONC`. You should use `APPEND` when you don't
depend on any side-effect. You should use `ALEXANDRIA:APPENDF` when you need to
update a variable. You should probably not depend on games being played with the
`CDR` of the current `CONS` cell (which some might argue is suggested but not
guaranteed by the specification); if you do, you must include a prominent
comment explaining the use of `NCONC`; and you should probably reconsider your
data representation strategy.

By extension, you should avoid `MAPCAN` or the `NCONC` feature of `LOOP`. You
should instead respectively use `ALEXANDRIA:MAPPEND` and the `APPEND` feature of
`LOOP`.

`NCONC` is very seldom a good idea, since its time complexity class is no better
than `APPEND`, its space complexity class also is no better than `APPEND` in the
common case where no one else is sharing the side-effected list, and its bug
complexity class is way higher than `APPEND`.

If the small performance hit due to `APPEND` vs. `NCONC` is a limiting factor in
your program, you have a big problem and are probably using the wrong data
structure: you should be using sequences with constant-time append (see
Okasaki's book, and add them to lisp-interface-library), or more simply you
should be accumulating data in a tree that will get flattened once in linear
time after the accumulation phase is complete.

You may only use `NCONC`, `MAPCAN` or the `NCONC` feature of `LOOP` in low-level
functions where performance matters, where the use of lists as a data structure
has been vetted because these lists are known to be short, and when the function
or expression the result of which are accumulated explicitly promises in its
contract that it only returns fresh lists (in particular, it can't be a constant
quote or backquote expression). Even then, the use of such primitives must be
rare, and accompanied by justifying documentation.

## Pitfalls

### Format Conditional Directives

-   Be careful when using the `FORMAT` conditional directive. The parameters are
    easy to forget.

No parameters, e.g. `"~[Siamese~;Manx~;Persian~] Cat"` \
Take one format argument, which should be an integer. Use it to choose a clause.
Clause numbers are zero-based. If the number is out of range, just print
nothing. You can provide a default value by putting a `":"` in front of the last
`";"`. E.g. in `"~[Siamese~;Manx~;Persian~:;Alley~] Cat"`, an out-of-range arg
prints `"Alley"`.

`:` parameter, e.g. `"~:[Siamese~;Manx~]"` \
Take one format argument. If it's `NIL`, use the first clause, otherwise use the
second clause.

`@` parameter, e.g. `"~@[Siamese ~a~]"` \
If the next format argument is true, use the choice, but do NOT take the
argument. If it's false, take one format argument and print nothing. (Normally
the clause uses the format argument.)

`#` parameter, e.g. `"~#[ none~; ~s~; ~s and ~s~]"` \
Use the number of arguments to format as the number to choose a clause. The same
as no parameters in all other ways. Here's the full hairy example: `"Items:~#[
none~; ~S~; ~S and ~S~:;~@{~#[~; and~] ~S~^ ,~}~]."`

### Comparison Operators

-   You should the appropriate predicates when comparing objects.
-   Also see the notes for
    [Comparison Operators](lispguide.md#comparison-operators) in the style
    guide for style rules.

Lisp provides four general equality predicates: `EQ`, `EQL`, `EQUAL`, and
`EQUALP`, which subtly vary in semantics. Additionally, Lisp provides the
type-specific predicates `=`, `CHAR=`, `CHAR-EQUAL`, `STRING=`, and
`STRING-EQUAL`. Know the distinction!

You should use `EQL` to compare objects and symbols for *identity*.

You must not use `EQ` to compare numbers or characters. Two numbers or
characters that are `EQL` are not required by Common Lisp to be `EQ`.

You should use `CHAR=` for case-dependent character comparisons, and
`CHAR-EQUAL` for case-ignoring character comparisons.

You should use `STRING=` for case-dependent string comparisons, and
`STRING-EQUAL` for case-ignoring string comparisons.

A common mistake when using `SEARCH` on strings is to provide `STRING=` or
`STRING-EQUAL` as the `:TEST` function. The `:TEST` function is given two
sequence elements to compare. If the sequences are strings, the `:TEST` function
is called on two characters, so the correct tests are `CHAR=` or `CHAR-EQUAL`.
If you use `STRING=` or `STRING-EQUAL`, the result is what you expect, but in
some Lisp implementations it's much slower. CCL (at least as of 8/2008) creates
a one-character string upon each comparison, for example, which is very
expensive.

You must not use exact comparison on floating point numbers, since the vague
nature of floating point arithmetic can produce little "errors" in numeric
value. You should compare absolute values to a threshold.

You must use `=` to compare numbers, unless you really mean for `0`, `0.0` and
`-0.0` to compare unequal, in which case you should use `EQL`. Then again, you
must not usually use exact comparison on floating point numbers.

Monetary amounts should be using decimal (rational) numbers to avoid the
complexities and rounding errors of floating-point arithmetic. Libraries such as
[wu-decimal](https://web.archive.org/web/20210423223211/https://wukix.com/lisp-decimals)
([source](https://github.com/Wukix/wu-decimal)) may help you; once again, if
this library is not satisfactory, see above about
[Using Libraries](#using-libraries).


### Case and Ecase

-   Use `CASE` and `ECASE` for numbers, characters, and symbols only.
-   Don't use gratuitous single quotes.
-   Use `OTHERWISE` and not `T`.

You should only use `CASE` and `ECASE` to compare numbers, characters or symbols
(including booleans and keywords). Indeed, `CASE` uses `EQL` for comparisons, so
strings, pathnames and structures may not compare the way you expect, and `1`
will differ from `1.0`.

You must not use gratuitous single quotes in `CASE` forms. This is a common
error:

```lisp
(ecase x
  ('bar :bar) ; Bad: catches QUOTE
  ('baz :baz)) ; Bad: also would catch QUOTE
```

```lisp
(ecase x
  ((bar) :bar) ; Better: won't match QUOTE
  ((baz) :baz)) ; Better: same reason
```

`'BAR` there is `(QUOTE BAR)`, meaning this leg of the case will be executed if
`X` is `QUOTE`... and ditto for the second leg (though `QUOTE` will be caught by
the first clause). This is unlikely to be what you really want.

In `CASE` forms, you must use `otherwise` instead of `t` when you mean "execute
this clause if the others fail". You must use `((t) ...)` when you mean "match
the symbol T" rather than "match anything". You must also use `((nil) ...)` when
you mean "match the symbol NIL" rather than "match nothing".

Therefore, if you want to map booleans `NIL` and `T` to respective symbols
`:BAR` and `:QUUX`, you should avoid the former way and do it the latter way:

```lisp
(ecase x ; Bad: has no actual error case!
  (nil :bar)) ; Bad: matches nothing
  (t :quux)) ; Bad: matches anything
```

```lisp
(ecase x ; Better: will actually catch non-booleans
  ((nil) :bar)) ; Better: matches NIL
  ((t) :quux)) ; Better: matches T
```

### Defining Constants

-   You must use proper defining forms for constant values.

The Lisp system we primarily use, SBCL, is very picky and signals a condition
whenever a constant is redefined to a value not `EQL` to its previous setting.
You must not use `DEFCONSTANT` when defining variables that are not numbers,
characters, or symbols (including booleans and keywords). Instead, consistently
use whichever alternative is recommended for your project.

```lisp
;; Two strings or lists with the same content might not be eql
(defconstant +google-url+ "https://www.google.com/")
(defconstant +valid-colors+ '(red green blue))
```

Open-Source libraries may use `ALEXANDRIA:DEFINE-CONSTANT` for constants other
than numbers, characters and symbols (including booleans and keywords). You may
use the `:TEST` keyword argument to specify an equality predicate.

```lisp
;; Better, for Open-Source code:
(alexandria:define-constant +google-url+ "https://www.google.com/"
                            :test #'string=)
(alexandria:define-constant +valid-colors+ '(red green blue))
```

Note that with optimizing implementations, such as SBCL or CMUCL, defining
constants this way precludes any later redefinition short of `UNINTERN`ing the
symbol and recompiling all its clients. This may make it "interesting" to debug
things at the REPL or to deploy live code upgrades. If there is a chance that
your "constants" are not going to be constant over the lifetime of your server
processes after taking into consideration scheduled and unscheduled code
patches, you should consider using `DEFPARAMETER` or `DEFVAR` instead, or
possibly a variant of `DEFINE-CONSTANT` that builds upon some future library
implementing global lexicals rather than `DEFCONSTANT`. You may keep the
`+plus+` convention in these cases to document the intent of the parameter as a
constant.

Also note that `LOAD-TIME-VALUE` may help you avoid the need for defined
constants.

### EVAL-WHEN

-   When using `EVAL-WHEN`, you should almost always use all of
    `(:compile-toplevel :load-toplevel :execute)`.

Lisp evaluation happens at several times, some of them interleaved. Be aware of
them when writing macros.
[EVAL-WHEN considered harmful to your mental health](https://fare.livejournal.com/146698.html).

In summary of the article linked above, unless you're doing truly advanced
macrology, the only valid combination in an `EVAL-WHEN` is to include all of
`(eval-when (:compile-toplevel :load-toplevel :execute) ...)`

You must use `(eval-when (:compile-toplevel :load-toplevel :execute) ...)`
whenever you define functions, types, classes, constants, variables, etc., that
are going to be used in macros.

It is usually an error to omit the `:execute`, because it prevents `LOAD`ing the
source rather than the fasl. It is usually an error to omit the `:load-toplevel`
(except to modify e.g. readtables and compile-time settings), because it
prevents `LOAD`ing future files or interactively compiling code that depends on
the effects that happen at compile-time, unless the current file was
`COMPILE-FILE`d within the same Lisp session.

Regarding variables, note that because macros may or may not be expanded in the
same process that runs the expanded code, you must not depend on compile-time
and runtime effects being either visible or invisible at the other time. There
are still valid uses of variables in macros:

-   Some variables may hold dictionaries for some new kind of definition and
    other meta-data. If such meta-data is to be visible at runtime and/or in
    other files, you must make sure that the macro expands into code that will
    register the definitions to those meta-data structures at load-time, in
    addition to effecting the registration at compile-time. Typically, your
    top-level definitions expand to code that does the registration. if your
    code doesn't expand at the top-level, you can sometimes use
    `LOAD-TIME-VALUE` for good effect. In extreme cases, you may have to use
    `ASDF-FINALIZERS:EVAL-AT-TOPLEVEL`.
-   Some variables may hold temporary data that is only used at compile-time in
    the same file, and can be cleaned up at the end of the file's compilation.
    Predefined such variables would include `*readtable*` or compiler-internal
    variables holding the current optimization settings. You can often manage
    existing and new such variables using the `:AROUND-COMPILE` hooks of `ASDF`.

### Pathnames

-   Common Lisp pathnames are tricky. Be aware of pitfalls. Use `UIOP`.

It is surprisingly hard to properly deal with pathnames in Common Lisp.

`ASDF 3` comes with a portability library `UIOP` that makes it *much* easier to
deal with pathnames portably — and correctly — in Common Lisp. You should use it
when appropriate.

First, be aware of the discrepancies between the syntax of Common Lisp
pathnames, which depends on which implementation and operating system you are
using, and the native syntax of pathnames on your operating system. The Lisp
syntax may involve quoting of special characters such as `#\.` and `#\*`, etc.,
in addition to the quoting of `#\\ ` and `#\"` within strings. By contrast, your
operating system's other system programming languages (shell, C, scripting
languages) may only have one layer of quoting, into strings. Use
`UIOP:NATIVE-NAMESTRING` and `UIOP:PARSE-NATIVE-NAMESTRING` to convert between
Lisp and OS representations of pathnames (on good implementations such as SBCL
and CCL, these functions work well, but on other implementations, they may fall
back to `NAMESTRING` and `PARSE-NAMESTRING` and not escape wildcard characters
properly).

Second, when using `MERGE-PATHNAMES`, be wary of the treatment of the `HOST`
component, which matters a lot on non-Unix platforms (and even on some Unix
implementations). You probably should be using `UIOP:MERGE-PATHNAMES*` or
`UIOP:SUBPATHNAME` instead of `MERGE-PATHNAMES`, especially if your expectations
for relative pathnames are informed by the way they work in Unix or Windows;
otherwise you might hit weird bugs whereby on some implementations, merging a
relative pathnames with an absolute pathname results in overriding the absolute
pathname's host and replacing it with the host from the value of
`*DEFAULT-PATHNAME-DEFAULTS*` at the time the relative pathname was created.

Third, be aware that `DIRECTORY` is not portable across implementations in how
it handles wildcards, sub-directories, symlinks, etc. There again, `UIOP`
provides several common abstractions to deal with pathnames, but only does so
good a job. For a complete portable solution, use IOLib — though its Windows
support lags behind.

`LOGICAL-PATHNAME`s are not a portable abstraction, and should not be used in
portable code. Many implementations have bugs in them, when they are supported
at all. SBCL implements them very well, but strictly enforces the limitations on
characters allowed by the standard, which restricts their applicability. Other
implementations allow arbitrary characters in such pathnames, but in doing so
are not being conformant, and are still incompatible with each other in many
ways. You should use other pathname abstractions, such as
`ASDF:SYSTEM-RELATIVE-PATHNAME` or the underlying `UIOP:SUBPATHNAME` and
`UIOP:PARSE-UNIX-NAMESTRING`.


Finally, be aware that paths may change between the time you build the Lisp
image for your application, and the time you run the application from its image.
You should be careful to reset your image to forget irrelevant build-time paths
and reinitialize any search path from current environment variables. `ASDF` for
instance requires you to reset its paths with `UIOP:CLEAR-CONFIGURATION`. `UIOP`
provides hooks to call functions before an image is dumped, from which to reset
or `makunbound` relevant variables.


### SATISFIES

-   You must be careful when using a `SATISFIES` clause in a type specifier.

Most Common Lisp implementations can't optimize based on a `SATISFIES` type, but
many of them offer simple optimizations based on a type of the form `(AND FOO
(SATISFIES BAR-P))` where the first term of the `AND` clause describes the
structure of the object without any `SATISFIES` and the second term is the
`SATISFIES`.

```lisp
; Can't optimize
(deftype prime-number () (satisfies prime-number-p))
```

```lisp
;; Can optimize based on the known type
(deftype prime-number () (and integer (satisfies prime-number-p))
```

However, `AND` in the `DEFTYPE` language isn't a left-to-right short-circuit
operator as in the expression language; it is a symmetrical connector that
allows for reordering subterms and doesn't guarantee short-circuiting.
Therefore, in the above example, you cannot rely on the test for `INTEGER`ness
to protect the function `PRIME-NUMBER-P` from being supplied non-integer
arguments to test for being of instances of the type. Implementations may, and
some *will*, invoke `SATISFIES`-specified function at compile-time to test
various relevant objects.

That is why any function specified in a `SATISFIES` clause MUST accept objects
of any type as argument to the function, and MUST be defined within an
`EVAL-WHEN` (as well as any variable it uses or function it calls):

```lisp
;; Doesn't check if argument is an integer, and the function isn't defined at
;; compile time.
(defun prime-number-p (n)
  (let ((m (abs n)))
    (if (<= m *prime-number-cutoff*)
        (small-prime-number-p m)
        (big-prime-number-p m))))
```

```lisp
;; Works when called at compile-time or passed a non-integer argument.
(eval-when (:compile-toplevel :load-toplevel :execute)
  (defun prime-number-p (n)
    (when (integerp n) ; Better
      (let ((m (abs n)))
        (if (<= m *prime-number-cutoff*)
            (small-prime-number-p m)
            (big-prime-number-p m))))))
```

In particular, the above means that the
[example](https://www.lispworks.com/documentation/HyperSpec/Body/t_satisf.htm)
used in the Common Lisp Standard is erroneous: `(and integer (satisfies evenp))`
is *not* a safe, conformant type specifier to use, because `EVENP` will throw an
error rather than return `NIL` when passed a non-integer as an argument.

Finally, there is a catch when your `DEFTYPE` code expands to a `SATISFIES` with
a dynamically generated function:

-   You cannot control when implementations will or will not expand a `DEFTYPE`.
-   The expansion itself cannot contain a function definition or any code in the
    expression language.
-   You cannot control when the expansion is used, it may happen in a different
    process that didn't expand the definition.

Therefore, you cannot merely create the function as a side-effect of expansion
using `EVAL` at type-expansion time. The solution is to use
`ASDF-FINALIZERS:EVAL-AT-TOPLEVEL` instead. See the very last point in the
discussion about [EVAL](lispguide.md#eval).

Common Lisp is hard to satisfy.
