#! /usr/bin/env python

from setuptools import setup, Command
from subprocess import check_call
from distutils.spawn import find_executable
import cpplint as cpplint

class Cmd(Command):
    '''
    Superclass for other commands to run via setup.py, declared in setup.cfg.
    These commands will auto-install setup_requires in a temporary folder.
    '''
    user_options = [
      ('executable', 'e', 'The executable to use for the command')
    ]

    def initialize_options(self):
        self.executable = find_executable(self.executable)

    def finalize_options(self):
        pass

    def execute(self, *k):
        check_call((self.executable,) + k)


class Lint(Cmd):
    '''run with python setup.py lint'''
    description = 'Run linting of the code'
    user_options = Cmd.user_options + [
      ('jobs', 'j', 'Use multiple processes to speed up the linting')
    ]
    executable = 'pylint'

    def run(self):
        self.execute('cpplint.py')

# some pip versions bark on comments (e.g. on travis)
def read_without_comments(filename):
    with open(filename) as f:
        return [l for l in f.read().splitlines() if not len(l) == 0 and not l.startswith('#')]

test_required = read_without_comments('test-requirements')

setup(name='cpplint',
      version=cpplint.__VERSION__,
      py_modules=['cpplint'],
      # generate platform specific start script
      entry_points={
          'console_scripts': [
              'cpplint = cpplint:main'
          ]
      },
      install_requires=[],
      url='https://github.com/cpplint/cpplint',
      download_url='https://github.com/cpplint/cpplint',
      keywords=['lint', 'python', 'c++'],
      maintainer='cpplint Developers',
      maintainer_email='see_github@nospam.com',
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
      description='Automated checker to ensure C++ files follow Google\'s style guide',
      long_description=open('README.rst').read(),
      license='BSD-3-Clause',
      setup_requires=[
          "pytest-runner"
      ],
      tests_require=test_required,
      # extras_require allow pip install .[dev]
      extras_require={
          'test': test_required,
          'dev': read_without_comments('dev-requirements') + test_required
      },
      cmdclass={
          'lint': Lint
      })
