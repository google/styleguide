#!/usr/bin/env python
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

import contextlib
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import pytest
from parameterized import parameterized
from testfixtures import compare

import cpplint  # noqa: F401

BASE_CMD = sys.executable + " " + os.path.abspath("./cpplint.py ")


def run_shell_command(cmd: str, args: str, cwd="."):
    """Executes a command

    Args:
        cmd: A string to execute.
        args: A string with arguments to the command.
        cwd: from which folder to run.
    """
    cmd, args = cmd.split(), args.split()
    proc = subprocess.run(cmd + args, cwd=cwd, capture_output=True, check=False)
    out, err = proc.stdout, proc.stderr

    # Make output system-agnostic, aka support Windows
    if os.sep == "\\":
        # TODO: Support scenario with multiple input names
        # We currently only support the last arguments as the input name
        # to prevent accidentally replacing sed tests.
        # Fixing would likely need coding an internal "replace slashes" option for cpplint itself.
        win_path = (os.path.dirname(args[-1]) + "\\").encode()
        good_path = win_path.replace(b"\\", b"/")
        out, err = out.replace(win_path, good_path), err.replace(win_path, good_path)
    if os.linesep == "\r\n":
        out, err = out.replace(b"\r\n", b"\n"), err.replace(b"\r\n", b"\n")

    # print(err) # to get the output at time of test
    return proc.returncode, out, err


class TestUsage:
    def test_help(self):
        (status, out, err) = run_shell_command(BASE_CMD, "--help")
        assert status == 0
        assert out == b""
        assert err.startswith(b"\nSyntax: cpplint")


class TemporaryFolderClassSetup:
    """
    Regression tests: The test starts a filetreewalker scanning for files name *.def
    Such files are expected to have as first line the argument
    to a cpplint invocation from within the same directory, as second line the
    expected status code, then the line count of stdout lines,
    then the stdout lines, and all other lines the expected
    systemerr output (two blank lines at end).
    """

    @pytest.fixture(autouse=True, name="setUpClass()", scope="class")
    @classmethod
    def setUpClass(cls):
        """setup tmp folder for testing with samples and custom additions by subclasses"""
        try:
            cls._root = os.path.realpath(tempfile.mkdtemp())
            shutil.copytree("samples", os.path.join(cls._root, "samples"))
            cls.prepare_directory(cls._root)
        except Exception:
            with contextlib.suppress(Exception):
                cls.tearDownClass()
            raise
        # yield
        # cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        if cls._root:
            # pass
            shutil.rmtree(cls._root)

    @classmethod
    def prepare_directory(cls, root):
        """Override in subclass to manipulate temporary samples root folder before tests"""
        pass

    def get_extra_command_args(self, cwd):
        """Override in subclass to add arguments to command"""
        return ""

    def check_all_in_folder(self, folder_name, expected_defs):
        # uncomment to show complete diff
        # self.maxDiff = None
        count = 0
        for dirpath, _, fnames in os.walk(folder_name):
            for f in fnames:
                if f.endswith(".def"):
                    count += 1
                    self.check_def(os.path.join(dirpath, f))
        assert count == expected_defs

    def check_def(self, path):
        """runs command and compares to expected output from def file"""
        # self.maxDiff = None # to see full diff
        with open(path, "rb") as file_handle:
            data = file_handle.readlines()
            stdout_lines = int(data[2])
            filenames = data[0].decode("utf8").strip()
            args, _, filenames = filenames.rpartition(" ")
            if "*" in filenames:
                rel_cwd = os.path.dirname(path)
                filenames = " ".join(
                    filename[len(rel_cwd) + 1 :]
                    for filename in glob.glob(rel_cwd + "/" + filenames)
                )
            args += " " + filenames
            self._run_and_compare(
                path,
                args,
                int(data[1]),
                [line.decode("utf8").strip() for line in data[3 : 3 + stdout_lines]],
                [line.decode("utf8").strip() for line in data[3 + stdout_lines :]],
            )

    def _run_and_compare(self, definition_file, args, expected_status, expected_out, expected_err):
        rel_cwd = os.path.dirname(definition_file)
        cmd = BASE_CMD + self.get_extra_command_args(rel_cwd)
        cwd = os.path.join(self._root, rel_cwd)
        # command to reproduce, do not forget first two lines have special meaning
        print("\ncd " + cwd + " && " + cmd + " " + args + " 2> <filename>")
        (status, out, err) = run_shell_command(cmd, args, cwd)
        assert expected_status == status, f"bad command status {status}"
        prefix = f"Failed check in {cwd} comparing to {definition_file} for command: {cmd}"
        compare("\n".join(expected_err), err.decode("utf8"), prefix=prefix, show_whitespace=True)
        compare("\n".join(expected_out), out.decode("utf8"), prefix=prefix, show_whitespace=True)


class TestNoRepoSignature(TemporaryFolderClassSetup):
    """runs in a temporary folder (under /tmp in linux) without any .git/.hg/.svn file"""

    def get_extra_command_args(self, cwd):
        return f" --repository {self._root} "

    @parameterized.expand(
        [
            (folder, case[:-4])
            for folder in ["chromium", "vlc", "silly", "boost", "protobuf", "codelite", "v8"]
            for case in os.listdir(f"./samples/{folder}-sample")
            if case.endswith(".def")
        ],
        name_func=lambda fun, _, x: f"test{x.args[0].capitalize()}Sample-{x.args[1]}",
    )
    @pytest.mark.timeout(180)
    def test_samples(self, folder, case):
        self.check_def(os.path.join(f"./samples/{folder}-sample", case + ".def"))


class TestGitRepoSignature(TemporaryFolderClassSetup):
    """runs in a temporary folder with .git file"""

    @classmethod
    def prepare_directory(cls, root):
        with open(os.path.join(root, ".git"), "a"):
            pass

    def test_codelite_sample(self):
        self.check_all_in_folder("./samples/codelite-sample", 1)


class TestMercurialRepoSignature(TemporaryFolderClassSetup):
    """runs in a temporary folder with .hg file"""

    @classmethod
    def prepare_directory(cls, root):
        with open(os.path.join(root, ".hg"), "a"):
            pass

    def test_codelite_sample(self):
        self.check_all_in_folder("./samples/codelite-sample", 1)


class TestSvnRepoSignature(TemporaryFolderClassSetup):
    """runs in a temporary folder with .svn file"""

    @classmethod
    def prepare_directory(cls, root):
        with open(os.path.join(root, ".svn"), "a"):
            pass

    def test_codelite_sample(self):
        self.check_all_in_folder("./samples/codelite-sample", 1)


if __name__ == "__main__":
    pytest.main([__file__])
