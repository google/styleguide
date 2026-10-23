# Rust Style Guide

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<style>
.google3 {
  background-color: #34A853;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

.android {
  background-color: #a4c639;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

.chrome {
  background-color: #4285F4;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

.fuchsia {
  background-color: #c154c1;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

:is(h1, h2, h3, h4, h5, h6) :is(.google3, .android, .chrome, .fuchsia) {
  font-size: large;
  border-radius: 5px;
  padding: 4px 8px;
  vertical-align: 10%;
}
</style>

This document is a *style guide* for the usage of the Rust programming language
at Google. In this context, “style” refers to more than just formatting; it
includes guidance on API and implementation design.

Rust is used in many places, including
[google3](https://opensource.google/documentation/reference/glossary#google3),
Android, ChromeOS, Fuchsia, and Chrome, and we'd like for Rust usage at Google
to be consistent both within and across codebases. In addition to bringing
consistency to our Rust code, style guidance also helps establish a standard of
quality.

## Background

### Scope

The current scope of authority of the rules outlined in this guide:

*   **In Android, Chromium, and other codebases**: This style guide has been
    developed in consultation with other codebases, and they intend to start
    applying it. These codebases may have their own rules about how strictly
    this is expected to be applied. Expect more information here as these
    codebases adopt this guide.

### Goals of the style guide

By and large, we have this document for
[the same reasons we have a C++ style guide](https://google.github.io/styleguide/cppguide.html#Goals).

Most style rules come from one or more of the goals listed below.

<dl>

<dt>Style rules should prioritize readability and maintainability over writeability</dt>
<dd>We expect our code to be around for long periods of time, and we
consider a little bit of extra effort applied during code writing to be
worth it in the long run if the style rule improves readability.
</dd>

<dt>Style rules should favor better automation</dt>
<dd>
Large-Scale Changes (LSCs)
are common at Google, and consistency helps
make LSCs easier to carry out.
</dd>


<dt>Style rules should be consistent with the wider Rust ecosystem where possible</dt>
<dd>The broader Rust ecosystem already has a pretty good amount of consistency
in style, and we should rely on that where possible to reduce surprise and make
it less work to learn Google's Rust style.
</dd>

<dt>Style rules should pull their weight</dt>
<dd>Every Rust developer and reviewer at Google has to keep these style rules
in mind: as such, we should be careful to include rules that have a tangible
benefit.
</dd>


<dt>Style rules may help avoid minor style disagreements</dt>
<dd>There are many cases where reasonable people may disagree about a style, and
we expect that disagreement to show up often on CLs. Having a style rule helps
avoid having to rehash this each time. Rules in this category that do not have other
benefits should be kept to a minimum.
</dd>

</dl>

<a id="public-rules"></a>

## Follow public Rust style rules

Follow the official public Rust style rules to the extent they don't conflict
with this style guide.

*   [Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

    *   Most code formatting conventions are enforced automatically by rustfmt.

*   [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

A “conflict” would be a case where this style guide suggests a pattern that is
discouraged, or counter to the primary encouraged pattern in the Rust style
guide.

Why does the guidance in this style guide deviate from regular Rust style rules?

Most style guides have three goals: consistency, readability, and encouraging
good API design. Regardless of the specific choices made, it helps everyone to
have these choices made beforehand to limit bikeshedding.

This style guide shares those goals, but it also has an additional goal not seen
as often: smoothing the way for Large-Scale Changes (LSCs). Large codebases like
many of the ones at Google occasionally need to run codebase-spanning
refactorings that are assisted by tooling: for this to work well, the code
should be something tooling has an easy time working with. Consistency helps for
this, but so does having deliberate refactor-friendly patterns.

<a id="api-design-context"></a>

## Apply API design rules in context

When applying rules that relate to API design, you should distinguish two types
of code:

*   Library code

    *   Intended for use by other projects (applications or other libraries).
    *   Solves a relatively general problem.

*   Application code

    *   Intended for use in a single application.
    *   Solves a more specific problem.

For *library code*, style guide rules that concern API design are binding.

For *application code*, the rules on API design are a strong recommendation. As
you apply them, keep in mind that since application code is written to solve a
specific problem, it should generally favor simplicity and directness over broad
reusability. Avoid premature generalization and abstraction; focus on what is
required to meet the immediate need.

<a id="code-organization"></a>

## Code organization

*Terminology:*

*   A *crate* is a unit of compilation. A crate always contains a nameless Rust
    module, the "root module".

*   A Rust *module* is a unit of code organization within a crate. Rust modules
    are used to control visibility of names. Modules can be nested. They can
    also be used to split code across files and directories.

The following sections convey that in Chromium, it is preferable to **not** make
use of all possibilities of splitting modules across files.

<a id="small-crates"></a>

### Prefer small crates <span class="chrome">[chrome]</span>

Prefer small crates in Chromium; ideally, but not necessarily, a single file
(focusing on one abstraction). If your code can be split up into small crates,
do so.

A crate corresponds to a single `rust_static_library` (chrome) rule, which may
contain one or more `.rs` files.

Additional considerations:

*   The root module is allowed to `re-export` public APIs from
    `leaf submodules`, making submodules an implementation detail of the crate
    (as users don't need to know about these submodules).

*   This rule about small crates applies equally to crates with and without
    submodules. First, evaluate whether the APIs need to be in the same crate,
    and only then consider whether submodules could help organize the APIs.

*   If you decide to use submodules, follow the
    [expected file structure](#structure).

Larger crates are allowed when
[trait impl coherence rules](https://smallcultfollowing.com/babysteps/blog/2015/01/14/little-orphan-impls/)
force multiple types and traits to be included in one library, or if you're
building a large foundational library.

Rationale

Fine-grained library targets are recommended in Chromium due to the massive size
of our codebase, non-local effects of adding dependencies in the build graph,
and to improve performance of parallel compilation and build caching.

<a id="structure"></a>

### Use flat file layout for `rust_library` sources <span class="chrome">[chrome]</span>

In Chromium `.rs` source files belonging to one `rust_library` (one Rust crate)
must reside in a single directory.

Don't use subdirectories to organize files that belong to a single crate. If
organizing one crate's files into subdirectories feels necessary, this is a
strong indication that the crate has grown [too large](#small-crates) and should
be split.

This crate layout is intentionally different from the conventional Cargo
directory structure typically used in open-source repositories.

Exception: Rust code in `//third_party` that is also built with
[Cargo](https://doc.rust-lang.org/cargo/) should follow the conventional Cargo
directory structure.

Rationale

The approach in Chromium is driven by the following factors:

*   Based on the preference for [small crates](#small-crates), most
    `rust_library` targets will only contain one source file.
*   Because of the above point, creating a directory for each `rust_library`
    target would result in most directories containing only one source file.
*   Multi-file `rust_library` targets should not create dedicated directories
    for submodules either; this ensures a consistent approach.

<a id="userdefined-item"></a>

### Name source files and leaf modules after the primary user-defined item

When a `leaf module` has a primary user-defined item (e.g., `Foo`), the module
should be named after that item (e.g., `mod foo` and `foo.rs`).

Leaf modules that are not primarily about any particular abstraction can be
named as desired.

Rationale

This makes it easy to identify the content/purpose of a source file or leaf
module at a glance.

<a id="non-leaf-modules"></a>

### Don’t implement APIs in non-leaf modules

The only items in non-leaf modules should be module declarations (not
definitions) and `re-exports`.

Note that the definition of `leaf modules` allows the following sub-modules:
`mod test` and cross-language binding modules like `#[cxx::bridge]`.

Exceptions:

*   Having a small amount of core “ties things together” implementation code in
    a non-leaf module may be fine. The goal is to not have a lot of code in
    these modules.

Rationale

This makes it easier to find things, and avoids mixing structure and contents.

<a id="glob-imports"></a>

### Don’t use glob imports

Don't use glob imports, except in the following situations where you may
optionally do so at your own discretion:

*   `use super::*` for inline modules
*   `use enum::*` in method bodies of enums, and functions that are primarily
    dealing with that enum
*   `pub use submodule::*` for non-leaf modules
*   C++ interop: Since the same namespace (in C++) is a submodule in different
    Rust crates (in Rust), you may merge the namespaces into a private copy
    using glob imports. For example:

    ```rust
    mod absl {
        pub use status::absl::*;
        pub use strings::absl::*;
    }
    ```

    In this hypothetical example, you can use `absl::Status` and `absl::StrCat`
    from Rust, the same way you would from C++, instead of spelling them as
    `status::absl::Status` and `strings::absl::StrCat`.

    This must only be used for merging C++ namespaces, and the resulting merged
    module must not be public.

If using third-party crates that encourage a prelude, it is up to the reviewer’s
discretion to allow it.

This also means that defining preludes should be avoided.

Rationale

Glob imports increase toil for code janitors running LSCs, and make it harder to
know where a type comes from in contexts without xrefs.

<a id="use-statement"></a>

### A `use` statement should import items from one module

This rule corresponds to the rustfmt setting `imports_granularity = Module`.

Basically, there should not be any `::`'s inside the `{..}` block of a `use`
statement. For example:

<div class='goodcode'></div>

```rust
use foo::Foo;
use foo::bar::Bar;
use foo::bar::Baz;
```

<div class='goodcode'></div>

```rust
use foo::Foo;
use foo::bar::{Bar, Baz};
```

<div class='badcode'></div>

```rust
use foo::{Foo, bar::Bar};
```

<a id="prefer-local-trait-imports"></a>

### Prefer locally-scoped trait imports

Import traits within function bodies, unless the trait's methods are used
extensively throughout the file.

<div class='goodcode'></div>

```rust
fn foo(s: &str) -> Result<u8, std::num::ParseIntError> {
    // Import the trait within a function, not at the module scope.
    use std::str::FromStr;

    u8::from_str(s)
}
```

<a id="toplevel-functions"></a>

### Qualify calls to top-level functions with a module name

To use top-level functions defined in other modules or crates, import their
module and call them with `modulename::functionname()`. For example:

<div class='goodcode'></div>

```rust
use std::mem;

let x = mem::transmute(y);
```

<div class='badcode'></div>

```rust
use std::mem::transmute;

let x = transmute(y);
```

Exceptions:

*   When importing functions with sufficiently disambiguated names, e.g.,
    functions from C++ (where it is typical to call top-level (free) functions
    directly).
*   In Chromium, when importing functions from
    [small, single-purpose first-party crates](#small-crates).

*   When the module name itself is prone to collisions. For example, when the
    module name is a C++ namespace name, and multiple crates define the same
    submodules.

Rationale

Many Rust codebases consistently keep a style such that unqualified lowercase
names are assumed local, so `foo()` can be assumed to be from the same module.
This rule largely exists to avoid reviewer disagreements, the benefit is mostly
consistency and a minor edge on reading code without xrefs.

<a id="type-names"></a>

### Type names should be imported and used unqualified

By default, types and traits should be referenced in code without using their
module path, e.g., code should use `Regex`, not `regex::Regex`, with a
`use regex::Regex` at the top of the file or potentially in the relevant
function.

Exceptions:

*   In cases where there are ambiguities, it is acceptable to directly reference
    types with common names like `io::Error`. It is also acceptable to rename
    (`use std::io::Error as IoError`).
*   In cases where you have a large “group” of types, e.g. the
    [`hir module in rustc`](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_hir/hir/index.html)
    which contains a large number of HIR types.
*   In macros and generated code; where requiring a `use` is counterproductive.
*   In code with lots of dependencies, where importing everything would lead to
    a very large import block with little benefit.

Rationale

This rule largely exists to avoid reviewer disagreements.

<a id="import-macro"></a>

### Use the appropriate import mechanism <span class="chrome">[chrome]</span>

*   <span class="chrome">Chrome</span> Use `chromium::import!()`.

<a id="code-formatting"></a>

## Code formatting and aesthetics

<a id="formatting-other"></a>

### Use the appropriate formatting tool

Use the appropriate formatting tool (e.g., `git cl format` in Chromium).

Configuration (for style guide authors)

A codebase may choose to not apply the following `rustfmt` options if they care
about building on stable and the option is unavailable on their stable Rust:

*   Maximum of 100 columns per line:
    [`max_width = 100`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#max_width)

*   Usage of lowercase alphabets in hex literals (`0xab123cdef` as opposed to
    `0xAB123CDEF`):
    [`hex_literal_case = Lower`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#hex_literal_case)

*   Macro matcher formatting:
    [`format_macro_matchers = true`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#format_macro_matchers)

*   Usage of escapes for invisible characters in literals. E.g., if you wish to
    have text containing a Zero-Width joiner, use `\u{200D}`.

<a id="formatting-optout"></a>

### Opting out of automatic formatting

You may opt out of automatic formatting using `#[rustfmt::skip]`, but only in
the following situations:

*   **Manual alignment** – If you have a situation-specific reason to have a
    snippet of code line up in a particular way (e.g., multiple similar lines of
    code that you want to remain aligned for readability, or a
    matrix-constructing function).
*   **Generated code** (ideally, use a genrule instead).

Important: Formatting should not be skipped for personal style choices.

<a id="ownership-borrowing"></a>

## Ownership and borrowing

<a id="avoid-rc-arc"></a>

### Avoid `Rc` and `Arc`

Prefer unique ownership and borrowing over `Rc` and `Arc` for managing memory.

Exception:

*   Use `Rc` and `Arc` when the alternative ownership and borrowing structure
    would be unreasonably complex to write, understand, or maintain. This is a
    judgment call to be discussed during code review.

Rationale

Generally, Rust allows representing object graphs without using shared ownership
smart pointers. These pointers add runtime overhead and their own unique
complexity. Engineers coming from other languages might tend to use `Rc` and
`Arc` too quickly.

<a id="prefer-borrows"></a>

### Prefer borrows over deep copies

Use `.clone()` when you genuinely need a deep copy of an object.

Avoid using `.clone()` as a substitute for borrowing. Design code that works
naturally with Rust's ownership and borrowing rules. However, if the borrowing
relationships become excessively complex, `.clone()` can be a pragmatic choice.

Consider the performance needs of the code while choosing between cloning and
borrowing.

Note: This advice does not apply to cloning `Rc` or `Arc` pointers. Cloning
reference-counted pointers does not create a deep copy, and is an expected way
to use them.

Rationale

Deep copies can be expensive to make due to memory allocation and data copying.

<a id="inputs-and-outputs"></a>

## Function inputs and outputs

<a id="flexible-references"></a>

### Accept flexible references for immutable data

When functions accept borrowed, immutable data, use a reference type that
affords the most flexibility. Pass references to the data itself instead of
references to smart pointers, containers, or wrappers.

<!-- mdformat off(keep table rows on single lines for Kramdown compatibility in the public style guide) -->

| Use          | Instead of   | Why?                                                         |
| ------------ | ------------ | ------------------------------------------------------------ |
| `&T`         | `&Box<T>`    | Borrow the data inside the box                               |
| `&[T]`       | `&Vec<T>`    | Accept any slice instead of specific containers              |
| `&str`       | `&String`    | Accept a string slice instead of references to owned strings |
| `Option<&T>` | `&Option<T>` | Borrow the data inside the Option                            |

<!-- mdformat on -->

Exceptions:

*   When expecting non-linear character data such as Rope/Cord.

For context, see Clippy lints
[`borrowed_box`](https://rust-lang.github.io/rust-clippy/master/index.html#borrowed_box)
and
[ptr_arg](https://rust-lang.github.io/rust-clippy/master/index.html#ptr_arg).

Rationale

Accepting reference types that don't mention specific smart pointers,
containers, or wrappers makes functions more versatile and performant: callers
can pass data held in a variety of ways without copying it first.

<a id="return-iterators"></a>

### Iterators vs. owned collections in return types

Prefer returning iterators (either concrete types or `impl Iterator`) where
possible over returning `Vec<T>`.

Note: In application code, returning a `Vec<T>` is fine if it simplifies the
code and if flexibility and performance advantages of iterators are not clearly
needed.

Exceptions:

*   Most callers will need to construct an owned vector.
*   The function's implementation naturally constructs a vector.
*   The returned value will likely need to be randomly indexed.
*   The algorithm works better as a `for` loop and the forced allocation doesn't
    matter too much.
*   The function's intended purpose is creating a new owned collection.
*   The function is returning a pre-existing vector.

Rationale

Highly reusable library code generally should strive to provide more flexible
and performant APIs. Returning an iterator allows callers to choose how to
consume the data: collect it into a vector, process it in a loop, or chain
further iterator adapters. Some of these options allow users to avoid
unnecessary allocations.

In application code, the usage patterns for a function are often easier to
predict. If it is clear that performance is not a concern, or that data would be
collected into a vector anyway, returning a vector makes for a simpler API.

<a id="accept-iterators"></a>

### Iterators vs. slices in function parameters

Highly reusable library code should accept iterators or `impl IntoIterator` if
it only needs to iterate over the input.

Note: In application code, accepting a slice `&[T]` is fine if it simplifies the
code and if flexibility and performance advantages of iterators are not clearly
needed.

Rationale

Highly reusable library code generally should strive to provide more flexible
and performant APIs. Functions that accept iterators offer callers:

*   More flexibility (data can be supplied from any collection)
*   Efficiency (data does not need to be copied into a contiguous piece of
    memory)
*   Composability (the function works better with iterator chains)

In application code, the usage patterns for a function are often easier to
predict. If it is clear that performance is not a concern, or that callers would
always have a vector anyway, accepting a slice makes for a simpler API.

<a id="accepting-into"></a>

### Accepting `Into`

When designing library APIs that accept a `T` but users are likely to have
various types, consider accepting `impl Into<T>` instead of `T` if **call-site
ergonomics are paramount**.

Tip: This should be balanced against code bloat concerns; it is not a
requirement to use lots of `Into<T>` in your code.

Note: Application code should almost never use `impl Into<T>` parameters.

Rationale

Using `impl Into<T>` allows a function to directly accept various arguments of
various compatible types. For example, a function accepting `impl Into<String>`
could be called with a `String` or a `&str` literal directly.

The tradeoff here is balancing the convenience of avoiding a `.into()` at the
callsite against the cost of generics (more complex API signature, increased
code size, sometimes even type inference difficulties).

<a id="enum-vs-bool"></a>

### Prefer `enum` over `bool` in APIs

Use `enum` function parameters instead of `bool` in cases where the purpose of
the parameter is not obvious.

If you do use `bool`, consider using an inline comment to document the purpose
of the `bool` in an argument list.

<a id="reporting-errors"></a>

### Reporting errors

Choose the error reporting mechanism that fits your API contract: `Option`,
`Result`, or `panic!`.

**Use `Option` for simple failures** where the cause is obvious and the caller
would not benefit from further details. This is best for standard, anticipated
outcomes like a missing value or a parsing mismatch.

<div class='goodcode'></div>

```rust
// Good: The cause of the failure is obvious (integer overflow). No further
// details could be reasonably provided.
fn checked_add(a: u32, b: u32) -> Option<u32> { ... }
```

**Use `Result` for recoverable failures where the caller needs context** to
handle the error. These are often "unavoidable" errors caused by external
factors (like I/O or network) that even correctly implemented code cannot
prevent with checks ahead of time. Nevertheless, the caller can reasonably
anticipate the kinds of errors (a file-related function can fail with an I/O
error). The error details allow the caller to distinguish failure modes and
recover appropriately.

<div class='goodcode'></div>

```rust
// Good: The caller needs to know *why* it failed (NotFound vs PermissionDenied).
fn open_file(path: &Path) -> Result<File, io::Error> { ... }
```

**Use `panic!` to report bugs and violated invariants.** These errors are
avoidable: the program is missing a check, and is calling an operation without
fulfilling a precondition. These defects must be fixed in the code, not handled
at runtime, although coarse-grained recovery might be possible with
`catch_unwind`.

<div class='goodcode'></div>

```rust
// Good: Panics if the invariant (index must be in bounds) is violated.
// This indicates a bug in the caller's logic.
impl<T> MyVec<T> {
    pub fn remove(&mut self, index: usize) -> T {
        if index >= self.len() {
            panic!("index out of bounds");
        }
        // ...
    }
}
```

Note: Some codebases may choose to avoid panics entirely, and require even
broken invariants to be reported via `Result`.

Exceptions:

*   Developer-facing binaries may use panics for non-fatal errors.
*   Tests may use panics for assertions.

<a id="types"></a>

## Types

<a id="newtypes-vs-type-aliases"></a>

### Newtypes versus type aliases

Use a
[newtype](https://doc.rust-lang.org/rust-by-example/generics/new_types.html)
instead of a type alias in the following cases:

*   If the type you are defining has notable semantic differences.
*   For types that warrant an API of their own.
*   If you want the flexibility to change the underlying type later, especially
    if you don't control all usages of your type.
*   For type safety, if it’s easy for the types to get mixed up. For example, a
    `Date` type may use newtypes to distinguish `Day`, `Month`, and `Year`
    numbers in its internal calculations.

<a id="prefer-named-fields"></a>

### Prefer named fields over tuples and non-newtype tuple structs

Prefer types with named fields over tuples, as tuple indexes (`.0`, `.1`, ...)
quickly become confusing.

Exceptions:

*   Newtype tuple structs (tuple structs with only one field).
*   In very local contexts where there is unlikely to be any confusion.

<a id="traits"></a>

## Traits

<a id="traits-yagni"></a>

### Add trait implementations when they become necessary

As a general rule, low-level library code should anticipate users' needs
proactively, while application code should add trait impls as needed.

<a id="known-traits"></a>

### Implement known standard library traits instead of custom methods

If a method matches the purpose and behavior of a standard library trait,
implement that trait. For example, instead of writing
`fn from_str(&str) -> Self` on `Foo`, you should `impl FromStr for Foo`.

It is acceptable to have both the method and the trait impl for discoverability
reasons.

For context, see Clippy lint
[`should_implement_trait`](https://rust-lang.github.io/rust-clippy/master/index.html#should_implement_trait)
([list of traits](https://github.com/rust-lang/rust-clippy/blob/928349795f9f28f54e69bd0f0ffeed33de5e272a/clippy_lints/src/methods/mod.rs#L3940-L3971)).

<a id="derive"></a>

### Use `#[derive()]` if possible

Manual implementations should be avoided if they can be expressed as a
`#[derive()]`.

<a id="generics-vs-dyn-trait"></a>

### Generics versus `dyn Trait`

In libraries, prefer accepting generics (`T: Trait` or `impl Trait`) in function
parameters over `dyn Trait`.

Exceptions:

*   Cases where code size matters.

Rationale

-   Efficiency

    -   Additional indirection: Creating a `dyn Trait` requires setting up a fat
        pointer, and a vtable lookup is required for every call of a function on
        the trait.
    -   If a function takes a `dyn Trait`, the compiler can't perform certain
        optimizations that it could if the function was generic, such as
        inlining calls to functions of the trait.

-   Some traits are not
    [`dyn` compatible](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility).
    For example, a trait is not `dyn` compatible if it has generic functions,
    associated functions without a `self` parameter, or functions that return
    `Self`.

<a id="trait-vs-inherent-impl"></a>

### When to define a trait versus an inherent implementation

Define a trait only for the following purposes:

*   To enable generic programming (to use `T: Trait` in constraints of generic
    functions and types).

*   To accept or return an `impl Trait` or `dyn Trait`.

*   To define an [extension trait](#extension-traits) (but see also the caveats
    in the section on extension traits).

In all other cases where you want to implement functionality for a type, use an
[inherent implementation](https://doc.rust-lang.org/std/keyword.impl.html#inherent-implementations).

Don't use traits merely to organize code.

<a id="extension-traits"></a>

### Extension traits

An
[extension trait](https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html)
is a trait that adds methods to a type from a different crate.

What differentiates an extension trait from other traits is that its sole
purpose is to add methods to the type; it is not intended for use in generics
(`T: Trait`, `impl Trait`) or dynamic dispatch (`dyn Trait`). To indicate this,
the name of an extension trait should carry the suffix `~Ext` (for example,
`ForeignTypeExt`).

In general, the team that owns the original type should also own the extension
trait.

Exceptions:

*   Extension methods that are expected to become well known and provide
    significant value, for example, in foundational libraries / frameworks.

Note: This rule is specifically about extension traits. It is relatively common
to define a trait as an input trait (e.g., `DateLike`) and implement it on a
bunch of foreign types.

Examples

```rust
extern crate foreign_crate;
use foreign_crate::ForeignType;

trait ForeignTypeExt {
  fn additional_method(&self);
}

impl ForeignTypeExt for ForeignType {
  fn additional_method(&self) { ... }
}
```

It is also possible to define an extension trait for every type that implements
some foreign trait. Effectively, this is equivalent to adding default methods to
the foreign trait:

```rust
extern crate foreign_crate;
use foreign_crate::ForeignTrait;

trait ForeignTraitExt {
  fn additional_method(&self);
}

impl<T: ForeignTrait> ForeignTraitExt for T {
  fn additional_method(&self) { ... }
}
```

Rationale

When the same team owns the extension trait and the type being extended, this
helps avoid method name conflicts between the base type and the extension trait
or between two extension traits.

<a id="important-traits"></a>

### Specific guidance for important traits

*   **Types with public fields**: Consider implementing traits implemented by
    all subfields.

*   **Error types**: Implement the `Copy` trait whenever possible. `Copy` types
    are simpler to manage and propagate because they can be passed by value
    without moving ownership. An example of a case where this is not possible is
    if the error must contain non-`Copy` fields like a `String`.

*   **`Copy`**: Implement whenever it is reasonably clear that the type will
    continue to be `Copy` in the future.

*   **`Clone`**: Most types should implement `Clone` unless they represent some
    external resource.

*   **`Default`**: Implement if the type implements `new()` or otherwise has a
    default state. For context, see Clippy lint
    [`new_without_default`](https://rust-lang.github.io/rust-clippy/master/index.html#new_without_default).

*   **`PartialEq`** / **`Eq`**: If you want users to use the `==` operator,
    prefer implementing `PartialEq` over `Eq`. When you do implement `Eq`, be
    aware of the additionally required reflexivity (details:
    https://doc.rust-lang.org/std/cmp/trait.Eq.html).

*   **`PartialOrd`** / **`Ord`**: If you want users to use the `<` or `>`
    operators, prefer implementing `PartialOrd` over `Ord`. When you do
    implement `Ord`, be aware that it requires total ordering (details:
    https://doc.rust-lang.org/std/cmp/trait.Ord.html).

*   **Map keys**

    *   If you think it is likely that a type will be used as a map key or
        otherwise cached, implement `Hash` and `Eq`.
    *   If, in addition, the type has a clear total ordering, implement `Ord`
        (and any traits it needs).

<a id="from-impls"></a>

### Pair important `From` impls with explicit constructor methods

If a type has an important `From` impl that is expected to be one of the primary
ways of constructing it, add an inherent `::new()`, `::new_from_foo()`, or
`::from_foo()` method.

<a id="options-should-implement-default"></a>

### Options structs should implement Default

Structs with all-public fields that are primarily used as a “bag of options” for
a function should implement `Default`.

Rationale

This enables convenient use of struct update syntax
(`Struct { a: 0, ..Default::default()}` ).

<a id="concurrency"></a>

## Concurrency

<a id="poison"></a>

### Handling poison

Never reach inside a poisoned mutex to get at its insides, no matter how
tempting the use case may seem.

<a id="async-await-chrome"></a>

### Don't use `async` / `.await` <span class="chrome">[chrome]</span>

Don't use `async` / `.await` in Chromium.

<a id="std-thread"></a>

### Don't start new threads through the Rust standard library <span class="chrome">[chrome]</span>

In Chromium, prefer to use sequences instead of threads.

<a id="fuchsia-mutex"></a>

### Use `fuchsia_sync::Mutex` <span class="fuchsia">[Fuchsia]</span>

Use Fuchsia’s mutex type, rather than one from `std::sync` or `parking_lot`.

<a id="macros"></a>

## Macros

When considering how to express an API, prefer in order:

-   Regular Rust functions, types, traits, objects, and modules. (Avoid macros,
    code generation, and metaprogramming where possible).

-   `macro_rules!`-style macros.

-   Other code generation strategies (e.g. `genrule`)

-   `proc_macro` macros.

When you decide to use a macro or code generation, please weigh the benefits
against the costs:

-   IDEs, Code Search and other developer tools will work less well on code that
    uses macros.
-   Macros can create dialects of the language that make it harder for engineers
    to work across the codebase.
-   Large scale changes are more difficult and expensive to apply.

Rationale

**Prefer non-macro facilities:** Macros can create dialects of the language that
make it harder for engineers to work across the codebase. When a reader sees a
usage of a macro, they can make fewer assumptions about that code than if it
didn't use a macro. Macros are harder to write correctly than regular Rust code.

**Use `macro_rules!` for simple code generation:** Since Rust macros operate on
the AST, they can be less fragile than textual code generation.

<a id="naming"></a>

## Naming

<a id="naming-methods"></a>

### Naming methods

Follow the Rust standard library style for naming methods. See also the guidance
on
[naming conventions](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions.html)
in the Comprehensive Rust course.

Specific considerations:

*   Use prefixes such as `as_...()`, `to_...()`, or `into_...()` with the
    appropriate `self` convention. See also
    [this section](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv)
    of the Rust API Guidelines and the Clippy lint
    [`wrong_self_convention`](https://rust-lang.github.io/rust-clippy/master/index.html#wrong_self_convention).

<a id="lifetimes"></a>

### Naming lifetimes

Lifetimes should have descriptive names, especially type lifetimes.

Exceptions:

*   Type lifetimes that are extremely generic abstractions like `Cow`.
*   It is fine to use anonymous lifetimes (`'_`) where they work.
*   Single-character lifetimes are okay when they are simply expressing the
    relationship between a method’s input and output, or needed for a local
    higher-ranked lifetime bounds (`for<'a>`). Up to two such local lifetimes
    are fine, if more are needed, we strongly advise you to use descriptive
    names.

<a id="generic-parameters"></a>

### Naming generic parameters

Use a short name for your generic parameters (either single or multi character),
related to the kind of thing they represent. Single-letter generics are okay,
but the letter chosen should be somewhat indicative of the object type, ideally
taken from the most important trait bound.

`T` or `U` are fine when the generics are in a relatively unbound context; i.e.
it is an API intended for use with most types, like `Vec<T>`.

<a id="naming-extension-traits"></a>

### Naming extension traits

When naming an [extension trait](#extension-traits), give the name an `~Ext`
suffix (for example, `ForeignTypeExt`).

<a id="naming-initialization-functions"></a>

### Naming initialization functions

Follow these guidelines when naming initialization functions:

*   Constructors: Use `new()`, or `new_with_foo()` if there is more than one. If
    the constructor returns a `Result`, use `try_new()`.

*   Value-to-value conversions: Use `from_foo()` with an associated `From` impl.
    See
    [here](https://doc.rust-lang.org/std/convert/trait.From.html#when-to-implement-from)
    for details on when an operation can be considered to be a value-to-value
    conversion.

<a id="avoid-abbreviations"></a>

### Avoid abbreviations

Don't use abbreviations (especially acronyms and initialisms) that someone
outside your project is unlikely to know. Don't abbreviate by deleting letters
within a word.

See also the
[Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html#General_Naming_Rules).

Exceptions:

*   Common abbreviations found in Wikipedia.
*   Abbreviations that are unlikely to be confusing to people outside of your
    project, for example `IpAddr`. You and your reviewer should make this
    determination. In general, the preference should still be not to abbreviate.

<a id="writing-doc"></a>

## When and how to write documentation

Add documentation comments to public APIs, potentially using the `missing_docs`
lint to help with this.

Best practices for documentation comments:

*   Consider including examples: It is not necessary for every function to have
    examples, but enough functionality should be covered in examples *somewhere*
    to give an idea of how the crate works.

*   Always document panic cases for functions which may panic due to malformed
    input.

*   Clearly document invariants for unsafe functions and traits.

*   Use capitalization and punctuation.

*   Don't explain the basics of the programming language. For example, don’t do
    the following:

    ```rust
    struct MockFileSystem { ... }

    /// A mock implementation of the FileSystem trait, intended to be used in unit tests.
    impl FileSystem for MockFileSystem
    ```

Exceptions:

*   Comments should say something that the code does not already say. If there's
    nothing insightful to say, it is better to omit the comment than to repeat
    the function name in a trivial way. For example, don’t do the following
    (it’s fine to `allow` the lint in that case):

    ```rust
    /// Removes an element.
    pub fn remove_element() -> Element {}
    ```

*   It is generally okay to omit documentation on individual enum variants,
    especially if their name is self-explanatory.

**How to format documentation comments**

Follow these guidelines when writing documentation comments:

*   Use `///` comments to document items following the comment, such as
    functions, structs, enums, traits, and type aliases.
*   Use `//!` comments to document the module or the library itself. These
    comments should be placed at the top of the file.
*   Follow the rules laid out in
    [the official Rust style guide on doc comments](https://doc.rust-lang.org/nightly/style-guide/#doc-comments).
*   Use Markdown syntax.
*   Use ordinary comment syntax (`//`) for non-documentation comments, such as
    implementation comments, TODOs that are not interesting for users, commented
    out source code, etc.
*   Prefer to document things in a straightforward manner, using `///` and `//!`
    comments, rather than generating documentation from macros. This makes the
    documentation directly readable when viewing or modifying the source code.

It is acceptable, and even encouraged, to mix doc comments (`///` and `//!`) and
ordinary comments (`//`). If you have one thing you wish to document publicly,
and another thing you want to note as an implementation comment, then use both!
For example:

<div class='goodcode'></div>

```rust
/// Finds the first `FooItem` with the given `name`, or `None` if not present.
// TODO: crbug.com/12345 - `name` should be &str, not String.
pub fn get_named(items: &[FooItem], name: String) -> Option<&FooItem> {...}
```

Rationale

Many, though not all, languages have a different commenting convention (such as
extra `*` characters) for doc comments as opposed to implementation comments.
Rust and Python are notable for not just having different commenting
conventions, but an actual different syntax entirely. This has concrete benefits
to the Rust ecosystem:

*   Doc comments can be consumed by tooling, including documentation generators
    like `rustdoc`, IDE features, and Kythe.
*   Doc comments have a standard structure and formatting rules (Markdown),
    allowing for rich text in those contexts.
*   Errors in applying doc comment syntax (e.g., applying it to an expression
    instead of a documentable item) are linted against, catching documentation
    errors early. If there are no lint errors, the doc comments are guaranteed
    to be visible to documentation tooling, removing a degree of flakiness and
    unpredictability from the documentation process.
*   Doc comments are a part of the AST, and so can be produced and consumed by
    macros, including both `macro_rules!` macros and procedural macros.

<a id="other-features"></a>

## Other Rust features

<a id="unsafe"></a>

### Unsafe code

Don't write unsafe code unless there is no way to implement the same
functionality with safe code.

If you do have to write unsafe code:

*   Encapsulate unsafe code in a safe abstraction and isolate it from business
    logic as much as possible. Ideally, unsafe code should be in a separate
    crate with few dependencies beyond the standard library.
*   Add a safety comment starting with `SAFETY:` that explains why the code is
    correct.
*   Add a technical justification for unsafe code. Depending on context, this
    can be a justification for an individual unsafe block or a more general
    justification that covers an entire file or build target. The justification
    should answer these questions:
    *   Why is this code not written in an equivalent safe way?
    *   If the reason is performance, are there benchmarks?

<a id="unstable-features"></a>

### No unstable features

Don't use unstable features.

Exceptions:

*   <span class="android">Android</span> Embedded programming may require the
    use of certain unstable features. While review will be required to enable
    them (to help search for alternatives), features absolutely required to
    build an artifact correctly will generally be approved.
*   <span class="chrome">Chrome</span> Style arbiters may blanket-approve a
    small list of features for the entire codebase. Typically, only features
    that have a clear path to stabilization will be approved.
*   <span class="fuchsia">Fuchsia</span> See guidance
    [here](https://fuchsia.dev/fuchsia-src/development/languages/rust/unstable).

<a id="getters-and-setters"></a>

### Getters and setters

Writing and naming getters and setters should follow these guidelines:

*   `foo()` for a getter that returns a `T` by value.
*   `foo_mut()` for a getter that returns a `&mut T`.
*   `take_foo()` for a getter that "clears" the value (by setting it to `None`
    or some other default state) and returns the old value.
*   `set_foo()` for a setter that takes a `T` by value.
*   `with_foo()` / `with_mut_foo()` for an accessor that operates via a closure
    (see details [below](#closure-accessors)). Such an accessor is invoked as
    `object.with_foo(|foo| frob(foo))`.
*   `replace_foo()` for a setter that returns the old value.

Examples

```rs
impl Stuff {
   fn foo(&self) -> &Foo { ...  }
   fn foo_mut(&mut self) -> &mut Foo { ... }

   /// Sets "baz" property to `None` and returns the old value.
   fn take_baz(&mut self) -> Option<Baz> { ... }

   fn set_foo(&mut self, foo: Foo) { ... }

   /// Calls `f` with a borrow of the "bar" property.
   /// Returns the return value of `f`.
   fn with_bar<R>(&self, f: impl FnOnce(&Bar) -> R) -> R { ... }

   /// Calls `f` with a mutable borrow of the "bar" property.
   /// Returns the return value of `f`.
   fn with_mut_bar<R>(&self, f: impl FnOnce(&mut Bar) -> R) -> R { ... }

   /// Sets "foo" property to `foo` and returns the old value.
   fn replace_foo(&mut self, foo: Foo) -> Foo  { ... }
}
```

<a id="closure-accessors"></a>

#### More on accessors that accept closures

Accessors that accept a closure (`.with_foo()`) are typically invoked as
`object.with_foo(|foo| do_something_with(foo))`. They can be a good choice in
the following situations:

*   When the property is contained in an interior mutability wrapper (e.g.
    `Mutex` or `RefCell`). These mechanisms need to constrain access to the
    property to a scope, and the closure provides this scope. This is usually
    preferable to directly returning the RAII object that implements the scope
    (e.g. `MutexGuard<T>`) because the latter would leak an implementation
    detail.

*   When follow-up work or validation is needed after a property is changed and
    a `set_foo()` accessor cannot be used (for example because the property's
    type is expensive to clone or cannot be cloned at all).

A `with_foo()` accessor will often allow the closure to return a value and
forward it by returning it from `with_foo()`.

If you need to provide two closure-accepting accessors, one for read-only access
and one for mutable access, it is common to name them `with_foo()` and
`with_mut_foo()`. Otherwise, `with_foo()` is often also used for mutating
accessors.

<a id="expected-api-sets"></a>

### Implement expected API sets together

If you implement `len()`, also implement `is_empty()`. For context, see Clippy
lint
[`len_without_is_empty`](https://rust-lang.github.io/rust-clippy/master/index.html#len_without_is_empty).

<a id="doc-hidden"></a>

### Do not access items marked `#[doc(hidden)]` that you don't own

Treat items marked `#[doc(hidden)]` as private. Don't access them unless you own
the code.

<a id="const-functions"></a>

### Use `const` functions responsibly

Mark a public function as `const` only if you expect it to remain `const` in the
future (or can commit to helping clients migrate when it changes).

Rationale

It’s a breaking change to turn a `const` function into a regular function.

<a id="operator-overloads"></a>

### Avoid overloading for non-mathematical purposes

Use operator overloads for their original mathematical/logical purpose, not just
to make the code more concise (as "syntax sugar").

<a id="non-exhaustive-enums"></a>

### Apply `#[non_exhaustive]` to publicly-exposed enums

If an enum is part of a public API used by other teams, mark it
`#[non_exhaustive]`.

Exceptions:

*   The enum will never change. For example:
    *   Enums describing an existing ontology (e.g.,
        `enum Color { Red, Green, Blue }`).
    *   Enums with two states that could be Booleans (e.g.,
        `enum Visibility { Visible, Hidden }`)
*   The enum *may* change in the future, but you are committed to fixing
    resulting breakages via an LSC.

For context, see Clippy lint
[`exhaustive_enums`](https://rust-lang.github.io/rust-clippy/master/index.html#exhaustive_enums).

Rationale

Marking an enum `#[non_exhaustive]` forces users to include a wildcard arm
(`_ => ...`) in `match` statements. This ensures code continues to compile when
new variants are added to the enum later.

This rule is primarily important for enums used across team boundaries, because
the scope of the breakage could be significant. Enums used only a small number
of times can't create a large breakage and thus may ignore this rule.

<a id="non-exhaustive-structs"></a>

### Apply `#[non_exhaustive]` to public structs with public fields

Structs with public fields that are part of a public API used by other teams
should be marked `#[non_exhaustive]`.

Exceptions:

*   The struct fields are unlikely to change, e.g., because they describe an
    existing ontology (e.g., a Rectangle type) or the reviewer can otherwise be
    confident that they will not change.
*   The struct fields *may* change in the future, but you are committed to
    fixing resulting breakages via an LSC.
*   You want to enable your users to use functional record update (FRU) struct
    initialization syntax (`Person { name: "foo", ..Default::default() }`).

Rationale

Adding a new field (even a private one) to a struct with all public fields is a
breaking change, because callers can no longer name all fields in a struct
literal.

A `#[non_exhaustive]` struct can't be constructed with the struct literal
syntax, except for the code in the same crate. This allows new private fields to
be added without breaking users.

This rule is primarily important for structs used across team boundaries,
because the scope of the breakage could be significant. Structs used only a
small number of times can't create a large breakage and thus may ignore this
rule.

<a id="must-use-on-functions"></a>

### `#[must_use]` on functions

Use `#[must_use]` on functions in these cases:

*   The caller cannot use the function correctly if they ignore the return
    value. This includes pure functions (functions without side effects), such
    as `HashMap::get()`.

*   Any function whose return value represents an error or otherwise critical
    information about the function's behavior. If the return type is already
    annotated `#[must_use]` (which is true of `Result`, for example), the
    function does not need to be annotated `#[must_use]`.

<a id="must-use-on-types"></a>

### `#[must_use]` on types

Use `#[must_use]` on types intended to be returned by functions that would
otherwise be annotated `#[must_use]` according to the
[rules above](#must-use-on-functions).

Examples:

*   The type is an error type (similar to `Result` or `StatusOr`).

*   The type represents a lazily evaluated computation. In other words, the
    function call doesn't do anything by itself, and the return value needs to
    be accessed to cause some desired side effect.

<a id="global-initialization"></a>

### Do not run code before `main()`

Do not cause code to run before `main()`, for example by using techniques such
as the [ctor crate](https://docs.rs/ctor/latest/ctor/).

## Implementation concerns

<a id="type-inference"></a>

### Don't overuse type inference

Add enough explicit types so that someone familiar with the codebase can figure
out what the inferred types are.

Prefer to add the types to variable declarations, rather than as
[turbofishes](https://doc.rust-lang.org/reference/glossary.html#turbofish). If
the compiler forces you to add a turbofish, it is generally fine to add a `_`
inference marker.

Specific situations in which you should probably add types:

*   When calling methods with a generic return type, such as `.into()` or
    `.parse()`.
*   For the result of complex iterator chains.

<a id="dont-check-then-unwrap"></a>

### Prefer pattern matching over check-then-unwrap

Avoid potentially panicking operations when the input data guarantees they
cannot panic. For example, instead of using `Option::unwrap` on a value known to
be valid, use pattern matching to prove correctness to the compiler.

<div class='goodcode'></div>

```rust
// Good: The match arm proves to the compiler that `x` is `Some`.
// A panic is obviously not possible.
if let Some(value) = option {
    use_value(value);
}
```

<div class='badcode'></div>

```rust
// Bad: Correctness of `unwrap` relies on a runtime check that `option` is `Some`.
if option.is_some() {
    use_value(option.unwrap());
}
```

<a id="expect-over-unwrap"></a>

### Prefer `expect` over `unwrap`

If a panic is necessary because an invariant cannot be expressed in the type
system, prefer `expect` over `unwrap` to document the reason.

<a id="non-exhaustive-enum-matching"></a>

### Don't omit patterns on `non_exhaustive` enums when matching

Prefer to list all enum variants in `match` statements over `non_exhaustive`
enums.

If you don't care about specific variants, place them in the wildcard arm. If
you *only* care about specific variants, use an `if let` or a `let … else {}`.

Examples:

```rust
#[non_exhaustive]
pub enum Shape {
    Circle,
    Square,
    Triangle,
}
```

<div class='goodcode'></div>

```rust
fn process_shape(shape: Shape) {
  match shape {
    Shape::Circle => println!("It's a circle"),
    Shape::Square => println!("It's a square"),
    // Triangle and any future variants don't require any actions.
    Shape::Triangle | _ => {}
  }
}
```

<div class='goodcode'></div>

```rust
fn process_shape(shape: Shape) {
  if let Shape::Circle = shape {
    println!("It's a circle");
  }
}
```

<div class='badcode'></div>

```rust
fn process_shape(shape: Shape) {
  match shape {
    Shape::Circle => println!("It's a circle"),
    _ => {}
  }
}
```

Exceptions:

*   You only care about specific variants *and* `match` is cleaner than
    `if let`.

<a id="assertion-context"></a>

### Use context strings to clarify assertions

While some assertions are self-explanatory, many benefit from additional context
that clarifies why an assertion is expected to hold, or what caused it to be
violated. Use the optional format string argument for `assert!` to convey this
context.

You should always consider adding context, but particularly in the following
situations:

*   If you're thinking of adding a comment to the assertion. Use a format string
    instead: It has the benefit that it will appear in logs.
*   If you expect failing assertions to be seen by users. In this case, a
    human-readable explanation is more helpful than a Rust expression.
*   If logging a value helps in understanding why the assertion failed.
*   To clarify whether a failing assertion means that
    *   The client misused an API (i.e., they should change their use of the
        API), or
    *   The implementation contains a bug (i.e., the client should file a bug
        report).

Examples

**Explaining why an assertion should hold**

<div class='goodcode'></div>

```rust
    assert!(
        values.is_sorted(),
        "`values` is populated from a `PriorityQueue`, so we expect it to be sorted"
    );
```

**Logging a value to clarify why the assertion failed**

<div class='goodcode'></div>

```rust
assert!(refund > 0, "Refund must be positive, got {refund:?}");
```

**Flagging misuse of an API**

<div class='goodcode'></div>

```rust
impl Database {
    ...

    fn execute_query(&self, query: &str) {
        assert!(self.stream.is_some(), "Call connect() before executing queries");
    }

    ...
}
```

**Don't use the context string merely to repeat the condition**

<div class='badcode'></div>

```rust
assert!(values.is_sorted(), "values should always be sorted");
```

<a id="combinator-chains"></a>

### Don't use iterator combinator chains when direct iteration is clearer

Avoid using combinator chains in ways that hurt readability. Specifically:

*   Avoid long and complex combinator chains.
*   Don't construct combinator chains in the header of a `for` loop. Instead,
    assign the combinator chain to a variable, then consume that variable in the
    `for` loop.
*   Avoid `Iterator::for_each` unless you're convinced you have a good reason. A
    `for` loop is usually easier to read.

Combinators *are* preferable for shorter chains and for cases where the
combinator itself provides a lot of logic that would otherwise have to be
written out in the corresponding `for` loop.

Examples

**Complex combinator chains**

Here's an example of a combinator chain that is hard to read because it involves
conditionals and mutates external state:

<div class='badcode'></div>

```rust
let mut error_count = 0;
let _processed_items: Vec<_> = items
    .into_iter()
    .map(transformation_that_may_fail)
    .map(|result| {
        if result.is_err() {
            error_count += 1;
        }
        result
    })
    .filter_map(Result::ok)
    .collect();
```

The corresponding `for` loop is easier to read:

<div class='goodcode'></div>

```rust
let mut error_count = 0;
let mut processed_items = Vec::with_capacity(items.len());

for item in items {
    match transformation_that_may_fail(item) {
        Ok(val) => processed_items.push(val),
        Err(_) => error_count += 1,
    }
}
```

**Combinator chains in for loops**

Avoid constructing a combinator chain in the header of a `for` loop:

<div class='badcode'></div>

```rust
for bug in bug_descriptions
    .iter()
    .filter_map(|description| parse_bug_description(description).ok())
    .filter(|bug| bug.priority <= Priority::P1)
{
    assign_bug(bug);
}
```

Instead, assign the combinator chain to a variable. This reduces clutter, and
the variable name documents what the combinator chain does:

<div class='goodcode'></div>

```rust
let urgent_bugs = bug_descriptions
    .iter()
    .filter_map(|description| parse_bug_description(description).ok())
    .filter(|bug| bug.priority <= Priority::P1);

for bug in urgent_bugs {
    assign_bug(bug);
}
```

**When to prefer a combinator chain**

Here's an example where a combinator chain is preferable:

<div class='goodcode'></div>

```rust
let threshold_exceeded = values.iter().any(|&v| v > threshold);
```

The corresponding for loop is harder to read and reinvents the logic contained
in `any()`:

<div class='badcode'></div>

```rust
let mut threshold_exceeded = false;
for v in values {
  if v > threshold {
    threshold_exceeded = true;
    break;
  }
}
```

<a id="catch-unwind"></a>

### Don't call `panic::catch_unwind`

Use of `panic::catch_unwind` is prohibited in first-party Rust code.

Exceptions:

*   It is acceptable as a defense in depth mechanism as long as it is never
    *relied* upon for any properties. A codebase that is already attempting to
    avoid panics may choose to wrap critical entry points with a `catch_unwind`
    recovery mechanism just in case a panic slips through. Code authors must
    convince the reviewer that the codebase is doing most of what it can to
    avoid panics. This exception only applies to code that has the possibility
    of being run with `panic=unwind` (so this does not apply to
    <span class=chrome>Chrome</span>, <span class=android>Android</span>,
    <span class=fuchsia>Fuchsia</span>).

Rationale

Rust code may be used in many environments, and `panic::catch_unwind` will only
function correctly in environments with `panic=unwind`. While the final panic
disposition of prod binaries has not yet been determined, Chrome, Android, and
Fuchsia all require `panic=abort`.

<a id="prefer-format-or-write"></a>

### Prefer `format!` / `write!` for concatenation and substitution

Prefer `format!()` and `write!()` to other alternatives in the following
situations:

*   To concatenate more than two strings. For example, use
    `format!("{a}{b}{c}")` instead of `a + b + c`.
*   To perform substitutions on a literal string (instead of using
    `str::replace`).

Rationale

*   `format!` / `write!` require fewer allocations than concatenating strings
    using `+`.
*   Prefer standard format strings to inventing your own templating syntax.

<a id="test-framework"></a>

## Use the right per-codebase test framework

Most codebases use their own specific test framework rather than `#[test]`.

*   <span class="chrome">Chrome</span> Use
    [rust_gtest_interop](https://source.chromium.org/chromium/chromium/src/+/main:testing/rust_gtest_interop/).
    This makes it possible to integrate Rust tests into C++ test binaries.

*   <span class="fuchsia">Fuchsia</span> Use `#[fuchsia::test]`. See
    [here](https://fuchsia.dev/fuchsia-src/development/languages/rust/testing.md)
    for more details.
