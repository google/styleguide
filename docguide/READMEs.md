# README.md files

About README.md files.

1.  [Overview](#overview)
1.  [Guidelines](#guidelines)
1.  [Filename](#filename)
1.  [Contents](#contents)
1.  [Example](#example)

## Overview

`README.md` files are Markdown files that describe a directory.
GitHub and Gitiles renders it when you browse the directory.

For example, the file /README.md is rendered when you view the contents of the
containing directory:

https://github.com/google/styleguide/tree/gh-pages

Also `README.md` at `HEAD` ref is rendered by Gitiles when displaying repository
index:

https://gerrit.googlesource.com/gitiles/

## Guidelines

**`README.md` files are intended to provide orientation for engineers browsing
your code, especially first-time users.** The `README.md` is likely the first
file a reader encounters when they browse a directory that
contains your code. In this way, it acts as a landing page for the directory.

We recommend that top-level directories for your code have an up-to-date
`README.md` file. This is especially important for package directories that
provide interfaces for other teams.

### Filename

Use `README.md`.

Files named `README` are not displayed in the directory view in Gitiles.

### Contents

At minimum, every package-level `README.md` should include or point to the
following information:

1.  **What** is in this package/library and what's it used for.
2.  **Who** to contact.
3.  **Status**: whether this package/library is deprecated, or not for general
    release, etc.
4.  **More info**: where to go for more detailed documentation, such as:
     * An overview.md file for more detailed conceptual information.
     * Any API documentation for using this package/library.

## Example

```markdown
# APIs

This is the top-level directory for all externally-visible APIs, plus some
private APIs under `internal/` directories.
See [API Style Guide](docs/apistyle.md) for more information.

*TL;DR*: API definitions and configurations should be defined in `.proto` files,
checked into `apis/`.

...
```
