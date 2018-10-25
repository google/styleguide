#! /usr/bin/env python

from setuptools import setup, Command
from setuptools.command.test import test as TestCommand
from subprocess import check_call
from multiprocessing import cpu_count
from distutils.spawn import find_executable


class Test(TestCommand):
    def run_tests(self):
        check_call(('./cpplint_unittest.py'))
        check_call(('./cpplint_clitest.py'))


class Cmd(Command):
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
    description = 'Run linting of the code'
    user_options = Cmd.user_options + [
      ('jobs', 'j', 'Use multiple processes to speed up the linting')
    ]
    executable = 'pylint'

    def initialize_options(self):
        self.jobs = cpu_count()

    def finalize_options(self):
        self.jobs = int(self.jobs)
        if self.jobs < 1:
            raise ValueError('Jobs must be one or larger')

    def run(self):
        self.execute('-j', str(self.jobs), 'cpplint.py')


class Format(Cmd):
    description = 'Formats the code'
    executable = 'yapf'

    def run(self):
        self.execute('--parallel', '--in-place', 'cpplint.py')


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
      description='An automated checker to make sure a C++ file follows Google\'s C++ style guide',
      long_description=open('README.rst').read(),
      extras_require={
        'dev': [
            'pylint',
            'flake8',
            'yapf',
        ]
      },
      cmdclass={
        'test': Test,
        'lint': Lint,
        'format': Format
      })
