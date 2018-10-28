cpplint - static code checker for C++
=====================================

.. image:: https://travis-ci.org/cpplint/cpplint.svg?branch=master
    :target: https://travis-ci.org/cpplint/cpplint

.. image:: https://img.shields.io/pypi/v/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/pyversions/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/status/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/l/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/dd/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/dw/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/dm/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

Cpplint is a command-line tool to check C/C++ files for style issues following `Google's C++ style guide <http://google.github.io/styleguide/cppguide.html>`_.
Cpplint is developed and maintained by Google Inc. at `google/styleguide <https://github.com/google/styleguide>`_

While Google maintains cpplint, Google is not (very) responsive to issues and pull requests, this fork aims to be (somewhat) more open to add fixes to cpplint to enable fixes, when those fixes make cpplint usable in wider contexts.

Goals
-----

* Provides cpplint as a PyPI package for multiple python versions
* Add a few features and fixes aimed at usages outside Google

Non-Goals
---------

* Become an independent fork adding major features
* Fix python style issues in cpplint

Installation
============


To install cpplint from PyPI, run:

.. code-block:: bash

    $ pip install cpplint

Then run it with:

.. code-block:: bash

    $ cpplint [OPTIONS] files

For full usage instructions, run:

.. code-block:: bash

    $ cpplint --help

Changes
-------

The modifications in this branch are minor fixes and cosmetic changes:

* more default extensions
* python 3 compatibility
* customizable file extensions with the --extensions and --headers arguments
* continuous integration on travis
* support for recursive file discovery via the --recursive argument
* support for excluding files via --exclude
* JUnit XML output format
* Overriding repository root auto-detection via --repository
* Support ``#pragma once`` as an alternative to header include guards
* Add quiet option to suppress non error-related output

Development
-----------

.. code-block:: bash

    pip install --user -e .[dev]
    ./setup.py lint
    ./setup.py style
    ./setup.py test
    ./setup.py ci # all the above

Maintaining
-----------

Checkout here and upstream google:

    git clone git@github.com:cpplint/cpplint.git
    cd cpplint
    git remote add google https://github.com/google/styleguide

Setup fetching of pull requests in .git/config:

    [remote "origin"]
    	url = git@github.com:cpplint/cpplint.git
    	fetch = +refs/heads/*:refs/remotes/origin/*
    # following line should be new, fetches PRs from cpplint
    	fetch = +refs/pull/*/head:refs/remotes/origin/pr/*
    [remote "google"]
    	url = https://github.com/google/styleguide
    	fetch = +refs/heads/*:refs/remotes/google/*
    # following line should be new, fetches PRs from google/styleguides
    	fetch = +refs/pull/*/head:refs/remotes/origin/pr/*


To compare this for with upstream (after git fetch):

    git diff google/gh-pages:cpplint/cpplint.py master:cpplint.py
    

Testing and checking on multiple python versions:

.. code-block:: bash

    tox

To release a new version:

.. code-block:: bash

    vi setup.py # increment the version
    vi changelog.rst # log changes
    git add setup.py changelog.rst
    git commit -m "Releasing 0.0.6"
    git tag 0.0.6
    git push
    git push --tags
    python setup.py sdist register -r pypi
    python setup.py sdist upload -r pypi

To incorporate google's changes:

.. code-block:: bash

    git fetch google gh-pages
    git checkout -b updates FETCH_HEAD
    git rebase master # this will have a lot of conflicts, most of which can be solved with the next command (run repeatedly)
    # solve conflicts with files deleted in our fork (this is idempotent and safe to be called. when cpplint.py has conflicts, it will do nothing)
    git status | grep 'new file:' | awk '{print $3}' | xargs -r git rm --cached ; git status | grep 'deleted by us' | awk '{print $4}' | xargs -r git rm ; git status --untracked-files=no | grep 'nothing to commit' && git rebase --skip

    git push -u origin updates
    # check travis
    git push origin --delete updates

    git rebase updates master
    git branch -D updates
    git push

Acknowledgements
----------------

Thanks to Google Inc. for open-sourcing their in-house tool.
Thanks to maintainers of the fork

* `tkruse <https://github.com/tkruse>`_  
* `mattyclarkson <https://github.com/mattyclarkson>`_
* `theandrewdavis <https://github.com/theandrewdavis>`_
