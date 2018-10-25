from setuptools import setup


setup(name='cpplint',
      version='1.3.0',
      py_modules=['cpplint'],
      # generate platform specific start script
      entry_points={
        'console_scripts': [
            'cpplint = cpplint:main'
        ]
      },
      install_requires=[],
      url='http://en.wikipedia.org/wiki/Cpplint',
      download_url='https://github.com/cpplint/cpplint',
      keywords=['lint', 'python', 'c++'],
      maintainer = 'cpplint Developers',
      maintainer_email = 'see_github@nospam.com',
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: C++',
                   'Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Topic :: Software Development :: Quality Assurance',
                   'License :: Freely Distributable'],
      description='An automated checker to make sure a C++ file follows Google\'s C++ style guide',
      long_description=open('README.rst').read())
