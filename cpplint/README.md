# cpplint - static code checker for C++

[![Build Status](https://travis-ci.org/tkruse/cpplint.svg)](https://travis-ci.org/tkruse/cpplint)

This project provides cpplint as a pypi package
(https://pypi.python.org/pypi/cpplint). It follows the code maintained as SVN
repository by google employees at
http://google-styleguide.googlecode.com/svn/trunk/cpplint.


It is possible that this repo lags behind the SVN repo, if you notice this,
feel free to open an issue asking for an update.
The ```svn``` branch should be a 1-to-1 copy of the history in SVN.
The ```pypi`` branch contains all local patches on top of svn.
This branch will be rebased frequently.

To install from pypi:

```
$ pip install cpplint
```

The run by calling
```
$ cpplint [OPTIONS] files
```

For more info, see [Original README](README)

## Customizations

The modifications in this branch are minor fixes and cosmetic changes:

- more default extensions
- python 3k compatibility
- minor fixes around default file extensions
- continuous integration on travis

## Maintaining

The strategy here is to have 3 branches: master, svn and pypi.
In the svn branch, only commits from the original svn repo are added.
The Pypi contains patches to upstream, that are intended to be rebased often.
The master branch will be update to the latest pypi state (Either by tedious
manual merging or by hard resets).

Prerequisites: Install git-svn.
To fetch the latest changes from SVN upstream after cloning:

```
# once after cloning
git svn init http://google-styleguide.googlecode.com/svn/trunk/cpplint/
# this creates a remote git-svn and get all new commits
git svn fetch
# update svn branch
git checkout master
git branch -D svn
git checkout git-svn -b svn
# this build will fail in travis, ignore that
git push origin -f svn
# rebase local patches
git checkout pypi
git rebase svn
# run tests, fix if fail
python cpplint_unittest.py
# when all good, push pypi to let travis have a go with all python versions
git push origin -f pypi
# check travis is happy (github badge on pypi branch)
git checkout master
# evil hard push, maintainer must be careful, or do a tedious merge instead
git reset --hard pypi
git push origin -f master
```

Then:
- Wait and see if travis likes the changes
- if necessary fix errors, like python3 compatibility (see earlier commit on common fixes)
- Version Bump in setup.py, update changelog
- Create new release in pypi:
 - ensure ~/.pypirc is valid
 - run:
```
python setup.py sdist register -r pypi
python setup.py sdist bdist upload -r pypi
 ```
