# READMEs

About README.md files.

1.  [Overview](#overview)
1.  [Readable README files](#readable-readme-files)
1.  [Where to put your README](#where-to-put-your-readme)
1.  [What to put in your README](#what-to-put-in-your-readme)

## Overview

A README is a short summary of the contents of a directory. The contents of the
file are displayed in GitHub and Gitiles when you view the contents of the
containing directory. README files provide critical information for people
browsing your code, especially first-time users.

This document covers how to create README files that are readable with GitHub
and Gitiles.

## Readable README files

**README files must be named `README.md`.** The file name *must* end with the
`.md` extension and is case sensitive.

For example, the file /README.md is rendered when you view the contents of the
containing directory:

https://github.com/google/styleguide/tree/gh-pages

Also `README.md` at `HEAD` ref is rendered by Gitiles when displaying repository
index:

https://gerrit.googlesource.com/gitiles/

## Where to put your README

Unlike all other Markdown files, `README.md` files should not be located inside
your product or library's documentation directory. `README.md` files should be
located in the top-level directory for your product or library's actual
codebase.

All top-level directories for a code package should have an up-to-date
`README.md` file. This is especially important for package directories that
provide interfaces for other teams.

## What to put in your README

At a minimum, your `README.md` file should contain a link to your user- and/or
team-facing documentation.

Every package-level `README.md` should include or point to the following
information:

1.  What is in this package or library and what's it used for.
1.  Points of contact.
1.  Status of whether this package or library is deprecated, or not for general
    release, etc.
1.  How to use the package or library. Examples include sample code, copyable
    `bazel run` or `bazel test` commands, etc.
1.  Links to relevant documentation.
