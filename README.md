# Google Style Guides

Every major open-source project has its own style guide: a set of conventions
(sometimes arbitrary) about how to write code for that project. It is much
easier to understand a large codebase when all the code in it is in a consistent
style.

“Style” covers a lot of ground, from “use camelCase for variable names” to
“never use global variables” to “never use exceptions.” This project
([google/styleguide](https://github.com/google/styleguide)) links to the style
guidelines we use for Google code. If you are modifying a project that
originated at Google, you may be pointed to this page to see the style guides
that apply to that project.

*   [Angular Style Guide][angular]
*   [Common Lisp Style Guide][cl]
*   [C++ Style Guide][cpp]
*   [C# Style Guide][csharp]
*   [Effective Dart][dart]
*   [Go Style Guide][go]
*   [Haskell Style Guide][haskell]
*   [HTML/CSS Style Guide][htmlcss]
*   [JavaScript Style Guide][js]
*   [Java Style Guide][java]
*   [JSON Style Guide][json]
*   [Kotlin Style Guide][kotlin]
*   [Markdown Style Guide][markdown]
*   [Objective-C Style Guide][objc]
*   [Python Style Guide][py]
*   [R Style Guide][r]
*   [Rust Style Guide][rust]
*   [Shell Style Guide][sh]
*   [Swift Style Guide][swift]
*   [TCL/TK Style Guide][tcltk]
*   [TypeScript Style Guide][ts]
*   [Verilog Style Guide][verilog]
*   [Vim script Style Guide][vim]
*   [XML Document Format Style Guide][xml]

## Source Code Management

Since projects are largely maintained in a [VCS], writing good commit messages
is important to long term project health. Please refer to
[How to Write a Git Commit Message](https://cbea.ms/git-commit/) as an excellent
resource. While it explicitly refers to the Git [SCM], its principles apply to
any system, and many Git conventions are trivial to translate to others.

## Editors & Tools

Google engineers use a wide variety of editors & IDEs.

*   Eclipse & IntelliJ
    *   C++: [eclipse-cpp-google-style.xml](./eclipse-cpp-google-style.xml)
    *   Java: <https://github.com/google/google-java-format>
*   Emacs: [google-c-style.el][emacs]
*   Vim: <https://github.com/google/vim-codefmt>
    *   Python: [google_python_style.vim](./google_python_style.vim)

We used to host the cpplint tool, but we stopped making internal updates public.
An open source community has forked the project, so users are encouraged to use
<https://github.com/cpplint/cpplint> instead.

## Contributing

With few exceptions, these style guides are copies of Google's internal style
guides to assist developers working on Google owned and originated open source
projects. Changes to the style guides are made to the internal style guides
first and eventually copied into the versions found here. **External
contributions are not accepted.** Pull requests are regularly closed without
comment.

While many of these guides are hosted directly in this project, others might be
hosted in other projects. Sometimes those projects are also maintained by
Google, sometimes they are wider community projects that Google contributes to
like anyone else. Before reporting issues against a particular language/guide,
please check where the guide is hosted.

People can file [issues using the GitHub tracker][gh-tracker]. Issues that raise
questions, justify changes on technical merits, or point out obvious mistakes
may get some engagement and could in theory lead to changes, but we are
primarily optimizing for Google's internal needs.

## Licensing

The style guides in this project are licensed under the CC-By 3.0 License, which
encourages you to share these documents. See
<https://creativecommons.org/licenses/by/3.0/> for more details.

Code samples are licensed under the Apache 2.0 License. See
<https://www.apache.org/licenses/LICENSE-2.0> for more details.

<a rel="license" href="https://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/88x31.png" /></a>

[angular]: https://angular.dev/style-guide
[cpp]: https://google.github.io/styleguide/cppguide.html
[csharp]: csharpguide.md
[swift]: https://google.github.io/swift/
[objc]: objcguide.md
[gh-tracker]: https://github.com/google/styleguide/issues
[go]: go/
[haskell]: haskellguide.md
[java]: https://google.github.io/styleguide/javaguide.html
[json]: jsoncguide.md
[kotlin]: https://developer.android.com/kotlin/style-guide
[py]: pyguide.md
[r]: Rguide.md
[rust]: rustguide.md
[sh]: shellguide.md
[tcltk]: https://wiki.tcl-lang.org/page/Dodekalogue
[htmlcss]: htmlcssguide.md
[js]: jsguide.md
[markdown]: docguide/style.md
[ts]: https://google.github.io/styleguide/tsguide.html
[cl]: lispguide.md
[verilog]: verilogguide.md
[vim]: vimscriptguide.md
[emacs]: https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el
[xml]: xmlguide.md
[dart]: https://www.dartlang.org/guides/language/effective-dart
[SCM]: https://en.wikipedia.org/wiki/Source_control_management
[VCS]: https://en.wikipedia.org/wiki/Version_control_system
