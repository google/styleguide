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

import os
import sys
import subprocess
import unittest
import shutil
import tempfile

BASE_CMD = sys.executable + ' ' + os.path.abspath('./cpplint.py ')

def RunShellCommand(cmd, cwd='.'):
    """
    executes a command
    :param cmd: A string to execute.
    :param cwd: from which folder to run.
    """

    stdout_target = subprocess.PIPE
    stderr_target = subprocess.PIPE

    proc = subprocess.Popen(cmd,
                            shell=True,
                            cwd=cwd,
                            stdout=stdout_target,
                            stderr=stderr_target)
    out, err = proc.communicate()
    # print(err) # to get the output at time of test
    return (proc.returncode, out, err)


class UsageTest(unittest.TestCase):

    def testHelp(self):
        (status, out, err) = RunShellCommand(BASE_CMD + ' --help')
        self.assertEqual(0, status)
        self.assertEqual(b'', out)
        self.assertTrue(err.startswith(b'\nSyntax: cpplint'))

class TemporaryFolderClassSetup(object):
    """
    Regression tests: The test starts a filetreewalker scanning for files name *.def
    Such files are expected to have as first line the argument
    to a cpplint invocation from within the same directory, as second line the
    expected status code, and all other lines the expected systemerr output (two blank
    lines at end).
    """

    @classmethod
    def setUpClass(cls):
        """setup tmp folder for testing with samples and custom additions by subclasses"""
        try:
            cls._root = tempfile.mkdtemp()
            shutil.copytree('samples', os.path.join(cls._root, 'samples'))
            cls.prepare_directory(cls._root)
        except Exception as e:
            try:
                cls.tearDownClass()
            except Exception as e2:
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
        self.assertEqual(count, expectedDefs)

    def _checkDef(self, path):
        """runs command and compares to expected output from def file"""
        # self.maxDiff = None # to see full diff
        with open(path, 'rb') as filehandle:
            datalines = filehandle.readlines()
            stdoutLines = int(datalines[2])
            self._runAndCheck(os.path.dirname(path),
                             datalines[0].decode('utf8').strip(),
                             int(datalines[1]),
                             [line.decode('utf8').strip() for line in datalines[3:3 + stdoutLines]],
                             [line.decode('utf8').strip() for line in datalines[3 + stdoutLines:]])

    def _runAndCheck(self, rel_cwd, args, expectedStatus, expectedOut, expectedErr):
        cmd = BASE_CMD + self.get_extra_command_args(rel_cwd) + args
        cwd = os.path.join(self._root, rel_cwd)
        # command to reproduce, do not forget first two lines have special meaning
        print("\ncd " + cwd + " && " + cmd + " 2> <filename>")
        (status, out, err) = RunShellCommand(cmd, cwd)
        try:
            self.assertEqual(expectedStatus, status, 'bad command status %s' % status)
            self.assertEqual(expectedErr, err.decode('utf8').split('\n'))
            self.assertEqual(expectedOut, out.decode('utf8').split('\n'))
        except AssertionError as e:
            e.args += ('Failed check in %s for command: %s' % (cwd, cmd),)
            raise e


class NoRepoSignatureTests(TemporaryFolderClassSetup, unittest.TestCase):
    """runs in a temporary folder (under /tmp in linux) without any .git/.hg/.svn file"""

    def get_extra_command_args(self, cwd):
        return (' --repository %s ' % self._root)

    def testChromiumSample(self):
        self.checkAllInFolder('./samples/chromium-sample', 1)

    def testVlcSample(self):
        self.checkAllInFolder('./samples/vlc-sample', 1)

    def testSillySample(self):
        self.checkAllInFolder('./samples/silly-sample', 2)

    def testBoostSample(self):
        self.checkAllInFolder('./samples/boost-sample', 3)

    def testProtobufSample(self):
        self.checkAllInFolder('./samples/protobuf-sample', 1)

    def testCodeliteSample(self):
        self.checkAllInFolder('./samples/codelite-sample', 1)


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
