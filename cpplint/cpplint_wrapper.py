#!/usr/bin/env python
"""Wrapper script for cpplint.

Intended to be invoked from CLion.
Adds new feature --git-diff, so script is invoked for the same list of files as in `arc lint`.
"""
import codecs
import os
import StringIO
import sys
import subprocess
import time

extensions = [".cpp", ".cc", ".c", ".hpp", ".h"]


def main():
    args = ['cpplint.py']
    filenames = []
    for arg in sys.argv[1:]:
        # --git-diff prepares the same file list as `arc lint`
        if arg == "--git-diff":
            commit = subprocess.check_output(["git", "merge-base", "origin/master", "HEAD"]).strip()
            output = subprocess.check_output(["git", "diff", commit, "--name-status"]).decode('utf-8')
            for fname in output.split("\n"):
                tokens = [x.strip() for x in fname.split('\t')]
                if len(tokens) == 0 or tokens[0] == 'D' or tokens[0] == '':
                    continue
                if tokens[0].startswith('R'):
                    fname = tokens[2]
                else:
                    fname = tokens[1]
                for ext in extensions:
                    if fname.endswith(ext):
                        filenames += [os.path.realpath(fname)]
                        break
        else:
            args += [arg]
    args += filenames
    pipes = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output, _) = pipes.communicate()
    for line in output.decode('utf-8').split("\n"):
        if line.startswith("Done processing "):
            continue
        print(line)

if __name__ == '__main__':
    main()
