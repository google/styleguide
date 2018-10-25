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
import subprocess
import unittest

BASE_CMD = 'python ' + os.path.abspath('./cpplint.py')

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
    return (proc.returncode, out, err)


class UsageTest(unittest.TestCase):

    def testHelp(self):
        (status, out, err) = RunShellCommand(BASE_CMD + ' --help')
        self.assertEqual(0, status)
        self.assertEqual(b'', out)
        self.assertTrue(err.startswith(b'\nSyntax: cpplint'))


class SignatureTests(unittest.TestCase):
    """
    Regression tests: The test starts a filetreewalker scanning for files name *.def
    Such files are expected to have as first line the argument
    to a cpplint invocation from within the same directory, as second line the
    expected status code, and all other lines the expected systemerr output (two blank
    lines at end).
    """

    def testChromiumSample(self):
        self.checkAllInFolder('./samples/chromium-sample', 1)

    def testVlcSample(self):
        self.checkAllInFolder('./samples/vlc-sample', 1)

    def testSillySample(self):
        self.checkAllInFolder('./samples/silly-sample', 2)

    def testBoostSample(self):
        self.checkAllInFolder('./samples/boost-sample', 2)

    def testProtobufSample(self):
        self.checkAllInFolder('./samples/protobuf-sample', 1)

    def testCodeliteSample(self):
        self.checkAllInFolder('./samples/codelite-sample', 1)

    def checkAllInFolder(self, foldername, expectedDefs):
        # uncomment to show complete diff
        # self.maxDiff = None
        count = 0
        for dirpath, _, fnames in os.walk(foldername):
            for f in fnames:
                if f.endswith('.def'):
                    count += 1
                    self.checkDef(os.path.join(dirpath, f))
        self.assertEqual(count, expectedDefs)

    def checkDef(self, path):
        with open(path, 'rb') as filehandle:
            datalines = filehandle.readlines()
            self.runAndCheck(os.path.dirname(path),
                             datalines[0].decode('utf8').strip(),
                             int(datalines[1]),
                             b'',
                             [line.decode('utf8').strip() for line in datalines[2:]])

    def runAndCheck(self, cwd, args, expectedStatus, expectedOut, expectedErr):
        cmd = BASE_CMD + ' ' + args
        # command to reproduce, do not forget first two lines have special meaning
        print("cd " + cwd + ";" + cmd + " 2> <filename>")
        (status, out, err) = RunShellCommand(cmd, cwd)
        try:
            self.assertEqual(expectedStatus, status)
            self.assertEqual(expectedErr, err.decode('utf8').split('\n'))
            self.assertEqual(expectedOut, out)
        except AssertionError as e:
            print('Failed check in ' + cwd)
            print('for command: ' + cmd)
            raise e


if __name__ == '__main__':
  unittest.main()
