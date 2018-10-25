cpplint - static code checker for C++
=====================================

.. image:: https://travis-ci.org/cpplint/cpplint.svg?branch=master
    :target: https://travis-ci.org/cpplint/cpplint

This project continues the work of cpplint, a C++ style checker following `Google's C++ style guide <http://google.github.io/styleguide/cppguide.html>`_. It provides cpplint as a PyPI package and adds a few features and fixes. It is maintained as a fork of `google/styleguide <https://github.com/google/styleguide>`_ in hopes that it can be merged in the future.

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
    git rebase master
    git push -u origin updates
    # check travis
    git push origin --delete updates

    git rebase updates master
    git branch -D updates
    git push

Thanks to `tkruse <https://github.com/tkruse>`_ for putting cpplint on PyPI and maintaining the PyPI version for many years!

.. image:: https://travis-ci.org/theandrewdavis/cpplint.svg
    :target: https://travis-ci.org/theandrewdavis/cpplint

.. image:: https://img.shields.io/pypi/v/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint
