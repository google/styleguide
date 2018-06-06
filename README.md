Move Digital Style Guides
=========================

Every organization must have its own style guide: a set of conventions
(sometimes arbitrary) about how to write code for that organization. It is
much easier to understand a large codebase when all the code in it is in a
consistent style. There is also benefit to be had from that style guide
matching (or closely following) a more widely used style guide.

“Style” covers a lot of ground, from “use camelCase for variable names” to
“never use global variables” to “never use exceptions.” This project
([AmanaAdvisors/styleguide](https://github.com/AmanaAdvisors/styleguide))
links to the style guidelines we use for Move Digital code. Much of it is
borrowed wholesale from the Google style guide (see the "arbitrary" and
"matching"/"following" above), with tiny, specific changes to better match
the prevailing status quo at the time of adoption.

The core and main focus of this project is the [Java Style Guide][java], as
we are primarily a Java shop. For that end it provides [Eclipse][java_eclipse]
and [IntelliJ][java_intellij] code style profiles, which imported into your
IDE of choice, allow you to quickly format code (and more easily write
properly formatted code to begin with).

This project also holds style guides for the [C++][cpp], [Objective-C][objc],
[Python][py], [R][r], [Shell Script][sh], [Common Lisp][cl], and
[Vimscript][vim]; as well as [cpplint][cpplint], a tool to assist with style
guide compliance, and [c-style.el][emacs], an Emacs settings file for C/C++.
If you find yourself writing code in one of these languages, it is arguably
better to begin with some rules in place.

The notable absentees from this list are JavaScript/HTML/CSS. The style
guides for these are covered in the UX team's [Coding Conventions and Team
Best Practices][ux_style] document.

If your project requires that you create a new XML document format, the [XML
Document Format Style Guide][xml] may be helpful. In addition to actual style
rules, it also contains advice on designing your own vs. adapting an existing
format, on XML instance document formatting, and on elements vs. attributes.

The following style guides live outside of this project:
[Go Code Review Comments][go] and [Effective Dart][dart].

The style guides in this project are licensed under the CC-By 3.0 License,
which encourages you to share these documents.
See [https://creativecommons.org/licenses/by/3.0/][ccl] for more details.


**How to integrate Java style settings in Intellij IDEA?**

1. Make sure you have intellij-java-style.xml locally.
2. In IDEA menu, follow
Intellij IDEA -> Preferences -> (In opened window expand) Editor -> Code Style -> Java -> Find _"Scheme"_ label and next to the value of it find the gear icon.
3. Click on the icon -> Import Scheme -> Intellij Idea Code Style XML -> Find and select intellij-java-style.xml on the local disk.


<a rel="license" href="https://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/88x31.png" /></a>

[java]: https://amanaadvisors.github.io/styleguide/javaguide.html
[java_eclipse]: https://raw.githubusercontent.com/amanaadvisors/styleguide/gh-pages/eclipse-java-style.xml
[java_intellij]: https://raw.githubusercontent.com/amanaadvisors/styleguide/gh-pages/intellij-java-style.xml
[ux_style]: https://amananexus.atlassian.net/wiki/spaces/MUWD/pages/461734025/Coding+Conventions+and+Team+Best+Practises
[cpp]: https://amanaadvisors.github.io/styleguide/cppguide.html
[objc]: objcguide.md
[py]: https://amanaadvisors.github.io/styleguide/pyguide.html
[r]: https://amanaadvisors.github.io/styleguide/Rguide.xml
[sh]: https://amanaadvisors.github.io/styleguide/shell.xml
[cl]: https://amanaadvisors.github.io/styleguide/lispguide.xml
[vim]: https://amanaadvisors.github.io/styleguide/vimscriptguide.xml
[cpplint]: https://github.com/amanaadvisors/styleguide/tree/gh-pages/cpplint
[emacs]: https://raw.githubusercontent.com/amanaadvisors/styleguide/gh-pages/c-style.el
[xml]: https://amanaadvisors.github.io/styleguide/xmlstyle.html
[go]: https://golang.org/wiki/CodeReviewComments
[dart]: https://www.dartlang.org/guides/language/effective-dart
[ccl]: https://creativecommons.org/licenses/by/3.0/
