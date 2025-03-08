#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# Copyright (c) 2009 Google Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Command Line interface integration test for cpplint.py."""

import glob
import os
import sys
import subprocess
import unittest
import shutil
import tempfile
import pytest
from testfixtures import compare

BASE_CMD = sys.executable + ' ' + os.path.abspath('./cpplint.py ')

def RunShellCommand(cmd: str, args: str, cwd='.'):
    """
    executes a command
    :param cmd: A string to execute.
    :param cwd: from which folder to run.
    """

    stdout_target = subprocess.PIPE
    stderr_target = subprocess.PIPE

    proc = subprocess.Popen(cmd + ' ' + args,
                            shell=True,
                            cwd=cwd,
                            stdout=stdout_target,
                            stderr=stderr_target)
    out, err = proc.communicate()

    # Make output system-agnostic, aka support Windows
    if os.sep == '\\':
        # TODO: Support scenario with multiple folder inputs
        win_path = (os.path.dirname(args.split(' ')[-1]) + '\\').encode()
        good_path = win_path.replace(b'\\', b'/')
        out, err = out.replace(win_path, good_path), err.replace(win_path, good_path)
    if os.linesep == '\r\n':
        out, err = out.replace(b'\r\n', b'\n'), err.replace(b'\r\n', b'\n')

    # print(err) # to get the output at time of test
    return (proc.returncode, out, err)


class UsageTest(unittest.TestCase):

    def testHelp(self):
        (status, out, err) = RunShellCommand(BASE_CMD, '--help')
        assert 0 == status
        assert b'' == out
        assert err.startswith(b'\nSyntax: cpplint')

class TemporaryFolderClassSetup(object):
    """
    Regression tests: The test starts a filetreewalker scanning for files name *.def
    Such files are expected to have as first line the argument
    to a cpplint invocation from within the same directory, as second line the
    expected status code, then the line count of stdout lines,
    then the stdout lines, and all other lines the expected
    systemerr output (two blank lines at end).
    """

    @classmethod
    def setUpClass(cls):
        """setup tmp folder for testing with samples and custom additions by subclasses"""
        try:
            cls._root = os.path.realpath(tempfile.mkdtemp())
            shutil.copytree('samples', os.path.join(cls._root, 'samples'))
            cls.prepare_directory(cls._root)
        except Exception:
            try:
                cls.tearDownClass()
            except Exception:
                pass
            raise

    @classmethod
    def tearDownClass(cls):
        if (cls._root):
            # pass
            shutil.rmtree(cls._root)

    @classmethod
    def prepare_directory(cls, root):
        """Override in subclass to manipulate temporary samples root folder before tests"""
        pass

    def get_extra_command_args(self, cwd):
        """Override in subclass to add arguments to command"""
        return ''

    def checkAllInFolder(self, foldername, expectedDefs):
        # uncomment to show complete diff
        # self.maxDiff = None
        count = 0
        for dirpath, _, fnames in os.walk(foldername):
            for f in fnames:
                if f.endswith('.def'):
                    count += 1
                    self._checkDef(os.path.join(dirpath, f))
        assert count == expectedDefs

    def _checkDef(self, path):
        """runs command and compares to expected output from def file"""
        # self.maxDiff = None # to see full diff
        with open(path, 'rb') as filehandle:
            datalines = filehandle.readlines()
            stdoutLines = int(datalines[2])
            filenames = datalines[0].decode('utf8').strip()
            args, _, filenames = filenames.rpartition(" ")
            if '*' in filenames:
                rel_cwd = os.path.dirname(path)
                filenames = ' '.join(
                    filename[len(rel_cwd)+1:]
                    for filename in glob.glob(rel_cwd + '/' + filenames)
                )
            args += ' ' + filenames
            self._runAndCheck(path,
                              args,
                              int(datalines[1]),
                              [line.decode('utf8').strip() for line in datalines[3:3 + stdoutLines]],
                              [line.decode('utf8').strip() for line in datalines[3 + stdoutLines:]])

    def _runAndCheck(
            self,
            definition_file,
            args,
            expected_status,
            expected_out,
            expected_err
    ):
        rel_cwd = os.path.dirname(definition_file)
        cmd = BASE_CMD + self.get_extra_command_args(rel_cwd)
        cwd = os.path.join(self._root, rel_cwd)
        # command to reproduce, do not forget first two lines have special meaning
        print("\ncd " + cwd + " && " + cmd + ' '  + args + " 2> <filename>")
        (status, out, err) = RunShellCommand(cmd, args, cwd)
        assert expected_status == status, 'bad command status %s' % status
        prefix = 'Failed check in %s comparing to %s for command: %s' % (cwd, definition_file, cmd)
        compare('\n'.join(expected_err), err.decode('utf8'), prefix=prefix, show_whitespace=True)
        compare('\n'.join(expected_out), out.decode('utf8'), prefix=prefix, show_whitespace=True)


class NoRepoSignatureTests(TemporaryFolderClassSetup, unittest.TestCase):
    """runs in a temporary folder (under /tmp in linux) without any .git/.hg/.svn file"""

    def get_extra_command_args(self, cwd):
        return (' --repository %s ' % self._root)

    def testChromiumSample(self):
        self.checkAllInFolder('./samples/chromium-sample', 1)

    def testVlcSample(self):
        self.checkAllInFolder('./samples/vlc-sample', 1)

    def testSillySample(self):
        self.checkAllInFolder('./samples/silly-sample', 5)

    def testBoostSample(self):
        self.checkAllInFolder('./samples/boost-sample', 4)

    @pytest.mark.timeout(180)
    def testProtobufSample(self):
        self.checkAllInFolder('./samples/protobuf-sample', 1)

    def testCodeliteSample(self):
        self.checkAllInFolder('./samples/codelite-sample', 1)

    def testV8Sample(self):
        self.checkAllInFolder('./samples/v8-sample', 1)

class GitRepoSignatureTests(TemporaryFolderClassSetup, unittest.TestCase):
    """runs in a temporary folder with .git file"""

    @classmethod
    def prepare_directory(cls, root):
        with open(os.path.join(root, '.git'), 'a'):
            pass

    def testCodeliteSample(self):
        self.checkAllInFolder('./samples/codelite-sample', 1)

class MercurialRepoSignatureTests(TemporaryFolderClassSetup, unittest.TestCase):
    """runs in a temporary folder with .hg file"""

    @classmethod
    def prepare_directory(cls, root):
        with open(os.path.join(root, '.hg'), 'a'):
            pass

    def testCodeliteSample(self):
        self.checkAllInFolder('./samples/codelite-sample', 1)

class SvnRepoSignatureTests(TemporaryFolderClassSetup, unittest.TestCase):
    """runs in a temporary folder with .svn file"""

    @classmethod
    def prepare_directory(cls, root):
        with open(os.path.join(root, '.svn'), 'a'):
            pass

    def testCodeliteSample(self):
        self.checkAllInFolder('./samples/codelite-sample', 1)

if __name__ == '__main__':
    unittest.main()
