# Style Guides

## Table of Contents

1.   [NexTraq](#nextraq)
     1.   [Modifications](#modifications)
          1.   [General](#general)
          1.   [Java](#java)
          1.   [JavaScript](#javascript)
     1.   [Formatting Tools](#formatting-tools)
          1.   [IDE Google Style Config](#ide-google-style-config)
          1.   [google-java-format](#google-java-format)
          1.   [ESLint](#eslint)
          1.   [Markdown](#markdown)
               1.   [markdownlint](#markdownlint)
               1.   [remark](#remark)
               1.   [Prettier](#prettier)
               1.   [Markdown Navigator](#markdown-navigator)
     1.   [Future Work](#future-work)
1.   [Google Style Guides](#google-style-guides)

## NexTraq

This repo contains the NexTraq style guides, primarily based on the Google Style
Guides for the relevant languages. It does, however, also include the Vue.js
style guide. adherence to the following guides is required for submission of new
code:

*   [Java](javaguide.html)
*   JavaScript
    *   [JS](jsguide.html)
    *   [Vue.js](https://vuejs.org/v2/style-guide/) (Non-Google guide)
*   Markdown
    *   [Google Markdown Guide](docguide/style.md)
    *   [Markdown Stye Guide](https://cirosantilli.com/markdown-style-guide)
        (Non-Google guide): Anywhere where this guide differs from the Google
        guide, the Google guide is preferred.
*   [Documentation](docguide) (Please read all documents in this folder)

Engineers are asked to read through the relevant guide before making a change in
a given language. Any points that are not mentioned or are left ambiguous in the
guides are left up to the engineer’s discretion. Reviewers are also asked to
ensure that code adheres to the style guide before approving changes.

### Modifications

#### General

Constants will be named in SCREAMING_SNAKE_CASE. Constants will be defined as
“Fields which can neither be reassigned, nor have the values they reference
changed in any way.” In other words, a field must be final, const, or whatever
the equivalent of the particular language is, and the object it points to must
be fully immutable. Generally speaking, these values will be at the top level
scope (global, class, etc.). In Java, they will usually be static. If you are
considering making a constant that is not at the top level scope, please think
carefully about your use case and consider alternatives. (There are no linting
configurations for this rule; it is the responsibility of the code author and
reviewer to ensure it is followed)

#### Java

*   Indent size will be 4. This will also imply:
    *   Continuation indent size is 8
    *   Tab size is 4

#### JavaScript

*   no-multi-str: We have disabled the rule that disallows multiline strings
*   es-module-exports: We will set the rule enforcing that only symbols used in
    other modules are exported to ‘warn’. In vanilla JS, this rule is important,
    but it is fundamentally incompatible with Vue.js

### Formatting Tools

<!-- TODO: There are more good ones; add them -->

The first class of tools is those which automatically detect and/or fix style
errors in code. It is strongly recommended to use these tools before sending
changes out for review. Do note, however, that sometimes these tools will make
strange decisions in cases where the guide leaves some level of choice up to the
engineer (one particularly common case is choosing where to break a line that is
too long). As such, it is also recommended that the engineer go back over the
code after formatting to ensure it is as readable as possible.

#### IDE Google Style Config

Google provides configuration files which bring IDEs into compliance with the
Google style guide, specifically for [IntelliJ](intellij-java-google-style.xml)
and [Eclipse](eclipse-java-google-style.xml) . For IntelliJ, follow the
instructions
[here](https://www.jetbrains.com/help/idea/copying-code-style-settings.html) to
install the style guide. For Eclipse, follow the instructions
[here](https://help.eclipse.org/neon/index.jsp?topic=%2Forg.eclipse.jdt.doc.user%2Freference%2Fpreferences%2Fjava%2Fcodestyle%2Fref-preferences-formatter.htm).

#### [google-java-format](https://github.com/google/google-java-format)

This open source project provides a CLI tool as well as IDE integrations for
IntelliJ, Android Studio, and Eclipse. These provide both linting and automatic
formatting of Java files. This tool also has two options for integration with
Gradle:
[google-java-format-gradle-plugin](https://github.com/sherter/google-java-format-gradle-plugin)
and integration with a formatting tool called
[Spotless](https://github.com/diffplug/spotless/tree/master/plugin-gradle#applying-to-java-source-google-java-format).
These provide Gradle tasks which either verify or fix formatting errors in the
entire project. While the verification task may be useful for saving time and
creating presubmit hooks (more on this later), use of the formatting task is not
necessarily recommended in most cases due to the concern about odd formatting
decisions mentioned above. Note that this tool does not support configuration or
modification. If we decide we want to make adjustments to the style guide, we
will need to find another tool.

#### ESLint

One of the most popular linters/formatters for JS is known as ESLint. It is
configurable and configurations can be exported and shared. The
[eslint-config-google](https://github.com/google/eslint-config-google),
[eslint-plugin-vue](https://vuejs.github.io/eslint-plugin-vue/user-guide/), and
[vue-enterprise-boilerplate projects](https://github.com/chrisvfritz/vue-enterprise-boilerplate)
are Shareable Configurations for ESLint which matches the Google JS and Vue.js
style guides. Use of ESLint with these configs is recommend for JS engineers.

#### Markdown

There are several tools for formatting Markdown, though none of them by default
conform to the Google style guidelines. These tools are configurable, but
whether it is even possible to create a configuration that supports Google style
is even possible has not yet been investigated. They are, however, still useful
for making common formatting changes such as line length conformance.
Unfortunately, no Eclipse plugin that supports automatic formatting has been
found.

##### markdownlint

The primary CLI tool for formatting Markdown is markdownlint. There are three
implementations of this tool: one written in
[Ruby](https://github.com/markdownlint/markdownlint) and two written in Node.js
([markdownlint](https://github.com/DavidAnson/markdownlint),
[markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli)). The most
well supported is the Ruby implementation.

##### remark

[Remark](https://github.com/remarkjs/remark-github) is a processing and linting
library for Markdown built on node. It is a bit difficult to use and the
documentation is lacking, but it provides a wide array of rules as well as a
framework called plugins for extension of both rules and functionality. It can
be used as a CLI, an API, or as an extension to the
[unified](https://unifiedjs.com/) in node applications.

##### Prettier

There is a style conformance tool called [Prettier](https://prettier.io)
primarily intended for JS, but also has support for Markdown. Its Markdown
support relies on remark. It specifically differentiates itself from a linter,
but it seems to have a proper subset of lint functionality, as described
[here](https://prettier.io/docs/en/comparison.html). It is very easy to use and
configure, and has all of the mechanisms for running that remark does. It does
allow for auto-formatting, but does so by rewriting the entire file. It is
unclear whether it is possible to validate specific lines. Prettier does not
have a very extensive library of rules, in comparison to remark, and the plugins
feature, which allows for extended rulesets, is currently in beta.

##### [Markdown Navigator](https://github.com/vsch/idea-multimarkdown)

Markdown Navigator is an IntelliJ plugin which, with the paid version, supports
automatic formatting.

### Future Work

*   Add info about Swagger style conventions and formatting tools
*   Investigate Markdown formatter conformance with Google style
*   Gather and resolve opinions from other engineers on style, then
*   Document the adjustments here
*   Modify our linter/formatter configurations to reflect the adjustments
*   Investigate and implement enforcement presubmit checks
*   Investigate CI/CD role in presubmit checks

## Google Style Guides

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

This project holds the [C++ Style Guide][cpp], [Objective-C Style Guide][objc],
[Java Style Guide][java], [Python Style Guide][py], [R Style Guide][r], [Shell
Style Guide][sh], [HTML/CSS Style Guide][htmlcss], [JavaScript Style Guide][js],
[AngularJS Style Guide][angular], [Common Lisp Style Guide][cl], and [Vimscript
Style Guide][vim]. This project also contains [cpplint][cpplint], a tool to
assist with style guide compliance, and [google-c-style.el][emacs], an Emacs
settings file for Google style.

If your project requires that you create a new XML document format, the [XML
Document Format Style Guide][xml] may be helpful. In addition to actual style
rules, it also contains advice on designing your own vs. adapting an existing
format, on XML instance document formatting, and on elements vs. attributes.

The style guides in this project are licensed under the CC-By 3.0 License, which
encourages you to share these documents. See
[https://creativecommons.org/licenses/by/3.0/][ccl] for more details.

The following Google style guides live outside of this project: [Go Code Review
Comments][go] and [Effective Dart][dart].

<a rel="license" href="https://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/88x31.png" /></a>

[cpp]: https://google.github.io/styleguide/cppguide.html
[objc]: objcguide.md
[java]: https://google.github.io/styleguide/javaguide.html
[py]: https://google.github.io/styleguide/pyguide.html
[r]: https://google.github.io/styleguide/Rguide.html
[sh]: https://google.github.io/styleguide/shell.xml
[htmlcss]: https://google.github.io/styleguide/htmlcssguide.html
[js]: https://google.github.io/styleguide/jsguide.html
[angular]: https://google.github.io/styleguide/angularjs-google-style.html
[cl]: https://google.github.io/styleguide/lispguide.xml
[vim]: https://google.github.io/styleguide/vimscriptguide.xml
[cpplint]: https://github.com/google/styleguide/tree/gh-pages/cpplint
[emacs]: https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el
[xml]: https://google.github.io/styleguide/xmlstyle.html
[go]: https://golang.org/wiki/CodeReviewComments
[dart]: https://www.dartlang.org/guides/language/effective-dart
[ccl]: https://creativecommons.org/licenses/by/3.0/
