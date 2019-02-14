Changelog
---------

1.4.0
-----

* Incorporate cpplint updates from google (62385582b847, 2017-08-16)
  * Fix the `build/endif_comment` check (https://github.com/google/styleguide/pull/169)
  * Teach the explicit constructor check about constexpr (#56)
  * Changed vs7 output format (#57)
  * Remove presubmit check for DISALLOW_* macros (#54)
  * add `--quiet` flag as in upstream (https://github.com/google/styleguide/pull/293)
  * support `--root` argument to run in different folder (https://github.com/google/styleguide/pull/291)
  * Fix 16bit Unicode issue (https://github.com/google/styleguide/issues/337)

1.3.0
-----

* Incorporate cpplint updates from google (6d3a7d8a2, 2016-07-14)
* Add --headers flag to choose which extensions are header files.
* Add regression testsing.

1.2.2
-----

* Fixes bug causing RValue detection with namespaces to fail.

1.2.1
-----

* Fixes error in setup.py.

1.2.0
-----

* Adds `.cu` and `.cuh` as supported file extensions by default.
* Moves the warning "Include the directory when naming .h files" from the `build/include` category to the `build/include_subdir` category.

1.1.0
-----

* Adds quiet option to suppress non error-related output.

1.0.1
-----

* Updates PyPi README.

1.0.0
-----

* Fixes a --repository flag bug.

0.0.9
-----

* Adds the --exclude flag to exclude files from being linted.

0.0.8
-----

* Adds the --repository flag to set the location of the project root for header guard calculations.
* Adds support for ``#pragma once`` as an alternative to header include guards.

0.0.7
-----

* Fixes a Windows include guard bug.
* Adds escaping and more detail to JUnit XML output.

0.0.6
-----

* Adds the --recursive flag.
* Adds JUnit XML output.

0.0.5
-----

* Maintenance release, undoes earlier project folder structure changes to remain as true to upstream as possible.

0.0.4
-----

* Merged with upstream revision r141 (2014-12-04)
* This includes many new checks, see commit messages for details
* This also reverts some renaming of files, to stay close to the original project


0.0.3
-----

* python 3 compatibility

0.0.2
-----

* fixed and extended allowed extensions

0.0.1
-----

* import from googlecode, added setup.py
* imported revision r83 (2012-05-11)
