from setuptools import setup


setup(name='cpplint',
      version='1.1.0',
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
      long_description=open('README.rst').read())
