# Markdown style guide

Much of what makes Markdown refreshing is the ability to write plain text and get
great formatted output as a result. To keep the slate clean for the next author,
your Markdown should be simple and consistent with the whole corpus wherever
possible.

We seek to balance three goals:

1.  *Source text is readable and portable.*
2.  *The Markdown corpus is maintainable over time and across teams.*
3.  *The syntax is simple and easy to remember.*

Contents:

1.  [Minimum viable documentation](#minimum-viable-documentation)
1.  [Better is better than best](#better-is-better-than-best)
1.  [Capitalization](#capitalization)
1.  [Document layout](#document-layout)
1.  [Table of contents](#table-of-contents)
1.  [Character line limit](#character-line-limit)
1.  [Trailing whitespace](#trailing-whitespace)
1.  [Headings](#headings)
    1.  [ATX-style headings](#atx-style-headings)
    1.  [Use unique, complete names for headings](#use-unique-complete-names-for-headings)
    1.  [Add spacing to headings](#add-spacing-to-headings)
    1.  [Use a single H1 heading](#use-a-single-h1-heading)
    1.  [Capitalization of titles and headers](#capitalization-of-titles-and-headers)
1.  [Lists](#lists)
    1.  [Use lazy numbering for long lists](#use-lazy-numbering-for-long-lists)
    1.  [Nested list spacing](#nested-list-spacing)
1.  [Code](#code)
    1.  [Inline](#inline)
    1.  [Use code span for escaping](#use-code-span-for-escaping)
    1.  [Codeblocks](#codeblocks)
        1.  [Declare the language](#declare-the-language)
        1.  [Escape newlines](#escape-newlines)
        1.  [Use fenced code blocks instead of indented code blocks](#use-fenced-code-blocks-instead-of-indented-code-blocks)
        1.  [Nest codeblocks within lists](#nest-codeblocks-within-lists)
1.  [Links](#links)
    1.  [Use explicit paths for links within Markdown](#use-explicit-paths-for-links-within-markdown)
    1.  [Avoid relative paths unless within the same directory](#avoid-relative-paths-unless-within-the-same-directory)
    1.  [Use informative Markdown link titles](#use-informative-markdown-link-titles)
    1.  [Reference links](#reference-links)
        1.  [Use reference links for long links](#use-reference-links-for-long-links)
        1.  [Use reference links to reduce duplication](#use-reference-links-to-reduce-duplication)
        1.  [Define reference links after their first use](#define-reference-links-after-their-first-use)
1.  [Images](#images)
1.  [Tables](#tables)
1.  [Strongly prefer Markdown to HTML](#strongly-prefer-markdown-to-html)

## Minimum viable documentation

A small set of fresh and accurate docs is better than a sprawling, loose
assembly of "documentation" in various states of disrepair.

The **Markdown way** encourages engineers to take ownership of their docs and
keep them up to date with the same zeal we keep our tests in good order. Strive
for this.

*   Identify what you really need: release docs, API docs, testing guidelines.
*   Delete cruft frequently and in small batches.

## Better is better than best

The standards for an internal documentation review are different from the
standards for code reviews. Reviewers should ask for improvements, but in
general, the author should always be able to invoke the "Better/Best Rule."

Fast iteration is your friend. To get long-term improvement, **authors must stay
productive** when making short-term improvements. Set lower standards for each
CL, so that **more such CLs** can happen.

As a reviewer of a documentation CL:

1.  When reasonable, LGTM immediately and trust that comments will be fixed
    appropriately.
2.  Prefer to suggest an alternative rather than leaving a vague comment.
3.  For substantial changes, start your own follow-up CL instead. Especially try
    to avoid comments of the form "You should *also*...".
4.  On rare occasions, hold up submission if the CL actually makes the docs
    worse. It's okay to ask the author to revert.

As an author:

1.  Avoid wasting cycles with trivial argument. Capitulate early and move on.
2.  Cite the Better/Best Rule as often as needed.

## Capitalization

Use the original names of products, tools and binaries, preserving the
capitalization. E.g.:

```markdown
# Markdown style guide

`Markdown` is a dead-simple platform for internal engineering documentation.
```

and not

```markdown
# markdown bad style guide example

`markdown` is a dead-simple platform for internal engineering documentation.
```

## Document layout

In general, documents benefit from some variation of the following layout:

```markdown
# Document Title

Short introduction.

[TOC]

## Topic

Content.

## See also

* https://link-to-more-info
```

1.  `# Document title`: The first heading should be a level-one heading, ideally
    the same or nearly the same as the filename. The first level-one heading is
    used as the page `<title>`.

1.  `author`: *Optional*. If you'd like to claim ownership of the document or
    if you are very proud of it, add yourself under the title. However,
    revision history generally suffices.

1.  `Short introduction.` 1–3 sentences providing a high-level overview of the
    topic. Imagine yourself as a complete newbie who landed on your "Extending Foo" doc
    and doesn't know the most basic information you take for granted. "What is
    Foo? Why would I extend it?"

1.  `[TOC]`: if you use hosting that supports table of contents, such as Gitiles,
    put `[TOC]` after the short introduction. See [`[TOC]` documentation][TOC-docs].

1.  `## Topic`: The rest of your headings should start from level 2.

1.  `## See also`: Put miscellaneous links at the bottom for the user who wants
    to know more or didn't find what they needed.

[TOC-docs]: https://gerrit.googlesource.com/gitiles/+/HEAD/Documentation/markdown.md#Table-of-contents

## Table of contents

### Use a `[TOC]` directive

Use a [`[TOC]` directive][TOC-docs] unless all
of your content is above the fold[^above] on a laptop.

[^above]: Content is "above the fold" if it is visible when the page is first
    displayed. Content is "below the fold" if it is hidden until the user
    scrolls down the page on a computer or literally unfolds a document
    such as a newspaper.

### Place the `[TOC]` directive after the introduction

Place the `[TOC]` directive after your page's introduction and before the first
H2 heading. For example:

```markdown
# My Page

This is my introduction **before** the TOC.

[TOC]

## My first H2
```

```markdown
# My Page

[TOC]

This is my introduction **after** the TOC where it should not be.

## My first H2
```

For users who read your documentation visually, it doesn't matter where your
`[TOC]` directive is placed, as Markdown always displays the TOC toward the top and
to the right of the page. However, `[TOC]` placement matters a lot when screen
readers or keyboard controls are involved.

That's because `[TOC]` inserts the HTML for the table of contents into the DOM
wherever you've included the directive in your Markdown file. If, for example,
you place the directive at the very bottom of your file, screen readers won't
read it until they get to the end of the document.

## Character line limit

Markdown content follows the residual convention of an 80-character line limit.
Why? Because it's what most of us do for code.

*   **Tooling integration**: All our tooling is designed around code, so the
    more our documents are formatted according to similar rules, the better
    these tools will work. For example, Code Search doesn't soft wrap.

*   **Quality**. The more engineers use their well-worn coding habits when
    creating and editing Markdown content, the better the quality. Markdown takes
    advantage of the excellent review culture we already have.

### Exceptions

Exceptions to the 80-character rule include:

*   Links
*   Tables
*   Headings
*   Code blocks

This means that lines with links are allowed to extend past column 80, along
with any relevant punctuation:

```markdown
*   See the
    [foo docs](https://gerrit.googlesource.com/gitiles/+/HEAD/Documentation/markdown.md).
    and find the logfile.
```

However, note that text before and after the link gets wrapped.

Tables may also run long. However, there are
[best practices for creating short, readable tables](#tables).

```markdown
Foo                                                                           | Bar | Baz
----------------------------------------------------------------------------- | --- | ---
Somehow-unavoidable-long-cell-filled-with-content-that-simply-refuses-to-wrap | Foo | Bar
```

## Trailing whitespace

Don't use trailing whitespace. Use a trailing backslash to break lines.

The [CommonMark spec](http://spec.commonmark.org/0.20/#hard-line-breaks) decrees
that two spaces at the end of a line should insert a `<br />` tag. However, many
directories have a presubmit check for trailing whitespace, and many IDEs will
clean it up anyway.

Use a trailing backslash, sparingly:

```markdown
For some reason I just really want a break here,\
though it's probably not necessary.
```

Best practice is to avoid the need for a `<br />` altogether. A pair of newlines
will create a paragraph tag; get used to that.

## Headings

### ATX-style headings

```markdown
# Heading 1

## Heading 2
```

Headings with `=` or `-` underlines can be annoying to maintain and don't fit
with the rest of the heading syntax. An editor has to ask: Does `---` mean H1 or
H2?

```markdown
Heading - do you remember what level? DO NOT DO THIS.
---------
```

### Use unique, complete names for headings

Use unique and fully descriptive names for each heading, even for sub-sections.
Since link anchors are constructed from headings, this helps ensure that the
automatically-constructed anchor links are intuitive and clear.

For example, instead of:

```markdown
## Foo
### Summary
### Example
## Bar
### Summary
### Example
```

prefer:

```markdown
## Foo
### Foo summary
### Foo example
## Bar
### Bar summary
### Bar example
```

### Add spacing to headings

Prefer spacing after `#` and newlines before and after:

```markdown
...text before.

## Heading 2

Text after...
```

Lack of spacing makes it a little harder to read in source:

```markdown
...text before.

##Heading 2
Text after... DO NOT DO THIS.
```

### Use a single H1 heading

Use one H1 heading as the title of your document. Subsequent headings should be
H2 or deeper. See [Document layout](#document-layout) for more information.

### Capitalization of titles and headers

Follow the guidance for
[capitalization](https://developers.google.com/style/capitalization#capitalization-in-titles-and-headings)
in the
[Google Developer Documentation Style Guide](https://developers.google.com/style/).

## Lists

### Use lazy numbering for long lists

Markdown is smart enough to let the resulting HTML render your numbered lists
correctly. For longer lists that may change, especially long nested lists, use
"lazy" numbering:

```markdown
1.  Foo.
1.  Bar.
    1.  Foofoo.
    1.  Barbar.
1.  Baz.
```

However, if the list is small and you don't anticipate changing it, prefer fully
numbered lists, because it's nicer to read in source:

```markdown
1.  Foo.
2.  Bar.
3.  Baz.
```

### Nested list spacing

When nesting lists, use a 4-space indent for both numbered and bulleted lists:

```markdown
1.  Use 2 spaces after the item number, so the text itself is indented 4 spaces.
    Use a 4-space indent for wrapped text.
2.  Use 2 spaces again for the next item.

*   Use 3 spaces after a bullet, so the text itself is indented 4 spaces.
    Use a 4-space indent for wrapped text.
    1.  Use 2 spaces with numbered lists, as before.
        Wrapped text in a nested list needs an 8-space indent.
    2.  Looks nice, doesn't it?
*   Back to the bulleted list, indented 3 spaces.
```

The following works, but it's very messy:

```markdown
* One space,
with no indent for wrapped text.
     1. Irregular nesting... DO NOT DO THIS.
```

Even when there's no nesting, using the 4 space indent makes layout consistent
for wrapped text:

```markdown
*   Foo,
    wrapped with a 4-space indent.

1.  Two spaces for the list item
    and 4 spaces before wrapped text.
2.  Back to 2 spaces.
```

However, when lists are small, not nested, and a single line, one space can
suffice for both kinds of lists:

```markdown
* Foo
* Bar
* Baz.

1. Foo.
2. Bar.
```

## Code

### Inline

&#96;Backticks&#96; designate `inline code` that will be rendered literally. Use
them for short code quotations, field names, and more:

```markdown
You'll want to run `really_cool_script.sh arg`.

Pay attention to the `foo_bar_whammy` field in that table.
```

Use inline code when referring to file types in a generic sense, rather than a
specific existing file:

```markdown
Be sure to update your `README.md`!
```

### Use code span for escaping

When you don't want text to be processed as normal Markdown, like a fake path or
example URL that would lead to a bad autolink, wrap it in backticks:

```markdown
An example Markdown shortlink would be: `Markdown/foo/Markdown/bar.md`

An example query might be: `https://www.google.com/search?q=$TERM`
```

### Codeblocks

For code quotations longer than a single line, use a fenced code block:

<pre>
```python
def Foo(self, bar):
  self.bar = bar
```
</pre>

#### Declare the language

It is best practice to explicitly declare the language, so that neither the
syntax highlighter nor the next editor must guess.

#### Use fenced code blocks instead of indented code blocks

Four-space indenting is also interpreted as a code block. However, we strongly
recommend fencing for all code blocks.

Indented code blocks can sometimes look cleaner in the source, but they have
several drawbacks:

*   You cannot specify the language. Some Markdown features are tied to language
    specifiers.
*   The beginning and end of the code block are ambiguous.
*   Indented code blocks are harder to search for in Code Search.

```markdown
You'll need to run:

    bazel run :thing -- --foo

And then:

    bazel run :another_thing -- --bar

And again:

    bazel run :yet_again -- --baz
```

#### Escape newlines

Because most command-line snippets are intended to be copied and pasted directly
into a terminal, it's best practice to escape any newlines. Use a single
backslash at the end of the line:

<pre>
```shell
$ bazel run :target -- --flag --foo=longlonglonglonglongvalue \
  --bar=anotherlonglonglonglonglonglonglonglonglonglongvalue
```
</pre>

#### Nest codeblocks within lists

If you need a code block within a list, make sure to indent it so as to not
break the list:

```markdown
*   Bullet.

    ```c++
    int foo;
    ```

*   Next bullet.
```

You can also create a nested code block with 4 spaces. Simply indent 4
additional spaces from the list indentation:

```markdown
*   Bullet.

        int foo;

*   Next bullet.
```

## Links

Long links make source Markdown difficult to read and break the 80 character
wrapping. **Wherever possible, shorten your links**.

### Use explicit paths for links within Markdown

Use the explicit path for Markdown links. For example:

```markdown
[...](/path/to/other/markdown/page.md)
```

You don't need to use the entire qualified URL:

```markdown
[...](https://bad-full-url.example.com/path/to/other/markdown/page.md)
```

### Avoid relative paths unless within the same directory

Relative paths are fairly safe within the same directory. For example:

```markdown
[...](other-page-in-same-dir.md)
[...](/path/to/another/dir/other-page.md)
```

Avoid relative links if you need to specify other directories with `../`:

```markdown
[...](../../bad/path/to/another/dir/other-page.md)
```

### Use informative Markdown link titles

Markdown link syntax allows you to set a link title. Use it wisely. Users often
do not read documents; they scan them.

Links catch the eye. But titling your links "here," "link," or simply
duplicating the target URL tells the hasty reader precisely nothing and is a
waste of space:

```markdown
DO NOT DO THIS.

See the Markdown guide for more info: [link](markdown.md), or check out the
style guide [here](style.md).

Check out a typical test result:
[https://example.com/foo/bar](https://example.com/foo/bar).
```

Instead, write the sentence naturally, then go back and wrap the most
appropriate phrase with the link:

```markdown
See the [Markdown guide](markdown.md) for more info, or check out the
[style guide](style.md).

Check out a
[typical test result](https://example.com/foo/bar).
```

### Reference

For long links or image URLs, you may want to split the link use from the link
definition, like this:

<!-- Known bug: We use a zero-width non-breaking space (U+FEFF) here to prevent -->
<!-- reference links from rendering within code blocks. -->

```markdown
See the [Markdown style guide][style], which has suggestions for making docs more
readable.

﻿[style]: http://Markdown/corp/Markdown/docs/reference/style.md
```

#### Use reference links for long links

Use reference links where the length of the link would detract from the
readability of the surrounding text if it were inlined. Reference links make it
harder to see the destination of a link in source text, and add additional
syntax.

In this example, reference link usage is not appropriate, because the link is
not long enough to disrupt the flow of the text:

```markdown
DO NOT DO THIS.

The [style guide][style_guide] says not to use reference links unless you have
to.

﻿[style_guide]: https://google.com/Markdown-style
```

Just inline it instead:

```markdown
https://google.com/Markdown-style says not to use reference links unless you have to.
```

In this example, the link destination is long enough that it makes sense to use
a reference link:

```markdown
The [style guide] says not to use reference links unless you have to.

﻿[style guide]: https://docs.google.com/document/d/13HQBxfhCwx8lVRuN2Wf6poqvAfVeEXmFVcawP5I6B3c/edit
```

Use reference links more often in tables. It is particularly important to keep
table content short, since Markdown does not provide a facility to break text in
cell tables across multiple lines, and smaller tables are more readable.

For example, this table's readability is worsened by inline links:

```markdown
DO NOT DO THIS.

Site                                                             | Description
---------------------------------------------------------------- | -----------------------
[site 1](http://google.com/excessively/long/path/example_site_1) | This is example site 1.
[site 2](http://google.com/excessively/long/path/example_site_2) | This is example site 2.
```

Instead, use reference links to keep the line length manageable:

```markdown
Site     | Description
-------- | -----------------------
[site 1] | This is example site 1.
[site 2] | This is example site 2.

﻿[site 1]: http://google.com/excessively/long/path/example_site_1
﻿[site 2]: http://google.com/excessively/long/path/example_site_2
```

#### Use reference links to reduce duplication

Consider using reference links when referencing the same link destination
multiple times in a document, to reduce duplication.

#### Define reference links after their first use

We recommend putting reference link definitions just before the next heading, at
the end of the section in which they're first used. If your editor has its own
opinion about where they should go, don't fight it; the tools always win.

We define a "section" as all text between two headings. Think of reference links
like footnotes, and the current section like the current page.

This arrangement makes it easy to find the link destination in source view,
while keeping the flow of text free from clutter. In long documents with lots of
reference links, it also prevents "footnote overload" at the bottom of the file,
which makes it difficult to pick out the relevant link destination.

There is one exception to this rule: reference link definitions that are used in
multiple sections should go at the end of the document. This avoids dangling
links when a section is updated or moved.

In the following example, the reference definition is far from its initial use,
which makes the document harder to read:

```markdown
# Header FOR A BAD DOCUMENT

Some text with a [link][link_def].

Some more text with the same [link][link_def].

## Header 2

... lots of text ...

## Header 3

Some more text using a [different_link][different_link_def].

﻿[link_def]: http://reallyreallyreallylonglink.com
﻿[different_link_def]: http://differentreallyreallylonglink.com
```

Instead, put it just before the header following its first use:

```markdown
# Header

Some text with a [link][link_def].

Some more text with the same [link][link_def].

﻿[link_def]: http://reallyreallyreallylonglink.com

## Header 2

... lots of text ...

## Header 3

Some more text using a [different_link][different_link_def].

﻿[different_link_def]: http://differentreallyreallylonglink.com
```

## Images

See [image syntax](https://gerrit.googlesource.com/gitiles/+/HEAD/Documentation/markdown.md#Images).

Use images sparingly, and prefer simple screenshots. This guide is designed
around the idea that plain text gets users down to the business of communication
faster with less reader distraction and author procrastination. However, it's
sometimes very helpful to show what you mean.

*   Use images when it's easier to *show* a reader something than to *describe
    it*. For example, explaining how to navigate a UI is often easier with an
    image than text.
*   Make sure to provide appropriate text to describe your image. Readers who
    are not sighted cannot see your image and still need to understand the
    content! See the alt text best practices below.

## Tables

Use tables when they make sense: for the presentation of tabular data that needs
to be scanned quickly.

Avoid using tables when your data could easily be presented in a list. Lists are
much easier to write and read in Markdown.

For example:

```markdown
DO NOT DO THIS

Fruit  | Metrics      | Grows on | Acute curvature    | Attributes                                                                                                  | Notes
------ | ------------ | -------- | ------------------ | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------
Apple  | Very popular | Trees    |                    | [Juicy](http://cs/SomeReallyReallyReallyReallyReallyReallyReallyReallyLongQuery), Firm, Sweet               | Apples keep doctors away.
Banana | Very popular | Trees    | 16 degrees average | [Convenient](http://cs/SomeDifferentReallyReallyReallyReallyReallyReallyReallyReallyLongQuery), Soft, Sweet | Contrary to popular belief, most apes prefer mangoes. Don't you? See the [design doc][banana_v2] for the newest hotness in bananiels.
```

This table illustrates a few typical problems:

*   **Poor distribution**: Several columns don't differ across rows, and some
    cells are empty. This is usually a sign that your data may not benefit from
    tabular display.

*   **Unbalanced dimensions**: There are a small number of rows relative to
    columns. When this ratio is unbalanced in either direction, a table becomes
    little more than an inflexible format for text.

*   **Rambling prose** in some cells. Tables should tell a succinct story at a
    glance.

[Lists](#lists) and subheadings sometimes suffice to present the same
information. Let's see this data in list form:

```markdown
## Fruits

Both types are highly popular, sweet, and grow on trees.

### Apple

*   [Juicy](http://SomeReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyLongURL)
*   Firm

Apples keep doctors away.

### Banana

*   [Convenient](http://cs/SomeDifferentReallyReallyReallyReallyReallyReallyReallyReallyLongQuery)
*   Soft
*   16 degrees average acute curvature.

Contrary to popular belief, most apes prefer mangoes. Don't you?

See the [design doc][banana_v2] for the newest hotness in bananiels.
```

The list form is more spacious, and arguably therefore much easier for the
reader to find what interests her in this case.

However, there are times a table is the best choice. When you have:

*   Relatively uniform data distribution across two dimensions.
*   Many parallel items with distinct attributes.

In those cases, a table format is just the thing. In fact, a compact table can
improve readability:

```markdown
Transport        | Favored by     | Advantages
---------------- | -------------- | -----------------------------------------------
Swallow          | Coconuts       | [Fast when unladen][airspeed]
Bicycle          | Miss Gulch     | [Weatherproof][tornado_proofing]
X-34 landspeeder | Whiny farmboys | [Cheap][tosche_station] since the XP-38 came out

﻿[airspeed]: http://google3/airspeed.h
﻿[tornado_proofing]: http://google3/kansas/
﻿[tosche_station]: http://google3/power_converter.h
```

Note that [reference links](#reference-links) are used to keep the table cells
manageable.

## Strongly prefer Markdown to HTML

Please prefer standard Markdown syntax wherever possible and avoid HTML hacks.
If you can't seem to accomplish what you want, reconsider whether you really
need it. Except for [big tables](#tables), Markdown meets almost all needs
already.

Every bit of HTML hacking reduces the readability and portability of our
Markdown corpus. This in turn limits the usefulness of integrations with other
tools, which may either present the source as plain text or render it. See
[Philosophy](philosophy.md).

Gitiles does not render HTML.
