Contributing guide
==================

Thanks for your interest in contributing to cpplint.

Any kinds of contributions are welcome: Bug reports, Documentation, Patches.

However cpplint is a bit special as a project because it aims to closely follow what Google does in the upstream repository.
That means Google remains the source of all major requirements and functinoality of cpplint, where as this fork adds extensions to cpplint run on more environments and in more companies.
The difference between this cpplint and Google should remain so small that anyone can at a glance see there is no added change that could be regarded as a security vulnerability.

Here are some tips to make best use of your time:

1. Feature suggestions should initially be opened at the `upstream repository <https://github.com/google/styleguide>`_, but feel free to open an issue here to and link to the upstream issue.

2. Consider the goals and non-goals of this project:

Goals:

* Provides cpplint as a PyPI package for multiple python versions
* Add a few features and fixes aimed at usages outside Google

Non-Goals:

* Become an independent fork adding major features
* Fix python style issues in cpplint


Development
-----------

You can setup your local environment for developing patches for cpplint like this:

.. code-block:: bash

    pip install --user -e .[dev]
    ./setup.py lint
    ./setup.py style
    ./setup.py test
    ./setup.py ci # all the above
    ./tox    # all of the above in all python environments

Releasing
---------

To release a new version:

.. code-block:: bash

    vi setup.py # increment the version
    vi changelog.rst # log changes
    git add setup.py changelog.rst
    git commit -m "Releasing 0.0.6"
    git tag 0.0.6
    git push
    git push --tags
    pip install --upgrade setuptools wheels twine
    python3 setup.py sdist bdist_wheel
    twine upload  dist/*


Catching up with Upstream
-------------------------

For maintainers, it is a regular duty to look at what cpplint changes were merged upstream, to include them in this fork.

Checkout here and upstream google:

.. code-block:: bash

    git clone git@github.com:cpplint/cpplint.git
    cd cpplint
    git remote add google https://github.com/google/styleguide

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
    
Setup fetching of pull requests in .git/config:

.. code-block:: bash

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

.. code-block:: bash
                
    git diff google/gh-pages:cpplint/cpplint.py master:cpplint.py
