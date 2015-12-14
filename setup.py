from setuptools import setup


setup(name='cpplint',
      version='0.0.6',
      py_modules=['cpplint'],
      # generate platform specific start script
      entry_points={
        'console_scripts': [
            'cpplint = cpplint:main'
        ]
      },
      install_requires=[],
      url="http://en.wikipedia.org/wiki/Cpplint",
      download_url="https://github.com/theandrewdavis/cpplint",
      keywords=["lint", "python", "c++"],
      maintainer = 'Andrew Davis',
      maintainer_email = 'see_github@nospam.com',
      classifiers=["Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: C++",
                   "License :: Freely Distributable"],
      description="An automated checker to make sure a C++ file follows Google's C++ style guide",
      long_description="""This is an automated checker to make sure a C++ file follows Google's C++ style
guide (https://google.github.io/styleguide/cppguide.html). As it heavily relies
on regular expressions, cpplint.py won't catch all violations of the style
guide and will very occasionally report a false positive. There is a list of
things we currently don't handle very well at the top of cpplint.py, and we
welcome patches to improve it.

This version includes some fixes and additional features. For the original
Google version, see https://github.com/google/styleguide/.""")
