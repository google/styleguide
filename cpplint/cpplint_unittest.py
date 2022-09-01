#!/usr/bin/python
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

"""Unit test for cpplint.py."""

# TODO(unknown): Add a good test that tests UpdateIncludeState.

import codecs
import os
import random
import re
import subprocess
import sys
import unittest

import cpplint

try:
  xrange          # Python 2
except NameError:
  xrange = range  # Python 3


# This class works as an error collector and replaces cpplint.Error
# function for the unit tests.  We also verify each category we see
# is in cpplint._ERROR_CATEGORIES, to help keep that list up to date.
class ErrorCollector(object):
  # These are a global list, covering all categories seen ever.
  _ERROR_CATEGORIES = cpplint._ERROR_CATEGORIES
  _SEEN_ERROR_CATEGORIES = {}

  def __init__(self, assert_fn):
    """assert_fn: a function to call when we notice a problem."""
    self._assert_fn = assert_fn
    self._errors = []
    cpplint.ResetNolintSuppressions()

  def __call__(self, unused_filename, linenum,
               category, confidence, message):
    self._assert_fn(category in self._ERROR_CATEGORIES,
                    'Message "%s" has category "%s",'
                    ' which is not in _ERROR_CATEGORIES' % (message, category))
    self._SEEN_ERROR_CATEGORIES[category] = 1
    if cpplint._ShouldPrintError(category, confidence, linenum):
      self._errors.append('%s  [%s] [%d]' % (message, category, confidence))

  def Results(self):
    if len(self._errors) < 2:
      return ''.join(self._errors)  # Most tests expect to have a string.
    else:
      return self._errors  # Let's give a list if there is more than one.

  def ResultList(self):
    return self._errors

  def VerifyAllCategoriesAreSeen(self):
    """Fails if there's a category in _ERROR_CATEGORIES~_SEEN_ERROR_CATEGORIES.

    This should only be called after all tests are run, so
    _SEEN_ERROR_CATEGORIES has had a chance to fully populate.  Since
    this isn't called from within the normal unittest framework, we
    can't use the normal unittest assert macros.  Instead we just exit
    when we see an error.  Good thing this test is always run last!
    """
    for category in self._ERROR_CATEGORIES:
      if category not in self._SEEN_ERROR_CATEGORIES:
        sys.exit('FATAL ERROR: There are no tests for category "%s"' % category)

  def RemoveIfPresent(self, substr):
    for (index, error) in enumerate(self._errors):
      if error.find(substr) != -1:
        self._errors = self._errors[0:index] + self._errors[(index + 1):]
        break


# This class is a lame mock of codecs. We do not verify filename, mode, or
# encoding, but for the current use case it is not needed.
class MockIo(object):

  def __init__(self, mock_file):
    self.mock_file = mock_file

  def open(self,  # pylint: disable-msg=C6409
           unused_filename, unused_mode, unused_encoding, _):
    return self.mock_file


class CpplintTestBase(unittest.TestCase):
  """Provides some useful helper functions for cpplint tests."""

  def setUp(self):
    # Allow subclasses to cheat os.path.abspath called in FileInfo class.
    self.os_path_abspath_orig = os.path.abspath

  def tearDown(self):
    os.path.abspath = self.os_path_abspath_orig

  # Perform lint on single line of input and return the error message.
  def PerformSingleLineLint(self, code):
    error_collector = ErrorCollector(self.assert_)
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments('foo.h', lines, error_collector)
    clean_lines = cpplint.CleansedLines(lines)
    include_state = cpplint._IncludeState()
    function_state = cpplint._FunctionState()
    nesting_state = cpplint.NestingState()
    cpplint.ProcessLine('foo.cc', 'cc', clean_lines, 0,
                        include_state, function_state,
                        nesting_state, error_collector)
    # Single-line lint tests are allowed to fail the 'unlintable function'
    # check.
    error_collector.RemoveIfPresent(
        'Lint failed to find start of function body.')
    return error_collector.Results()

  # Perform lint over multiple lines and return the error message.
  def PerformMultiLineLint(self, code):
    error_collector = ErrorCollector(self.assert_)
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments('foo.h', lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    nesting_state = cpplint.NestingState()
    for i in xrange(lines.NumLines()):
      nesting_state.Update('foo.h', lines, i, error_collector)
      cpplint.CheckStyle('foo.h', lines, i, 'h', nesting_state,
                         error_collector)
      cpplint.CheckForNonStandardConstructs('foo.h', lines, i,
                                            nesting_state, error_collector)
    nesting_state.CheckCompletedBlocks('foo.h', error_collector)
    return error_collector.Results()

  # Similar to PerformMultiLineLint, but calls CheckLanguage instead of
  # CheckForNonStandardConstructs
  def PerformLanguageRulesCheck(self, file_name, code):
    error_collector = ErrorCollector(self.assert_)
    include_state = cpplint._IncludeState()
    nesting_state = cpplint.NestingState()
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments(file_name, lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    ext = file_name[file_name.rfind('.') + 1:]
    for i in xrange(lines.NumLines()):
      cpplint.CheckLanguage(file_name, lines, i, ext, include_state,
                            nesting_state, error_collector)
    return error_collector.Results()

  def PerformFunctionLengthsCheck(self, code):
    """Perform Lint function length check on block of code and return warnings.

    Builds up an array of lines corresponding to the code and strips comments
    using cpplint functions.

    Establishes an error collector and invokes the function length checking
    function following cpplint's pattern.

    Args:
      code: C++ source code expected to generate a warning message.

    Returns:
      The accumulated errors.
    """
    file_name = 'foo.cc'
    error_collector = ErrorCollector(self.assert_)
    function_state = cpplint._FunctionState()
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments(file_name, lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    for i in xrange(lines.NumLines()):
      cpplint.CheckForFunctionLengths(file_name, lines, i,
                                      function_state, error_collector)
    return error_collector.Results()

  def PerformIncludeWhatYouUse(self, code, filename='foo.h', io=codecs):
    # First, build up the include state.
    error_collector = ErrorCollector(self.assert_)
    include_state = cpplint._IncludeState()
    nesting_state = cpplint.NestingState()
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments(filename, lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    for i in xrange(lines.NumLines()):
      cpplint.CheckLanguage(filename, lines, i, '.h', include_state,
                            nesting_state, error_collector)
    # We could clear the error_collector here, but this should
    # also be fine, since our IncludeWhatYouUse unittests do not
    # have language problems.

    # Second, look for missing includes.
    cpplint.CheckForIncludeWhatYouUse(filename, lines, include_state,
                                      error_collector, io)
    return error_collector.Results()

  # Perform lint and compare the error message with "expected_message".
  def TestLint(self, code, expected_message):
    self.assertEquals(expected_message, self.PerformSingleLineLint(code))

  def TestMultiLineLint(self, code, expected_message):
    self.assertEquals(expected_message, self.PerformMultiLineLint(code))

  def TestMultiLineLintRE(self, code, expected_message_re):
    message = self.PerformMultiLineLint(code)
    if not re.search(expected_message_re, message):
      self.fail('Message was:\n' + message + 'Expected match to "' +
                expected_message_re + '"')

  def TestLanguageRulesCheck(self, file_name, code, expected_message):
    self.assertEquals(expected_message,
                      self.PerformLanguageRulesCheck(file_name, code))

  def TestIncludeWhatYouUse(self, code, expected_message):
    self.assertEquals(expected_message,
                      self.PerformIncludeWhatYouUse(code))

  def TestBlankLinesCheck(self, lines, start_errors, end_errors):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc', lines, error_collector)
    self.assertEquals(
        start_errors,
        error_collector.Results().count(
            'Redundant blank line at the start of a code block '
            'should be deleted.  [whitespace/blank_line] [2]'))
    self.assertEquals(
        end_errors,
        error_collector.Results().count(
            'Redundant blank line at the end of a code block '
            'should be deleted.  [whitespace/blank_line] [3]'))


class CpplintTest(CpplintTestBase):

  def GetNamespaceResults(self, lines):
    error_collector = ErrorCollector(self.assert_)
    cpplint.RemoveMultiLineComments('foo.h', lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    nesting_state = cpplint.NestingState()
    for i in xrange(lines.NumLines()):
      nesting_state.Update('foo.h', lines, i, error_collector)
      cpplint.CheckForNamespaceIndentation('foo.h', nesting_state,
                                           lines, i, error_collector)

    return error_collector.Results()

  def testForwardDeclarationNameSpaceIndentation(self):
    lines = ['namespace Test {',
             '  class ForwardDeclaration;',
             '}  // namespace Test']

    results = self.GetNamespaceResults(lines)
    self.assertEquals(results, 'Do not indent within a namespace '
                      ' [runtime/indentation_namespace] [4]')

  def testNameSpaceIndentationForClass(self):
    lines = ['namespace Test {',
             'void foo() { }',
             '  class Test {',
             '  };',
             '}  // namespace Test']

    results = self.GetNamespaceResults(lines)
    self.assertEquals(results, 'Do not indent within a namespace '
                      ' [runtime/indentation_namespace] [4]')

  def testNameSpaceIndentationNoError(self):
    lines = ['namespace Test {',
             'void foo() { }',
             '}  // namespace Test']

    results = self.GetNamespaceResults(lines)
    self.assertEquals(results, '')

  def testWhitespaceBeforeNamespace(self):
    lines = ['  namespace Test {',
             '  void foo() { }',
             '  }  // namespace Test']

    results = self.GetNamespaceResults(lines)
    self.assertEquals(results, '')

  def testFalsePositivesNoError(self):
    lines = ['namespace Test {',
             'struct OuterClass {',
             '  struct NoFalsePositivesHere;',
             '  struct NoFalsePositivesHere member_variable;',
             '};',
             '}  // namespace Test']

    results = self.GetNamespaceResults(lines)
    self.assertEquals(results, '')


  # Test get line width.
  def testGetLineWidth(self):
    self.assertEquals(0, cpplint.GetLineWidth(''))
    self.assertEquals(10, cpplint.GetLineWidth(u'x' * 10))
    self.assertEquals(16, cpplint.GetLineWidth(u'都|道|府|県|支庁'))
    self.assertEquals(5 + 13 + 9, cpplint.GetLineWidth(
        u'd𝐱/dt' + u'f : t ⨯ 𝐱 → ℝ' + u't ⨯ 𝐱 → ℝ'))

  def testGetTextInside(self):
    self.assertEquals('', cpplint._GetTextInside('fun()', r'fun\('))
    self.assertEquals('x, y', cpplint._GetTextInside('f(x, y)', r'f\('))
    self.assertEquals('a(), b(c())', cpplint._GetTextInside(
        'printf(a(), b(c()))', r'printf\('))
    self.assertEquals('x, y{}', cpplint._GetTextInside('f[x, y{}]', r'f\['))
    self.assertEquals(None, cpplint._GetTextInside('f[a, b(}]', r'f\['))
    self.assertEquals(None, cpplint._GetTextInside('f[x, y]', r'f\('))
    self.assertEquals('y, h(z, (a + b))', cpplint._GetTextInside(
        'f(x, g(y, h(z, (a + b))))', r'g\('))
    self.assertEquals('f(f(x))', cpplint._GetTextInside('f(f(f(x)))', r'f\('))
    # Supports multiple lines.
    self.assertEquals('\n  return loop(x);\n',
                      cpplint._GetTextInside(
                          'int loop(int x) {\n  return loop(x);\n}\n', r'\{'))
    # '^' matches the beginning of each line.
    self.assertEquals('x, y',
                      cpplint._GetTextInside(
                          '#include "inl.h"  // skip #define\n'
                          '#define A2(x, y) a_inl_(x, y, __LINE__)\n'
                          '#define A(x) a_inl_(x, "", __LINE__)\n',
                          r'^\s*#define\s*\w+\('))

  def testFindNextMultiLineCommentStart(self):
    self.assertEquals(1, cpplint.FindNextMultiLineCommentStart([''], 0))

    lines = ['a', 'b', '/* c']
    self.assertEquals(2, cpplint.FindNextMultiLineCommentStart(lines, 0))

    lines = ['char a[] = "/*";']  # not recognized as comment.
    self.assertEquals(1, cpplint.FindNextMultiLineCommentStart(lines, 0))

  def testFindNextMultiLineCommentEnd(self):
    self.assertEquals(1, cpplint.FindNextMultiLineCommentEnd([''], 0))
    lines = ['a', 'b', ' c */']
    self.assertEquals(2, cpplint.FindNextMultiLineCommentEnd(lines, 0))

  def testRemoveMultiLineCommentsFromRange(self):
    lines = ['a', '  /* comment ', ' * still comment', ' comment */   ', 'b']
    cpplint.RemoveMultiLineCommentsFromRange(lines, 1, 4)
    self.assertEquals(['a', '/**/', '/**/', '/**/', 'b'], lines)

  def testSpacesAtEndOfLine(self):
    self.TestLint(
        '// Hello there ',
        'Line ends in whitespace.  Consider deleting these extra spaces.'
        '  [whitespace/end_of_line] [4]')

  # Test line length check.
  def testLineLengthCheck(self):
    self.TestLint(
        '// Hello',
        '')
    self.TestLint(
        '// x' + ' x' * 40,
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')
    self.TestLint(
        '// x' + ' x' * 50,
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')
    self.TestLint(
        '// //some/path/to/f' + ('i' * 100) + 'le',
        '')
    self.TestLint(
        '//   //some/path/to/f' + ('i' * 100) + 'le',
        '')
    self.TestLint(
        '//   //some/path/to/f' + ('i' * 50) + 'le and some comments',
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')
    self.TestLint(
        '// http://g' + ('o' * 100) + 'gle.com/',
        '')
    self.TestLint(
        '//   https://g' + ('o' * 100) + 'gle.com/',
        '')
    self.TestLint(
        '//   https://g' + ('o' * 60) + 'gle.com/ and some comments',
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')
    self.TestLint(
        '// Read https://g' + ('o' * 60) + 'gle.com/',
        '')
    self.TestLint(
        '// $Id: g' + ('o' * 80) + 'gle.cc#1 $',
        '')
    self.TestLint(
        '// $Id: g' + ('o' * 80) + 'gle.cc#1',
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')
    self.TestMultiLineLint(
        'static const char kCStr[] = "g' + ('o' * 50) + 'gle";\n',
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')
    self.TestMultiLineLint(
        'static const char kRawStr[] = R"(g' + ('o' * 50) + 'gle)";\n',
        '')  # no warning because raw string content is elided
    self.TestMultiLineLint(
        'static const char kMultiLineRawStr[] = R"(\n'
        'g' + ('o' * 80) + 'gle\n'
        ')";',
        '')
    self.TestMultiLineLint(
        'static const char kL' + ('o' * 50) + 'ngIdentifier[] = R"()";\n',
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')

  # Test error suppression annotations.
  def testErrorSuppression(self):
    # Two errors on same line:
    self.TestLint(
        'long a = (int64) 65;',
        ['Using C-style cast.  Use static_cast<int64>(...) instead'
         '  [readability/casting] [4]',
         'Use int16/int64/etc, rather than the C type long'
         '  [runtime/int] [4]',
        ])
    # One category of error suppressed:
    self.TestLint(
        'long a = (int64) 65;  // NOLINT(runtime/int)',
        'Using C-style cast.  Use static_cast<int64>(...) instead'
        '  [readability/casting] [4]')
    # All categories suppressed: (two aliases)
    self.TestLint('long a = (int64) 65;  // NOLINT', '')
    self.TestLint('long a = (int64) 65;  // NOLINT(*)', '')
    # Malformed NOLINT directive:
    self.TestLint(
        'long a = 65;  // NOLINT(foo)',
        ['Unknown NOLINT error category: foo'
         '  [readability/nolint] [5]',
         'Use int16/int64/etc, rather than the C type long  [runtime/int] [4]',
        ])
    # Irrelevant NOLINT directive has no effect:
    self.TestLint(
        'long a = 65;  // NOLINT(readability/casting)',
        'Use int16/int64/etc, rather than the C type long'
        '  [runtime/int] [4]')
    # NOLINTNEXTLINE silences warning for the next line instead of current line
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('test.cc', 'cc',
                            ['// Copyright 2014 Your Company.',
                             '// NOLINTNEXTLINE(whitespace/line_length)',
                             '//  ./command' + (' -verbose' * 80),
                             ''],
                            error_collector)
    self.assertEquals('', error_collector.Results())
    # LINT_C_FILE silences cast warnings for entire file.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('test.h', 'h',
                            ['// Copyright 2014 Your Company.',
                             '// NOLINT(build/header_guard)',
                             'int64 a = (uint64) 65;',
                             '//  LINT_C_FILE',
                             ''],
                            error_collector)
    self.assertEquals('', error_collector.Results())
    # Vim modes silence cast warnings for entire file.
    for modeline in ['vi:filetype=c',
                     'vi:sw=8 filetype=c',
                     'vi:sw=8 filetype=c ts=8',
                     'vi: filetype=c',
                     'vi: sw=8 filetype=c',
                     'vi: sw=8 filetype=c ts=8',
                     'vim:filetype=c',
                     'vim:sw=8 filetype=c',
                     'vim:sw=8 filetype=c ts=8',
                     'vim: filetype=c',
                     'vim: sw=8 filetype=c',
                     'vim: sw=8 filetype=c ts=8',
                     'vim: set filetype=c:',
                     'vim: set sw=8 filetype=c:',
                     'vim: set sw=8 filetype=c ts=8:',
                     'vim: set filetype=c :',
                     'vim: set sw=8 filetype=c :',
                     'vim: set sw=8 filetype=c ts=8 :',
                     'vim: se filetype=c:',
                     'vim: se sw=8 filetype=c:',
                     'vim: se sw=8 filetype=c ts=8:',
                     'vim: se filetype=c :',
                     'vim: se sw=8 filetype=c :',
                     'vim: se sw=8 filetype=c ts=8 :']:
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData('test.h', 'h',
                              ['// Copyright 2014 Your Company.',
                               '// NOLINT(build/header_guard)',
                               'int64 a = (uint64) 65;',
                               '/* Prevent warnings about the modeline',
                               modeline,
                               '*/',
                               ''],
                              error_collector)
      self.assertEquals('', error_collector.Results())
    # LINT_KERNEL_FILE silences whitespace/tab warnings for entire file.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('test.h', 'h',
                            ['// Copyright 2014 Your Company.',
                             '// NOLINT(build/header_guard)',
                             'struct test {',
                             '\tint member;',
                             '};',
                             '//  LINT_KERNEL_FILE',
                             ''],
                            error_collector)
    self.assertEquals('', error_collector.Results())
    # NOLINT, NOLINTNEXTLINE silences the readability/braces warning for "};".
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('test.cc', 'cc',
                            ['// Copyright 2014 Your Company.',
                             'for (int i = 0; i != 100; ++i) {',
                             '\tstd::cout << i << std::endl;',
                             '};  // NOLINT',
                             'for (int i = 0; i != 100; ++i) {',
                             '\tstd::cout << i << std::endl;',
                             '// NOLINTNEXTLINE',
                             '};',
                             '//  LINT_KERNEL_FILE',
                             ''],
                            error_collector)
    self.assertEquals('', error_collector.Results())

  # Test Variable Declarations.
  def testVariableDeclarations(self):
    self.TestLint(
        'long a = 65;',
        'Use int16/int64/etc, rather than the C type long'
        '  [runtime/int] [4]')
    self.TestLint(
        'long double b = 65.0;',
        '')
    self.TestLint(
        'long long aa = 6565;',
        'Use int16/int64/etc, rather than the C type long'
        '  [runtime/int] [4]')

  # Test C-style cast cases.
  def testCStyleCast(self):
    self.TestLint(
        'int a = (int)1.0;',
        'Using C-style cast.  Use static_cast<int>(...) instead'
        '  [readability/casting] [4]')
    self.TestLint(
        'int a = (int)-1.0;',
        'Using C-style cast.  Use static_cast<int>(...) instead'
        '  [readability/casting] [4]')
    self.TestLint(
        'int *a = (int *)NULL;',
        'Using C-style cast.  Use reinterpret_cast<int *>(...) instead'
        '  [readability/casting] [4]')

    self.TestLint(
        'uint16 a = (uint16)1.0;',
        'Using C-style cast.  Use static_cast<uint16>(...) instead'
        '  [readability/casting] [4]')
    self.TestLint(
        'int32 a = (int32)1.0;',
        'Using C-style cast.  Use static_cast<int32>(...) instead'
        '  [readability/casting] [4]')
    self.TestLint(
        'uint64 a = (uint64)1.0;',
        'Using C-style cast.  Use static_cast<uint64>(...) instead'
        '  [readability/casting] [4]')

    # These shouldn't be recognized casts.
    self.TestLint('u a = (u)NULL;', '')
    self.TestLint('uint a = (uint)NULL;', '')
    self.TestLint('typedef MockCallback<int(int)> CallbackType;', '')
    self.TestLint('scoped_ptr< MockCallback<int(int)> > callback_value;', '')
    self.TestLint('std::function<int(bool)>', '')
    self.TestLint('x = sizeof(int)', '')
    self.TestLint('x = alignof(int)', '')
    self.TestLint('alignas(int) char x[42]', '')
    self.TestLint('alignas(alignof(x)) char y[42]', '')
    self.TestLint('void F(int (func)(int));', '')
    self.TestLint('void F(int (func)(int*));', '')
    self.TestLint('void F(int (Class::member)(int));', '')
    self.TestLint('void F(int (Class::member)(int*));', '')
    self.TestLint('void F(int (Class::member)(int), int param);', '')
    self.TestLint('void F(int (Class::member)(int*), int param);', '')

    # These should not be recognized (lambda functions without arg names).
    self.TestLint('[](int/*unused*/) -> bool {', '')
    self.TestLint('[](int /*unused*/) -> bool {', '')
    self.TestLint('auto f = [](MyStruct* /*unused*/)->int {', '')
    self.TestLint('[](int) -> bool {', '')
    self.TestLint('auto f = [](MyStruct*)->int {', '')

    # Cast with brace initializers
    self.TestLint('int64_t{4096} * 1000 * 1000', '')
    self.TestLint('size_t{4096} * 1000 * 1000', '')
    self.TestLint('uint_fast16_t{4096} * 1000 * 1000', '')

    # Brace initializer with templated type
    self.TestMultiLineLint(
        """
        template <typename Type1,
                  typename Type2>
        void Function(int arg1,
                      int arg2) {
          variable &= ~Type1{0} - 1;
        }""",
        '')
    self.TestMultiLineLint(
        """
        template <typename Type>
        class Class {
          void Function() {
            variable &= ~Type{0} - 1;
          }
        };""",
        '')
    self.TestMultiLineLint(
        """
        template <typename Type>
        class Class {
          void Function() {
            variable &= ~Type{0} - 1;
          }
        };""",
        '')
    self.TestMultiLineLint(
        """
        namespace {
        template <typename Type>
        class Class {
          void Function() {
            if (block) {
              variable &= ~Type{0} - 1;
            }
          }
        };
        }""",
        '')

  # Test taking address of casts (runtime/casting)
  def testRuntimeCasting(self):
    error_msg = ('Are you taking an address of a cast?  '
                 'This is dangerous: could be a temp var.  '
                 'Take the address before doing the cast, rather than after'
                 '  [runtime/casting] [4]')
    self.TestLint('int* x = &static_cast<int*>(foo);', error_msg)
    self.TestLint('int* x = &reinterpret_cast<int *>(foo);', error_msg)
    self.TestLint('int* x = &(int*)foo;',
                  ['Using C-style cast.  Use reinterpret_cast<int*>(...) '
                   'instead  [readability/casting] [4]',
                   error_msg])
    self.TestLint('BudgetBuckets&(BudgetWinHistory::*BucketFn)(void) const;',
                  '')
    self.TestLint('&(*func_ptr)(arg)', '')
    self.TestLint('Compute(arg, &(*func_ptr)(i, j));', '')

    # Alternative error message
    alt_error_msg = ('Are you taking an address of something dereferenced '
                     'from a cast?  Wrapping the dereferenced expression in '
                     'parentheses will make the binding more obvious'
                     '  [readability/casting] [4]')
    self.TestLint('int* x = &down_cast<Obj*>(obj)->member_;', alt_error_msg)
    self.TestLint('int* x = &down_cast<Obj*>(obj)[index];', alt_error_msg)
    self.TestLint('int* x = &(down_cast<Obj*>(obj)->member_);', '')
    self.TestLint('int* x = &(down_cast<Obj*>(obj)[index]);', '')
    self.TestLint('int* x = &down_cast<Obj*>(obj)\n->member_;', alt_error_msg)
    self.TestLint('int* x = &(down_cast<Obj*>(obj)\n->member_);', '')

    # It's OK to cast an address.
    self.TestLint('int* x = reinterpret_cast<int *>(&foo);', '')

    # Function pointers returning references should not be confused
    # with taking address of old-style casts.
    self.TestLint('auto x = implicit_cast<string &(*)(int)>(&foo);', '')

  def testRuntimeSelfinit(self):
    self.TestLint(
        'Foo::Foo(Bar r, Bel l) : r_(r_), l_(l_) { }',
        'You seem to be initializing a member variable with itself.'
        '  [runtime/init] [4]')
    self.TestLint(
        'Foo::Foo(Bar r, Bel l) : r_(CHECK_NOTNULL(r_)) { }',
        'You seem to be initializing a member variable with itself.'
        '  [runtime/init] [4]')
    self.TestLint(
        'Foo::Foo(Bar r, Bel l) : r_(r), l_(l) { }',
        '')
    self.TestLint(
        'Foo::Foo(Bar r) : r_(r), l_(r_), ll_(l_) { }',
        '')

  # Test for unnamed arguments in a method.
  def testCheckForUnnamedParams(self):
    self.TestLint('virtual void Func(int*) const;', '')
    self.TestLint('virtual void Func(int*);', '')
    self.TestLint('void Method(char*) {', '')
    self.TestLint('void Method(char*);', '')
    self.TestLint('static void operator delete[](void*) throw();', '')
    self.TestLint('int Method(int);', '')

    self.TestLint('virtual void Func(int* p);', '')
    self.TestLint('void operator delete(void* x) throw();', '')
    self.TestLint('void Method(char* x) {', '')
    self.TestLint('void Method(char* /*x*/) {', '')
    self.TestLint('void Method(char* x);', '')
    self.TestLint('typedef void (*Method)(int32 x);', '')
    self.TestLint('static void operator delete[](void* x) throw();', '')
    self.TestLint('static void operator delete[](void* /*x*/) throw();', '')

    self.TestLint('X operator++(int);', '')
    self.TestLint('X operator++(int) {', '')
    self.TestLint('X operator--(int);', '')
    self.TestLint('X operator--(int /*unused*/) {', '')
    self.TestLint('MACRO(int);', '')
    self.TestLint('MACRO(func(int));', '')
    self.TestLint('MACRO(arg, func(int));', '')

    self.TestLint('void (*func)(void*);', '')
    self.TestLint('void Func((*func)(void*)) {}', '')
    self.TestLint('template <void Func(void*)> void func();', '')
    self.TestLint('virtual void f(int /*unused*/) {', '')
    self.TestLint('void f(int /*unused*/) override {', '')
    self.TestLint('void f(int /*unused*/) final {', '')

  # Test deprecated casts such as int(d)
  def testDeprecatedCast(self):
    self.TestLint(
        'int a = int(2.2);',
        'Using deprecated casting style.  '
        'Use static_cast<int>(...) instead'
        '  [readability/casting] [4]')

    self.TestLint(
        '(char *) "foo"',
        'Using C-style cast.  '
        'Use const_cast<char *>(...) instead'
        '  [readability/casting] [4]')

    self.TestLint(
        '(int*)foo',
        'Using C-style cast.  '
        'Use reinterpret_cast<int*>(...) instead'
        '  [readability/casting] [4]')

    # Checks for false positives...
    self.TestLint('int a = int();', '')  # constructor
    self.TestLint('X::X() : a(int()) {}', '')  # default constructor
    self.TestLint('operator bool();', '')  # Conversion operator
    self.TestLint('new int64(123);', '')  # "new" operator on basic type
    self.TestLint('new   int64(123);', '')  # "new" operator on basic type
    self.TestLint('new const int(42);', '')  # "new" on const-qualified type
    self.TestLint('using a = bool(int arg);', '')  # C++11 alias-declaration
    self.TestLint('x = bit_cast<double(*)[3]>(y);', '')  # array of array
    self.TestLint('void F(const char(&src)[N]);', '')  # array of references

    # Placement new
    self.TestLint(
        'new(field_ptr) int(field->default_value_enum()->number());',
        '')

    # C++11 function wrappers
    self.TestLint('std::function<int(bool)>', '')
    self.TestLint('std::function<const int(bool)>', '')
    self.TestLint('std::function< int(bool) >', '')
    self.TestLint('mfunction<int(bool)>', '')

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'test.cc', 'cc',
        ['// Copyright 2014 Your Company. All Rights Reserved.',
         'typedef std::function<',
         '    bool(int)> F;',
         ''],
        error_collector)
    self.assertEquals('', error_collector.Results())

    # Return types for function pointers
    self.TestLint('typedef bool(FunctionPointer)();', '')
    self.TestLint('typedef bool(FunctionPointer)(int param);', '')
    self.TestLint('typedef bool(MyClass::*MemberFunctionPointer)();', '')
    self.TestLint('typedef bool(MyClass::* MemberFunctionPointer)();', '')
    self.TestLint('typedef bool(MyClass::*MemberFunctionPointer)() const;', '')
    self.TestLint('void Function(bool(FunctionPointerArg)());', '')
    self.TestLint('void Function(bool(FunctionPointerArg)()) {}', '')
    self.TestLint('typedef set<int64, bool(*)(int64, int64)> SortedIdSet', '')
    self.TestLint(
        'bool TraverseNode(T *Node, bool(VisitorBase:: *traverse) (T *t)) {}',
        '')

  # The second parameter to a gMock method definition is a function signature
  # that often looks like a bad cast but should not picked up by lint.
  def testMockMethod(self):
    self.TestLint(
        'MOCK_METHOD0(method, int());',
        '')
    self.TestLint(
        'MOCK_CONST_METHOD1(method, float(string));',
        '')
    self.TestLint(
        'MOCK_CONST_METHOD2_T(method, double(float, float));',
        '')
    self.TestLint(
        'MOCK_CONST_METHOD1(method, SomeType(int));',
        '')

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('mock.cc', 'cc',
                            ['MOCK_METHOD1(method1,',
                             '             bool(int));',
                             'MOCK_METHOD1(',
                             '    method2,',
                             '    bool(int));',
                             'MOCK_CONST_METHOD2(',
                             '    method3, bool(int,',
                             '                  int));',
                             'MOCK_METHOD1(method4, int(bool));',
                             'const int kConstant = int(42);'],  # true positive
                            error_collector)
    self.assertEquals(
        0,
        error_collector.Results().count(
            ('Using deprecated casting style.  '
             'Use static_cast<bool>(...) instead  '
             '[readability/casting] [4]')))
    self.assertEquals(
        1,
        error_collector.Results().count(
            ('Using deprecated casting style.  '
             'Use static_cast<int>(...) instead  '
             '[readability/casting] [4]')))

  # Like gMock method definitions, MockCallback instantiations look very similar
  # to bad casts.
  def testMockCallback(self):
    self.TestLint(
        'MockCallback<bool(int)>',
        '')
    self.TestLint(
        'MockCallback<int(float, char)>',
        '')

  # Test false errors that happened with some include file names
  def testIncludeFilenameFalseError(self):
    self.TestLint(
        '#include "foo/long-foo.h"',
        '')
    self.TestLint(
        '#include "foo/sprintf.h"',
        '')

  # Test typedef cases.  There was a bug that cpplint misidentified
  # typedef for pointer to function as C-style cast and produced
  # false-positive error messages.
  def testTypedefForPointerToFunction(self):
    self.TestLint(
        'typedef void (*Func)(int x);',
        '')
    self.TestLint(
        'typedef void (*Func)(int *x);',
        '')
    self.TestLint(
        'typedef void Func(int x);',
        '')
    self.TestLint(
        'typedef void Func(int *x);',
        '')

  def testIncludeWhatYouUseNoImplementationFiles(self):
    code = 'std::vector<int> foo;'
    self.assertEquals('Add #include <vector> for vector<>'
                      '  [build/include_what_you_use] [4]',
                      self.PerformIncludeWhatYouUse(code, 'foo.h'))
    self.assertEquals('',
                      self.PerformIncludeWhatYouUse(code, 'foo.cc'))

  def testIncludeWhatYouUse(self):
    self.TestIncludeWhatYouUse(
        """#include <vector>
           std::vector<int> foo;
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include <map>
           std::pair<int,int> foo;
        """,
        'Add #include <utility> for pair<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <multimap>
           std::pair<int,int> foo;
        """,
        'Add #include <utility> for pair<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <hash_map>
           std::pair<int,int> foo;
        """,
        'Add #include <utility> for pair<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <hash_map>
           auto foo = std::make_pair(1, 2);
        """,
        'Add #include <utility> for make_pair'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <utility>
           std::pair<int,int> foo;
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include <vector>
           DECLARE_string(foobar);
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include <vector>
           DEFINE_string(foobar, "", "");
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include <vector>
           std::pair<int,int> foo;
        """,
        'Add #include <utility> for pair<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include "base/foobar.h"
           std::vector<int> foo;
        """,
        'Add #include <vector> for vector<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <vector>
           std::set<int> foo;
        """,
        'Add #include <set> for set<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include "base/foobar.h"
          hash_map<int, int> foobar;
        """,
        'Add #include <hash_map> for hash_map<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include "base/containers/hash_tables.h"
          base::hash_map<int, int> foobar;
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include "base/foobar.h"
           bool foobar = std::less<int>(0,1);
        """,
        'Add #include <functional> for less<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include "base/foobar.h"
           bool foobar = min<int>(0,1);
        """,
        'Add #include <algorithm> for min  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        'void a(const string &foobar);',
        'Add #include <string> for string  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        'void a(const std::string &foobar);',
        'Add #include <string> for string  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        'void a(const my::string &foobar);',
        '')  # Avoid false positives on strings in other namespaces.
    self.TestIncludeWhatYouUse(
        """#include "base/foobar.h"
           bool foobar = swap(0,1);
        """,
        'Add #include <utility> for swap  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include "base/foobar.h"
           bool foobar = transform(a.begin(), a.end(), b.start(), Foo);
        """,
        'Add #include <algorithm> for transform  '
        '[build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include "base/foobar.h"
           bool foobar = min_element(a.begin(), a.end());
        """,
        'Add #include <algorithm> for min_element  '
        '[build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """foo->swap(0,1);
           foo.swap(0,1);
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include <string>
           void a(const std::multimap<int,string> &foobar);
        """,
        'Add #include <map> for multimap<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <string>
           void a(const std::unordered_map<int,string> &foobar);
        """,
        'Add #include <unordered_map> for unordered_map<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <string>
           void a(const std::unordered_set<int> &foobar);
        """,
        'Add #include <unordered_set> for unordered_set<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <queue>
           void a(const std::priority_queue<int> &foobar);
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include <assert.h>
           #include <string>
           #include <vector>
           #include "base/basictypes.h"
           #include "base/port.h"
           vector<string> hajoa;""", '')
    self.TestIncludeWhatYouUse(
        """#include <string>
           int i = numeric_limits<int>::max()
        """,
        'Add #include <limits> for numeric_limits<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <limits>
           int i = numeric_limits<int>::max()
        """,
        '')
    self.TestIncludeWhatYouUse(
        """#include <string>
           std::unique_ptr<int> x;
        """,
        'Add #include <memory> for unique_ptr<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <string>
           auto x = std::make_unique<int>(0);
        """,
        'Add #include <memory> for make_unique<>'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <vector>
           vector<int> foo(vector<int> x) { return std::move(x); }
        """,
        'Add #include <utility> for move'
        '  [build/include_what_you_use] [4]')
    self.TestIncludeWhatYouUse(
        """#include <string>
           int a, b;
           std::swap(a, b);
        """,
        'Add #include <utility> for swap'
        '  [build/include_what_you_use] [4]')

    # Test the UpdateIncludeState code path.
    mock_header_contents = ['#include "blah/foo.h"', '#include "blah/bar.h"']
    message = self.PerformIncludeWhatYouUse(
        '#include "blah/a.h"',
        filename='blah/a.cc',
        io=MockIo(mock_header_contents))
    self.assertEquals(message, '')

    mock_header_contents = ['#include <set>']
    message = self.PerformIncludeWhatYouUse(
        """#include "blah/a.h"
           std::set<int> foo;""",
        filename='blah/a.cc',
        io=MockIo(mock_header_contents))
    self.assertEquals(message, '')

    # Make sure we can find the correct header file if the cc file seems to be
    # a temporary file generated by Emacs's flymake.
    mock_header_contents = ['']
    message = self.PerformIncludeWhatYouUse(
        """#include "blah/a.h"
           std::set<int> foo;""",
        filename='blah/a_flymake.cc',
        io=MockIo(mock_header_contents))
    self.assertEquals(message, 'Add #include <set> for set<>  '
                      '[build/include_what_you_use] [4]')

    # If there's just a cc and the header can't be found then it's ok.
    message = self.PerformIncludeWhatYouUse(
        """#include "blah/a.h"
           std::set<int> foo;""",
        filename='blah/a.cc')
    self.assertEquals(message, '')

    # Make sure we find the headers with relative paths.
    mock_header_contents = ['']
    message = self.PerformIncludeWhatYouUse(
        """#include "%s/a.h"
           std::set<int> foo;""" % os.path.basename(os.getcwd()),
        filename='a.cc',
        io=MockIo(mock_header_contents))
    self.assertEquals(message, 'Add #include <set> for set<>  '
                      '[build/include_what_you_use] [4]')

  def testFilesBelongToSameModule(self):
    f = cpplint.FilesBelongToSameModule
    self.assertEquals((True, ''), f('a.cc', 'a.h'))
    self.assertEquals((True, ''), f('base/google.cc', 'base/google.h'))
    self.assertEquals((True, ''), f('base/google_test.cc', 'base/google.h'))
    self.assertEquals((True, ''),
                      f('base/google_unittest.cc', 'base/google.h'))
    self.assertEquals((True, ''),
                      f('base/internal/google_unittest.cc',
                        'base/public/google.h'))
    self.assertEquals((True, 'xxx/yyy/'),
                      f('xxx/yyy/base/internal/google_unittest.cc',
                        'base/public/google.h'))
    self.assertEquals((True, 'xxx/yyy/'),
                      f('xxx/yyy/base/google_unittest.cc',
                        'base/public/google.h'))
    self.assertEquals((True, ''),
                      f('base/google_unittest.cc', 'base/google-inl.h'))
    self.assertEquals((True, '/home/build/google3/'),
                      f('/home/build/google3/base/google.cc', 'base/google.h'))

    self.assertEquals((False, ''),
                      f('/home/build/google3/base/google.cc', 'basu/google.h'))
    self.assertEquals((False, ''), f('a.cc', 'b.h'))

  def testCleanseLine(self):
    self.assertEquals('int foo = 0;',
                      cpplint.CleanseComments('int foo = 0;  // danger!'))
    self.assertEquals('int o = 0;',
                      cpplint.CleanseComments('int /* foo */ o = 0;'))
    self.assertEquals('foo(int a, int b);',
                      cpplint.CleanseComments('foo(int a /* abc */, int b);'))
    self.assertEqual('f(a, b);',
                     cpplint.CleanseComments('f(a, /* name */ b);'))
    self.assertEqual('f(a, b);',
                     cpplint.CleanseComments('f(a /* name */, b);'))
    self.assertEqual('f(a, b);',
                     cpplint.CleanseComments('f(a, /* name */b);'))
    self.assertEqual('f(a, b, c);',
                     cpplint.CleanseComments('f(a, /**/b, /**/c);'))
    self.assertEqual('f(a, b, c);',
                     cpplint.CleanseComments('f(a, /**/b/**/, c);'))

  def testRawStrings(self):
    self.TestMultiLineLint(
        """
        void Func() {
          static const char kString[] = R"(
            #endif  <- invalid preprocessor should be ignored
            */      <- invalid comment should be ignored too
          )";
        }""",
        '')
    self.TestMultiLineLint(
        """
        void Func() {
          string s = R"TrueDelimiter(
              )"
              )FalseDelimiter"
              )TrueDelimiter";
        }""",
        '')
    self.TestMultiLineLint(
        """
        void Func() {
          char char kString[] = R"(  ";" )";
        }""",
        '')
    self.TestMultiLineLint(
        """
        static const char kRawString[] = R"(
          \tstatic const int kLineWithTab = 1;
          static const int kLineWithTrailingWhiteSpace = 1;\x20

           void WeirdNumberOfSpacesAtLineStart() {
            string x;
            x += StrCat("Use StrAppend instead");
          }

          void BlankLineAtEndOfBlock() {
            // TODO incorrectly formatted
            //Badly formatted comment

          }

        )";""",
        '')
    self.TestMultiLineLint(
        """
        void Func() {
          string s = StrCat(R"TrueDelimiter(
              )"
              )FalseDelimiter"
              )TrueDelimiter", R"TrueDelimiter2(
              )"
              )FalseDelimiter2"
              )TrueDelimiter2");
        }""",
        '')
    self.TestMultiLineLint(
        """
        static SomeStruct kData = {
            {0, R"(line1
                   line2
                   )"}
            };""",
        '')

  def testMultiLineComments(self):
    # missing explicit is bad
    self.TestMultiLineLint(
        r"""int a = 0;
            /* multi-liner
            class Foo {
            Foo(int f);  // should cause a lint warning in code
            }
            */ """,
        '')
    self.TestMultiLineLint(
        r"""/* int a = 0; multi-liner
              static const int b = 0;""",
        'Could not find end of multi-line comment'
        '  [readability/multiline_comment] [5]')
    self.TestMultiLineLint(r"""  /* multi-line comment""",
                           'Could not find end of multi-line comment'
                           '  [readability/multiline_comment] [5]')
    self.TestMultiLineLint(r"""  // /* comment, but not multi-line""", '')
    self.TestMultiLineLint(r"""/**********
                                 */""", '')
    self.TestMultiLineLint(r"""/**
                                 * Doxygen comment
                                 */""",
                           '')
    self.TestMultiLineLint(r"""/*!
                                 * Doxygen comment
                                 */""",
                           '')

  def testMultilineStrings(self):
    multiline_string_error_message = (
        'Multi-line string ("...") found.  This lint script doesn\'t '
        'do well with such strings, and may give bogus warnings.  '
        'Use C++11 raw strings or concatenation instead.'
        '  [readability/multiline_string] [5]')

    file_path = 'mydir/foo.cc'

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'cc',
                            ['const char* str = "This is a\\',
                             ' multiline string.";'],
                            error_collector)
    self.assertEquals(
        2,  # One per line.
        error_collector.ResultList().count(multiline_string_error_message))

  # Test non-explicit single-argument constructors
  def testExplicitSingleArgumentConstructors(self):
    old_verbose_level = cpplint._cpplint_state.verbose_level
    cpplint._cpplint_state.verbose_level = 0

    try:
      # missing explicit is bad
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # missing explicit is bad, even with whitespace
      self.TestMultiLineLint(
          """
          class Foo {
            Foo (int f);
          };""",
          ['Extra space before ( in function call  [whitespace/parens] [4]',
           'Single-parameter constructors should be marked explicit.'
           '  [runtime/explicit] [5]'])
      # missing explicit, with distracting comment, is still bad
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f);  // simpler than Foo(blargh, blarg)
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # missing explicit, with qualified classname
      self.TestMultiLineLint(
          """
          class Qualifier::AnotherOne::Foo {
            Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # missing explicit for inline constructors is bad as well
      self.TestMultiLineLint(
          """
          class Foo {
            inline Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # missing explicit for constexpr constructors is bad as well
      self.TestMultiLineLint(
          """
          class Foo {
            constexpr Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # missing explicit for constexpr+inline constructors is bad as well
      self.TestMultiLineLint(
          """
          class Foo {
            constexpr inline Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      self.TestMultiLineLint(
          """
          class Foo {
            inline constexpr Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # explicit with inline is accepted
      self.TestMultiLineLint(
          """
          class Foo {
            inline explicit Foo(int f);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            explicit inline Foo(int f);
          };""",
          '')
      # explicit with constexpr is accepted
      self.TestMultiLineLint(
          """
          class Foo {
            constexpr explicit Foo(int f);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            explicit constexpr Foo(int f);
          };""",
          '')
      # explicit with constexpr+inline is accepted
      self.TestMultiLineLint(
          """
          class Foo {
            inline constexpr explicit Foo(int f);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            explicit inline constexpr Foo(int f);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            constexpr inline explicit Foo(int f);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            explicit constexpr inline Foo(int f);
          };""",
          '')
      # structs are caught as well.
      self.TestMultiLineLint(
          """
          struct Foo {
            Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # Templatized classes are caught as well.
      self.TestMultiLineLint(
          """
          template<typename T> class Foo {
            Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # inline case for templatized classes.
      self.TestMultiLineLint(
          """
          template<typename T> class Foo {
            inline Foo(int f);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # constructors with a default argument should still be marked explicit
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f = 0);
          };""",
          'Constructors callable with one argument should be marked explicit.'
          '  [runtime/explicit] [5]')
      # multi-argument constructors with all but one default argument should be
      # marked explicit
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f, int g = 0);
          };""",
          'Constructors callable with one argument should be marked explicit.'
          '  [runtime/explicit] [5]')
      # multi-argument constructors with all default arguments should be marked
      # explicit
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f = 0, int g = 0);
          };""",
          'Constructors callable with one argument should be marked explicit.'
          '  [runtime/explicit] [5]')
      # explicit no-argument constructors are bad
      self.TestMultiLineLint(
          """
          class Foo {
            explicit Foo();
          };""",
          'Zero-parameter constructors should not be marked explicit.'
          '  [runtime/explicit] [5]')
      # void constructors are considered no-argument
      self.TestMultiLineLint(
          """
          class Foo {
            explicit Foo(void);
          };""",
          'Zero-parameter constructors should not be marked explicit.'
          '  [runtime/explicit] [5]')
      # No warning for multi-parameter constructors
      self.TestMultiLineLint(
          """
          class Foo {
            explicit Foo(int f, int g);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            explicit Foo(int f, int g = 0);
          };""",
          '')
      # single-argument constructors that take a function that takes multiple
      # arguments should be explicit
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(void (*f)(int f, int g));
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # single-argument constructors that take a single template argument with
      # multiple parameters should be explicit
      self.TestMultiLineLint(
          """
          template <typename T, typename S>
          class Foo {
            Foo(Bar<T, S> b);
          };""",
          'Single-parameter constructors should be marked explicit.'
          '  [runtime/explicit] [5]')
      # but copy constructors that take multiple template parameters are OK
      self.TestMultiLineLint(
          """
          template <typename T, S>
          class Foo {
            Foo(Foo<T, S>& f);
          };""",
          '')
      # proper style is okay
      self.TestMultiLineLint(
          """
          class Foo {
            explicit Foo(int f);
          };""",
          '')
      # two argument constructor is okay
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f, int b);
          };""",
          '')
      # two argument constructor, across two lines, is okay
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f,
                int b);
          };""",
          '')
      # non-constructor (but similar name), is okay
      self.TestMultiLineLint(
          """
          class Foo {
            aFoo(int f);
          };""",
          '')
      # constructor with void argument is okay
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(void);
          };""",
          '')
      # single argument method is okay
      self.TestMultiLineLint(
          """
          class Foo {
            Bar(int b);
          };""",
          '')
      # comments should be ignored
      self.TestMultiLineLint(
          """
          class Foo {
          // Foo(int f);
          };""",
          '')
      # single argument function following class definition is okay
      # (okay, it's not actually valid, but we don't want a false positive)
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(int f, int b);
          };
          Foo(int f);""",
          '')
      # single argument function is okay
      self.TestMultiLineLint(
          """static Foo(int f);""",
          '')
      # single argument copy constructor is okay.
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(const Foo&);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(Foo const&);
          };""",
          '')
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(Foo&);
          };""",
          '')
      # templatized copy constructor is okay.
      self.TestMultiLineLint(
          """
          template<typename T> class Foo {
            Foo(const Foo<T>&);
          };""",
          '')
      # Special case for std::initializer_list
      self.TestMultiLineLint(
          """
          class Foo {
            Foo(std::initializer_list<T> &arg) {}
          };""",
          '')
      # Anything goes inside an assembly block
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData('foo.cc', 'cc',
                              ['void Func() {',
                               '  __asm__ (',
                               '    "hlt"',
                               '  );',
                               '  asm {',
                               '    movdqa [edx + 32], xmm2',
                               '  }',
                               '}'],
                              error_collector)
      self.assertEquals(
          0,
          error_collector.ResultList().count(
              'Extra space before ( in function call  [whitespace/parens] [4]'))
      self.assertEquals(
          0,
          error_collector.ResultList().count(
              'Closing ) should be moved to the previous line  '
              '[whitespace/parens] [2]'))
      self.assertEquals(
          0,
          error_collector.ResultList().count(
              'Extra space before [  [whitespace/braces] [5]'))
    finally:
      cpplint._cpplint_state.verbose_level = old_verbose_level

  def testSlashStarCommentOnSingleLine(self):
    self.TestMultiLineLint(
        """/* static */ Foo(int f);""",
        '')
    self.TestMultiLineLint(
        """/*/ static */  Foo(int f);""",
        '')
    self.TestMultiLineLint(
        """/*/ static Foo(int f);""",
        'Could not find end of multi-line comment'
        '  [readability/multiline_comment] [5]')
    self.TestMultiLineLint(
        """  /*/ static Foo(int f);""",
        'Could not find end of multi-line comment'
        '  [readability/multiline_comment] [5]')
    self.TestMultiLineLint(
        """  /**/ static Foo(int f);""",
        '')

  # Test suspicious usage of "if" like this:
  # if (a == b) {
  #   DoSomething();
  # } if (a == c) {   // Should be "else if".
  #   DoSomething();  // This gets called twice if a == b && a == c.
  # }
  def testSuspiciousUsageOfIf(self):
    self.TestLint(
        '  if (a == b) {',
        '')
    self.TestLint(
        '  } if (a == b) {',
        'Did you mean "else if"? If not, start a new line for "if".'
        '  [readability/braces] [4]')

  # Test suspicious usage of memset. Specifically, a 0
  # as the final argument is almost certainly an error.
  def testSuspiciousUsageOfMemset(self):
    # Normal use is okay.
    self.TestLint(
        '  memset(buf, 0, sizeof(buf))',
        '')

    # A 0 as the final argument is almost certainly an error.
    self.TestLint(
        '  memset(buf, sizeof(buf), 0)',
        'Did you mean "memset(buf, 0, sizeof(buf))"?'
        '  [runtime/memset] [4]')
    self.TestLint(
        '  memset(buf, xsize * ysize, 0)',
        'Did you mean "memset(buf, 0, xsize * ysize)"?'
        '  [runtime/memset] [4]')

    # There is legitimate test code that uses this form.
    # This is okay since the second argument is a literal.
    self.TestLint(
        "  memset(buf, 'y', 0)",
        '')
    self.TestLint(
        '  memset(buf, 4, 0)',
        '')
    self.TestLint(
        '  memset(buf, -1, 0)',
        '')
    self.TestLint(
        '  memset(buf, 0xF1, 0)',
        '')
    self.TestLint(
        '  memset(buf, 0xcd, 0)',
        '')

  def testRedundantVirtual(self):
    self.TestLint('virtual void F()', '')
    self.TestLint('virtual void F();', '')
    self.TestLint('virtual void F() {}', '')

    message_template = ('"%s" is redundant since function is already '
                        'declared as "%s"  [readability/inheritance] [4]')
    for virt_specifier in ['override', 'final']:
      error_message = message_template % ('virtual', virt_specifier)
      self.TestLint('virtual int F() %s' % virt_specifier, error_message)
      self.TestLint('virtual int F() %s;' % virt_specifier, error_message)
      self.TestLint('virtual int F() %s {' % virt_specifier, error_message)

      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData(
          'foo.cc', 'cc',
          ['// Copyright 2014 Your Company.',
           'virtual void F(int a,',
           '               int b) ' + virt_specifier + ';',
           'virtual void F(int a,',
           '               int b) LOCKS_EXCLUDED(lock) ' + virt_specifier + ';',
           'virtual void F(int a,',
           '               int b)',
           '    LOCKS_EXCLUDED(lock) ' + virt_specifier + ';',
           ''],
          error_collector)
      self.assertEquals(
          [error_message, error_message, error_message],
          error_collector.Results())

    error_message = message_template % ('override', 'final')
    self.TestLint('int F() override final', error_message)
    self.TestLint('int F() override final;', error_message)
    self.TestLint('int F() override final {}', error_message)
    self.TestLint('int F() final override', error_message)
    self.TestLint('int F() final override;', error_message)
    self.TestLint('int F() final override {}', error_message)

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'foo.cc', 'cc',
        ['// Copyright 2014 Your Company.',
         'struct A : virtual B {',
         '  ~A() override;'
         '};',
         'class C',
         '    : public D,',
         '      public virtual E {',
         '  void Func() override;',
         '}',
         ''],
        error_collector)
    self.assertEquals('', error_collector.Results())

    self.TestLint('void Finalize(AnnotationProto *final) override;', '')

  def testCheckDeprecated(self):
    self.TestLanguageRulesCheck('foo_test.cc', '#include <iostream>', '')
    self.TestLanguageRulesCheck('foo_unittest.cc', '#include <iostream>', '')

  def testCheckPosixThreading(self):
    self.TestLint('var = sctime_r()', '')
    self.TestLint('var = strtok_r()', '')
    self.TestLint('var = strtok_r(foo, ba, r)', '')
    self.TestLint('var = brand()', '')
    self.TestLint('_rand()', '')
    self.TestLint('.rand()', '')
    self.TestLint('->rand()', '')
    self.TestLint('ACMRandom rand(seed)', '')
    self.TestLint('ISAACRandom rand()', '')
    self.TestLint('var = rand()',
                  'Consider using rand_r(...) instead of rand(...)'
                  ' for improved thread safety.'
                  '  [runtime/threadsafe_fn] [2]')
    self.TestLint('var = strtok(str, delim)',
                  'Consider using strtok_r(...) '
                  'instead of strtok(...)'
                  ' for improved thread safety.'
                  '  [runtime/threadsafe_fn] [2]')

  def testVlogMisuse(self):
    self.TestLint('VLOG(1)', '')
    self.TestLint('VLOG(99)', '')
    self.TestLint('LOG(ERROR)', '')
    self.TestLint('LOG(INFO)', '')
    self.TestLint('LOG(WARNING)', '')
    self.TestLint('LOG(FATAL)', '')
    self.TestLint('LOG(DFATAL)', '')
    self.TestLint('VLOG(SOMETHINGWEIRD)', '')
    self.TestLint('MYOWNVLOG(ERROR)', '')
    errmsg = ('VLOG() should be used with numeric verbosity level.  '
              'Use LOG() if you want symbolic severity levels.'
              '  [runtime/vlog] [5]')
    self.TestLint('VLOG(ERROR)', errmsg)
    self.TestLint('VLOG(INFO)', errmsg)
    self.TestLint('VLOG(WARNING)', errmsg)
    self.TestLint('VLOG(FATAL)', errmsg)
    self.TestLint('VLOG(DFATAL)', errmsg)
    self.TestLint('  VLOG(ERROR)', errmsg)
    self.TestLint('  VLOG(INFO)', errmsg)
    self.TestLint('  VLOG(WARNING)', errmsg)
    self.TestLint('  VLOG(FATAL)', errmsg)
    self.TestLint('  VLOG(DFATAL)', errmsg)


  # Test potential format string bugs like printf(foo).
  def testFormatStrings(self):
    self.TestLint('printf("foo")', '')
    self.TestLint('printf("foo: %s", foo)', '')
    self.TestLint('DocidForPrintf(docid)', '')  # Should not trigger.
    self.TestLint('printf(format, value)', '')  # Should not trigger.
    self.TestLint('printf(__VA_ARGS__)', '')  # Should not trigger.
    self.TestLint('printf(format.c_str(), value)', '')  # Should not trigger.
    self.TestLint('printf(format(index).c_str(), value)', '')
    self.TestLint(
        'printf(foo)',
        'Potential format string bug. Do printf("%s", foo) instead.'
        '  [runtime/printf] [4]')
    self.TestLint(
        'printf(foo.c_str())',
        'Potential format string bug. '
        'Do printf("%s", foo.c_str()) instead.'
        '  [runtime/printf] [4]')
    self.TestLint(
        'printf(foo->c_str())',
        'Potential format string bug. '
        'Do printf("%s", foo->c_str()) instead.'
        '  [runtime/printf] [4]')
    self.TestLint(
        'StringPrintf(foo)',
        'Potential format string bug. Do StringPrintf("%s", foo) instead.'
        ''
        '  [runtime/printf] [4]')

  # Test disallowed use of operator& and other operators.
  def testIllegalOperatorOverloading(self):
    errmsg = ('Unary operator& is dangerous.  Do not use it.'
              '  [runtime/operator] [4]')
    self.TestLint('void operator=(const Myclass&)', '')
    self.TestLint('void operator&(int a, int b)', '')   # binary operator& ok
    self.TestLint('void operator&() { }', errmsg)
    self.TestLint('void operator & (  ) { }',
                  ['Extra space after (  [whitespace/parens] [2]', errmsg])

  # const string reference members are dangerous..
  def testConstStringReferenceMembers(self):
    errmsg = ('const string& members are dangerous. It is much better to use '
              'alternatives, such as pointers or simple constants.'
              '  [runtime/member_string_references] [2]')

    members_declarations = ['const string& church',
                            'const string &turing',
                            'const string & godel']
    # TODO(unknown): Enable also these tests if and when we ever
    # decide to check for arbitrary member references.
    #                         "const Turing & a",
    #                         "const Church& a",
    #                         "const vector<int>& a",
    #                         "const     Kurt::Godel    &    godel",
    #                         "const Kazimierz::Kuratowski& kk" ]

    # The Good.

    self.TestLint('void f(const string&)', '')
    self.TestLint('const string& f(const string& a, const string& b)', '')
    self.TestLint('typedef const string& A;', '')

    for decl in members_declarations:
      self.TestLint(decl + ' = b;', '')
      self.TestLint(decl + '      =', '')

    # The Bad.

    for decl in members_declarations:
      self.TestLint(decl + ';', errmsg)

  # Variable-length arrays are not permitted.
  def testVariableLengthArrayDetection(self):
    errmsg = ('Do not use variable-length arrays.  Use an appropriately named '
              "('k' followed by CamelCase) compile-time constant for the size."
              '  [runtime/arrays] [1]')

    self.TestLint('int a[any_old_variable];', errmsg)
    self.TestLint('int doublesize[some_var * 2];', errmsg)
    self.TestLint('int a[afunction()];', errmsg)
    self.TestLint('int a[function(kMaxFooBars)];', errmsg)
    self.TestLint('bool a_list[items_->size()];', errmsg)
    self.TestLint('namespace::Type buffer[len+1];', errmsg)

    self.TestLint('int a[64];', '')
    self.TestLint('int a[0xFF];', '')
    self.TestLint('int first[256], second[256];', '')
    self.TestLint('int array_name[kCompileTimeConstant];', '')
    self.TestLint('char buf[somenamespace::kBufSize];', '')
    self.TestLint('int array_name[ALL_CAPS];', '')
    self.TestLint('AClass array1[foo::bar::ALL_CAPS];', '')
    self.TestLint('int a[kMaxStrLen + 1];', '')
    self.TestLint('int a[sizeof(foo)];', '')
    self.TestLint('int a[sizeof(*foo)];', '')
    self.TestLint('int a[sizeof foo];', '')
    self.TestLint('int a[sizeof(struct Foo)];', '')
    self.TestLint('int a[128 - sizeof(const bar)];', '')
    self.TestLint('int a[(sizeof(foo) * 4)];', '')
    self.TestLint('int a[(arraysize(fixed_size_array)/2) << 1];', '')
    self.TestLint('delete a[some_var];', '')
    self.TestLint('return a[some_var];', '')

  # DISALLOW_COPY_AND_ASSIGN and DISALLOW_IMPLICIT_CONSTRUCTORS should be at
  # end of class if present.
  def testDisallowMacrosAtEnd(self):
    for macro_name in (
        'DISALLOW_COPY_AND_ASSIGN',
        'DISALLOW_IMPLICIT_CONSTRUCTORS'):
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData(
          'foo.cc', 'cc',
          ['// Copyright 2014 Your Company.',
           'class SomeClass {',
           ' private:',
           '  %s(SomeClass);' % macro_name,
           '  int member_;',
           '};',
           ''],
          error_collector)
      self.assertEquals(
          ('%s should be the last thing in the class' % macro_name) +
          '  [readability/constructors] [3]',
          error_collector.Results())

      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData(
          'foo.cc', 'cc',
          ['// Copyright 2014 Your Company.',
           'class OuterClass {',
           ' private:',
           '  struct InnerClass {',
           '   private:',
           '    %s(InnerClass);' % macro_name,
           '    int member;',
           '  };',
           '};',
           ''],
          error_collector)
      self.assertEquals(
          ('%s should be the last thing in the class' % macro_name) +
          '  [readability/constructors] [3]',
          error_collector.Results())

      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData(
          'foo.cc', 'cc',
          ['// Copyright 2014 Your Company.',
           'class OuterClass1 {',
           ' private:',
           '  struct InnerClass1 {',
           '   private:',
           '    %s(InnerClass1);' % macro_name,
           '  };',
           '  %s(OuterClass1);' % macro_name,
           '};',
           'struct OuterClass2 {',
           ' private:',
           '  class InnerClass2 {',
           '   private:',
           '    %s(InnerClass2);' % macro_name,
           '    // comment',
           '  };',
           '',
           '  %s(OuterClass2);' % macro_name,
           '',
           '  // comment',
           '};',
           'void Func() {',
           '  struct LocalClass {',
           '   private:',
           '    %s(LocalClass);' % macro_name,
           '  } variable;',
           '}',
           ''],
          error_collector)
      self.assertEquals('', error_collector.Results())

  # Brace usage
  def testBraces(self):
    # Braces shouldn't be followed by a ; unless they're defining a struct
    # or initializing an array
    self.TestLint('int a[3] = { 1, 2, 3 };', '')
    self.TestLint(
        """const int foo[] =
               {1, 2, 3 };""",
        '')
    # For single line, unmatched '}' with a ';' is ignored (not enough context)
    self.TestMultiLineLint(
        """int a[3] = { 1,
                        2,
                        3 };""",
        '')
    self.TestMultiLineLint(
        """int a[2][3] = { { 1, 2 },
                         { 3, 4 } };""",
        '')
    self.TestMultiLineLint(
        """int a[2][3] =
               { { 1, 2 },
                 { 3, 4 } };""",
        '')

  # CHECK/EXPECT_TRUE/EXPECT_FALSE replacements
  def testCheckCheck(self):
    self.TestLint('CHECK(x == 42);',
                  'Consider using CHECK_EQ instead of CHECK(a == b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x != 42);',
                  'Consider using CHECK_NE instead of CHECK(a != b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x >= 42);',
                  'Consider using CHECK_GE instead of CHECK(a >= b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x > 42);',
                  'Consider using CHECK_GT instead of CHECK(a > b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x <= 42);',
                  'Consider using CHECK_LE instead of CHECK(a <= b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x < 42);',
                  'Consider using CHECK_LT instead of CHECK(a < b)'
                  '  [readability/check] [2]')

    self.TestLint('DCHECK(x == 42);',
                  'Consider using DCHECK_EQ instead of DCHECK(a == b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x != 42);',
                  'Consider using DCHECK_NE instead of DCHECK(a != b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x >= 42);',
                  'Consider using DCHECK_GE instead of DCHECK(a >= b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x > 42);',
                  'Consider using DCHECK_GT instead of DCHECK(a > b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x <= 42);',
                  'Consider using DCHECK_LE instead of DCHECK(a <= b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x < 42);',
                  'Consider using DCHECK_LT instead of DCHECK(a < b)'
                  '  [readability/check] [2]')

    self.TestLint(
        'EXPECT_TRUE("42" == x);',
        'Consider using EXPECT_EQ instead of EXPECT_TRUE(a == b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE("42" != x);',
        'Consider using EXPECT_NE instead of EXPECT_TRUE(a != b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE(+42 >= x);',
        'Consider using EXPECT_GE instead of EXPECT_TRUE(a >= b)'
        '  [readability/check] [2]')

    self.TestLint(
        'EXPECT_FALSE(x == 42);',
        'Consider using EXPECT_NE instead of EXPECT_FALSE(a == b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_FALSE(x != 42);',
        'Consider using EXPECT_EQ instead of EXPECT_FALSE(a != b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_FALSE(x >= 42);',
        'Consider using EXPECT_LT instead of EXPECT_FALSE(a >= b)'
        '  [readability/check] [2]')
    self.TestLint(
        'ASSERT_FALSE(x > 42);',
        'Consider using ASSERT_LE instead of ASSERT_FALSE(a > b)'
        '  [readability/check] [2]')
    self.TestLint(
        'ASSERT_FALSE(x <= 42);',
        'Consider using ASSERT_GT instead of ASSERT_FALSE(a <= b)'
        '  [readability/check] [2]')

    self.TestLint('CHECK(x<42);',
                  ['Missing spaces around <'
                   '  [whitespace/operators] [3]',
                   'Consider using CHECK_LT instead of CHECK(a < b)'
                   '  [readability/check] [2]'])
    self.TestLint('CHECK(x>42);',
                  ['Missing spaces around >'
                   '  [whitespace/operators] [3]',
                   'Consider using CHECK_GT instead of CHECK(a > b)'
                   '  [readability/check] [2]'])

    self.TestLint('using some::namespace::operator<<;', '')
    self.TestLint('using some::namespace::operator>>;', '')

    self.TestLint('CHECK(x->y == 42);',
                  'Consider using CHECK_EQ instead of CHECK(a == b)'
                  '  [readability/check] [2]')

    self.TestLint(
        '  EXPECT_TRUE(42 < x);  // Random comment.',
        'Consider using EXPECT_LT instead of EXPECT_TRUE(a < b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE( 42 < x );',
        ['Extra space after ( in function call'
         '  [whitespace/parens] [4]',
         'Extra space before )  [whitespace/parens] [2]',
         'Consider using EXPECT_LT instead of EXPECT_TRUE(a < b)'
         '  [readability/check] [2]'])

    self.TestLint('CHECK(4\'2 == x);',
                  'Consider using CHECK_EQ instead of CHECK(a == b)'
                  '  [readability/check] [2]')

  def testCheckCheckFalsePositives(self):
    self.TestLint('CHECK(some_iterator == obj.end());', '')
    self.TestLint('EXPECT_TRUE(some_iterator == obj.end());', '')
    self.TestLint('EXPECT_FALSE(some_iterator == obj.end());', '')
    self.TestLint('CHECK(some_pointer != NULL);', '')
    self.TestLint('EXPECT_TRUE(some_pointer != NULL);', '')
    self.TestLint('EXPECT_FALSE(some_pointer != NULL);', '')

    self.TestLint('CHECK(CreateTestFile(dir, (1 << 20)));', '')
    self.TestLint('CHECK(CreateTestFile(dir, (1 >> 20)));', '')

    self.TestLint('CHECK(x ^ (y < 42));', '')
    self.TestLint('CHECK((x > 42) ^ (x < 54));', '')
    self.TestLint('CHECK(a && b < 42);', '')
    self.TestLint('CHECK(42 < a && a < b);', '')
    self.TestLint('SOFT_CHECK(x > 42);', '')

    self.TestMultiLineLint(
        """_STLP_DEFINE_BINARY_OP_CHECK(==, _OP_EQUAL);
        _STLP_DEFINE_BINARY_OP_CHECK(!=, _OP_NOT_EQUAL);
        _STLP_DEFINE_BINARY_OP_CHECK(<, _OP_LESS_THAN);
        _STLP_DEFINE_BINARY_OP_CHECK(<=, _OP_LESS_EQUAL);
        _STLP_DEFINE_BINARY_OP_CHECK(>, _OP_GREATER_THAN);
        _STLP_DEFINE_BINARY_OP_CHECK(>=, _OP_GREATER_EQUAL);
        _STLP_DEFINE_BINARY_OP_CHECK(+, _OP_PLUS);
        _STLP_DEFINE_BINARY_OP_CHECK(*, _OP_TIMES);
        _STLP_DEFINE_BINARY_OP_CHECK(/, _OP_DIVIDE);
        _STLP_DEFINE_BINARY_OP_CHECK(-, _OP_SUBTRACT);
        _STLP_DEFINE_BINARY_OP_CHECK(%, _OP_MOD);""",
        '')

    self.TestLint('CHECK(x < 42) << "Custom error message";', '')

  # Alternative token to punctuation operator replacements
  def testCheckAltTokens(self):
    self.TestLint('true or true',
                  'Use operator || instead of or'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('true and true',
                  'Use operator && instead of and'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('if (not true)',
                  'Use operator ! instead of not'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('1 bitor 1',
                  'Use operator | instead of bitor'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('1 xor 1',
                  'Use operator ^ instead of xor'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('1 bitand 1',
                  'Use operator & instead of bitand'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('x = compl 1',
                  'Use operator ~ instead of compl'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('x and_eq y',
                  'Use operator &= instead of and_eq'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('x or_eq y',
                  'Use operator |= instead of or_eq'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('x xor_eq y',
                  'Use operator ^= instead of xor_eq'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('x not_eq y',
                  'Use operator != instead of not_eq'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('line_continuation or',
                  'Use operator || instead of or'
                  '  [readability/alt_tokens] [2]')
    self.TestLint('if(true and(parentheses',
                  'Use operator && instead of and'
                  '  [readability/alt_tokens] [2]')

    self.TestLint('#include "base/false-and-false.h"', '')
    self.TestLint('#error false or false', '')
    self.TestLint('false nor false', '')
    self.TestLint('false nand false', '')

  # Passing and returning non-const references
  def testNonConstReference(self):
    # Passing a non-const reference as function parameter is forbidden.
    operand_error_message = ('Is this a non-const reference? '
                             'If so, make const or use a pointer: %s'
                             '  [runtime/references] [2]')
    # Warn of use of a non-const reference in operators and functions
    self.TestLint('bool operator>(Foo& s, Foo& f);',
                  [operand_error_message % 'Foo& s',
                   operand_error_message % 'Foo& f'])
    self.TestLint('bool operator+(Foo& s, Foo& f);',
                  [operand_error_message % 'Foo& s',
                   operand_error_message % 'Foo& f'])
    self.TestLint('int len(Foo& s);', operand_error_message % 'Foo& s')
    # Allow use of non-const references in a few specific cases
    self.TestLint('stream& operator>>(stream& s, Foo& f);', '')
    self.TestLint('stream& operator<<(stream& s, Foo& f);', '')
    self.TestLint('void swap(Bar& a, Bar& b);', '')
    self.TestLint('ostream& LogFunc(ostream& s);', '')
    self.TestLint('ostringstream& LogFunc(ostringstream& s);', '')
    self.TestLint('istream& LogFunc(istream& s);', '')
    self.TestLint('istringstream& LogFunc(istringstream& s);', '')
    # Returning a non-const reference from a function is OK.
    self.TestLint('int& g();', '')
    # Passing a const reference to a struct (using the struct keyword) is OK.
    self.TestLint('void foo(const struct tm& tm);', '')
    # Passing a const reference to a typename is OK.
    self.TestLint('void foo(const typename tm& tm);', '')
    # Const reference to a pointer type is OK.
    self.TestLint('void foo(const Bar* const& p) {', '')
    self.TestLint('void foo(Bar const* const& p) {', '')
    self.TestLint('void foo(Bar* const& p) {', '')
    # Const reference to a templated type is OK.
    self.TestLint('void foo(const std::vector<std::string>& v);', '')
    # Non-const reference to a pointer type is not OK.
    self.TestLint('void foo(Bar*& p);',
                  operand_error_message % 'Bar*& p')
    self.TestLint('void foo(const Bar*& p);',
                  operand_error_message % 'const Bar*& p')
    self.TestLint('void foo(Bar const*& p);',
                  operand_error_message % 'Bar const*& p')
    self.TestLint('void foo(struct Bar*& p);',
                  operand_error_message % 'struct Bar*& p')
    self.TestLint('void foo(const struct Bar*& p);',
                  operand_error_message % 'const struct Bar*& p')
    self.TestLint('void foo(struct Bar const*& p);',
                  operand_error_message % 'struct Bar const*& p')
    # Non-const reference to a templated type is not OK.
    self.TestLint('void foo(std::vector<int>& p);',
                  operand_error_message % 'std::vector<int>& p')
    # Returning an address of something is not prohibited.
    self.TestLint('return &something;', '')
    self.TestLint('if (condition) {return &something; }', '')
    self.TestLint('if (condition) return &something;', '')
    self.TestLint('if (condition) address = &something;', '')
    self.TestLint('if (condition) result = lhs&rhs;', '')
    self.TestLint('if (condition) result = lhs & rhs;', '')
    self.TestLint('a = (b+c) * sizeof &f;', '')
    self.TestLint('a = MySize(b) * sizeof &f;', '')
    # We don't get confused by C++11 range-based for loops.
    self.TestLint('for (const string& s : c)', '')
    self.TestLint('for (auto& r : c)', '')
    self.TestLint('for (typename Type& a : b)', '')
    # We don't get confused by some other uses of '&'.
    self.TestLint('T& operator=(const T& t);', '')
    self.TestLint('int g() { return (a & b); }', '')
    self.TestLint('T& r = (T&)*(vp());', '')
    self.TestLint('T& r = v', '')
    self.TestLint('static_assert((kBits & kMask) == 0, "text");', '')
    self.TestLint('COMPILE_ASSERT((kBits & kMask) == 0, text);', '')
    # Spaces before template arguments.  This is poor style, but
    # happens 0.15% of the time.
    self.TestLint('void Func(const vector <int> &const_x, '
                  'vector <int> &nonconst_x) {',
                  operand_error_message % 'vector<int> &nonconst_x')

    # Derived member functions are spared from override check
    self.TestLint('void Func(X& x);', operand_error_message % 'X& x')
    self.TestLint('void Func(X& x) {}', operand_error_message % 'X& x')
    self.TestLint('void Func(X& x) override;', '')
    self.TestLint('void Func(X& x) override {', '')
    self.TestLint('void Func(X& x) const override;', '')
    self.TestLint('void Func(X& x) const override {', '')

    # Don't warn on out-of-line method definitions.
    self.TestLint('void NS::Func(X& x) {', '')
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'foo.cc', 'cc',
        ['// Copyright 2014 Your Company. All Rights Reserved.',
         'void a::b() {}',
         'void f(int& q) {}',
         ''],
        error_collector)
    self.assertEquals(
        operand_error_message % 'int& q',
        error_collector.Results())

    # Other potential false positives.  These need full parser
    # state to reproduce as opposed to just TestLint.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'foo.cc', 'cc',
        ['// Copyright 2014 Your Company. All Rights Reserved.',
         'void swap(int &x,',
         '          int &y) {',
         '}',
         'void swap(',
         '    sparsegroup<T, GROUP_SIZE, Alloc> &x,',
         '    sparsegroup<T, GROUP_SIZE, Alloc> &y) {',
         '}',
         'ostream& operator<<(',
         '    ostream& out',
         '    const dense_hash_set<Value, Hash, Equals, Alloc>& seq) {',
         '}',
         'class A {',
         '  void Function(',
         '      string &x) override {',
         '  }',
         '};',
         'void Derived::Function(',
         '    string &x) {',
         '}',
         '#define UNSUPPORTED_MASK(_mask) \\',
         '  if (flags & _mask) { \\',
         '    LOG(FATAL) << "Unsupported flag: " << #_mask; \\',
         '  }',
         'Constructor::Constructor()',
         '    : initializer1_(a1 & b1),',
         '      initializer2_(a2 & b2) {',
         '}',
         'Constructor::Constructor()',
         '    : initializer1_{a3 & b3},',
         '      initializer2_(a4 & b4) {',
         '}',
         'Constructor::Constructor()',
         '    : initializer1_{a5 & b5},',
         '      initializer2_(a6 & b6) {}',
         ''],
        error_collector)
    self.assertEquals('', error_collector.Results())

    # Multi-line references
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'foo.cc', 'cc',
        ['// Copyright 2014 Your Company. All Rights Reserved.',
         'void Func(const Outer::',
         '              Inner& const_x,',
         '          const Outer',
         '              ::Inner& const_y,',
         '          const Outer<',
         '              int>::Inner& const_z,',
         '          Outer::',
         '              Inner& nonconst_x,',
         '          Outer',
         '              ::Inner& nonconst_y,',
         '          Outer<',
         '              int>::Inner& nonconst_z) {',
         '}',
         ''],
        error_collector)
    self.assertEquals(
        [operand_error_message % 'Outer::Inner& nonconst_x',
         operand_error_message % 'Outer::Inner& nonconst_y',
         operand_error_message % 'Outer<int>::Inner& nonconst_z'],
        error_collector.Results())

    # A peculiar false positive due to bad template argument parsing
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'foo.cc', 'cc',
        ['// Copyright 2014 Your Company. All Rights Reserved.',
         'inline RCULocked<X>::ReadPtr::ReadPtr(const RCULocked* rcu) {',
         '  DCHECK(!(data & kFlagMask)) << "Error";',
         '}',
         '',
         'RCULocked<X>::WritePtr::WritePtr(RCULocked* rcu)',
         '    : lock_(&rcu_->mutex_) {',
         '}',
         ''],
        error_collector.Results())
    self.assertEquals('', error_collector.Results())

  def testBraceAtBeginOfLine(self):
    self.TestLint('{',
                  '{ should almost always be at the end of the previous line'
                  '  [whitespace/braces] [4]')

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['int function()',
                             '{',  # warning here
                             '  MutexLock l(&mu);',
                             '}',
                             'int variable;'
                             '{',  # no warning
                             '  MutexLock l(&mu);',
                             '}',
                             'MyType m = {',
                             '  {value1, value2},',
                             '  {',  # no warning
                             '    loooong_value1, looooong_value2',
                             '  }',
                             '};',
                             '#if PREPROCESSOR',
                             '{',  # no warning
                             '  MutexLock l(&mu);',
                             '}',
                             '#endif'],
                            error_collector)
    self.assertEquals(1, error_collector.Results().count(
        '{ should almost always be at the end of the previous line'
        '  [whitespace/braces] [4]'))

    self.TestMultiLineLint(
        """
        foo(
          {
            loooooooooooooooong_value,
          });""",
        '')

  def testMismatchingSpacesInParens(self):
    self.TestLint('if (foo ) {', 'Mismatching spaces inside () in if'
                  '  [whitespace/parens] [5]')
    self.TestLint('switch ( foo) {', 'Mismatching spaces inside () in switch'
                  '  [whitespace/parens] [5]')
    self.TestLint('for (foo; ba; bar ) {', 'Mismatching spaces inside () in for'
                  '  [whitespace/parens] [5]')
    self.TestLint('for (; foo; bar) {', '')
    self.TestLint('for ( ; foo; bar) {', '')
    self.TestLint('for ( ; foo; bar ) {', '')
    self.TestLint('for (foo; bar; ) {', '')
    self.TestLint('while (  foo  ) {', 'Should have zero or one spaces inside'
                  ' ( and ) in while  [whitespace/parens] [5]')

  def testSpacingForFncall(self):
    self.TestLint('if (foo) {', '')
    self.TestLint('for (foo; bar; baz) {', '')
    self.TestLint('for (;;) {', '')
    # Space should be allowed in placement new operators.
    self.TestLint('Something* p = new (place) Something();', '')
    # Test that there is no warning when increment statement is empty.
    self.TestLint('for (foo; baz;) {', '')
    self.TestLint('for (foo;bar;baz) {', 'Missing space after ;'
                  '  [whitespace/semicolon] [3]')
    # we don't warn about this semicolon, at least for now
    self.TestLint('if (condition) {return &something; }',
                  '')
    # seen in some macros
    self.TestLint('DoSth();\\', '')
    # Test that there is no warning about semicolon here.
    self.TestLint('abc;// this is abc',
                  'At least two spaces is best between code'
                  ' and comments  [whitespace/comments] [2]')
    self.TestLint('while (foo) {', '')
    self.TestLint('switch (foo) {', '')
    self.TestLint('foo( bar)', 'Extra space after ( in function call'
                  '  [whitespace/parens] [4]')
    self.TestLint('foo(  // comment', '')
    self.TestLint('foo( // comment',
                  'At least two spaces is best between code'
                  ' and comments  [whitespace/comments] [2]')
    self.TestLint('foobar( \\', '')
    self.TestLint('foobar(     \\', '')
    self.TestLint('( a + b)', 'Extra space after ('
                  '  [whitespace/parens] [2]')
    self.TestLint('((a+b))', '')
    self.TestLint('foo (foo)', 'Extra space before ( in function call'
                  '  [whitespace/parens] [4]')
    # asm volatile () may have a space, as it isn't a function call.
    self.TestLint('asm volatile ("")', '')
    self.TestLint('__asm__ __volatile__ ("")', '')
    self.TestLint('} catch (const Foo& ex) {', '')
    self.TestLint('case (42):', '')
    self.TestLint('typedef foo (*foo)(foo)', '')
    self.TestLint('typedef foo (*foo12bar_)(foo)', '')
    self.TestLint('typedef foo (Foo::*bar)(foo)', '')
    self.TestLint('using foo = type (Foo::*bar)(foo)', '')
    self.TestLint('using foo = type (Foo::*bar)(', '')
    self.TestLint('using foo = type (Foo::*)(', '')
    self.TestLint('foo (Foo::*bar)(', '')
    self.TestLint('foo (x::y::*z)(', '')
    self.TestLint('foo (Foo::bar)(',
                  'Extra space before ( in function call'
                  '  [whitespace/parens] [4]')
    self.TestLint('foo (*bar)(', '')
    self.TestLint('typedef foo (Foo::*bar)(', '')
    self.TestLint('(foo)(bar)', '')
    self.TestLint('Foo (*foo)(bar)', '')
    self.TestLint('Foo (*foo)(Bar bar,', '')
    self.TestLint('char (*p)[sizeof(foo)] = &foo', '')
    self.TestLint('char (&ref)[sizeof(foo)] = &foo', '')
    self.TestLint('const char32 (*table[])[6];', '')
    # The sizeof operator is often written as if it were a function call, with
    # an opening parenthesis directly following the operator name, but it can
    # also be written like any other operator, with a space following the
    # operator name, and the argument optionally in parentheses.
    self.TestLint('sizeof(foo)', '')
    self.TestLint('sizeof foo', '')
    self.TestLint('sizeof (foo)', '')

  def testSpacingBeforeBraces(self):
    self.TestLint('if (foo){', 'Missing space before {'
                  '  [whitespace/braces] [5]')
    self.TestLint('for{', 'Missing space before {'
                  '  [whitespace/braces] [5]')
    self.TestLint('for {', '')
    self.TestLint('EXPECT_DEBUG_DEATH({', '')
    self.TestLint('std::is_convertible<A, B>{}', '')
    self.TestLint('blah{32}', 'Missing space before {'
                  '  [whitespace/braces] [5]')
    self.TestLint('int8_t{3}', '')
    self.TestLint('int16_t{3}', '')
    self.TestLint('int32_t{3}', '')
    self.TestLint('uint64_t{12345}', '')
    self.TestLint('constexpr int64_t kBatchGapMicros ='
                  ' int64_t{7} * 24 * 3600 * 1000000;  // 1 wk.', '')
    self.TestLint('MoveOnly(int i1, int i2) : ip1{new int{i1}}, '
                  'ip2{new int{i2}} {}',
                  '')

  def testSemiColonAfterBraces(self):
    self.TestLint('if (cond) { func(); };',
                  'You don\'t need a ; after a }  [readability/braces] [4]')
    self.TestLint('void Func() {};',
                  'You don\'t need a ; after a }  [readability/braces] [4]')
    self.TestLint('void Func() const {};',
                  'You don\'t need a ; after a }  [readability/braces] [4]')
    self.TestLint('class X {};', '')
    for keyword in ['struct', 'union']:
      for align in ['', ' alignas(16)']:
        for typename in ['', ' X']:
          for identifier in ['', ' x']:
            self.TestLint(keyword + align + typename + ' {}' + identifier + ';',
                          '')

    self.TestLint('class X : public Y {};', '')
    self.TestLint('class X : public MACRO() {};', '')
    self.TestLint('class X : public decltype(expr) {};', '')
    self.TestLint('DEFINE_FACADE(PCQueue::Watcher, PCQueue) {};', '')
    self.TestLint('VCLASS(XfaTest, XfaContextTest) {};', '')
    self.TestLint('class STUBBY_CLASS(H, E) {};', '')
    self.TestLint('class STUBBY2_CLASS(H, E) {};', '')
    self.TestLint('TEST(TestCase, TestName) {};',
                  'You don\'t need a ; after a }  [readability/braces] [4]')
    self.TestLint('TEST_F(TestCase, TestName) {};',
                  'You don\'t need a ; after a }  [readability/braces] [4]')

    self.TestLint('file_tocs_[i] = (FileToc) {a, b, c};', '')
    self.TestMultiLineLint('class X : public Y,\npublic Z {};', '')

  def testLambda(self):
    self.TestLint('auto x = []() {};', '')
    self.TestLint('return []() {};', '')
    self.TestMultiLineLint('auto x = []() {\n};\n', '')
    self.TestLint('int operator[](int x) {};',
                  'You don\'t need a ; after a }  [readability/braces] [4]')

    self.TestMultiLineLint('auto x = [&a,\nb]() {};', '')
    self.TestMultiLineLint('auto x = [&a,\nb]\n() {};', '')
    self.TestMultiLineLint('auto x = [&a,\n'
                           '          b](\n'
                           '    int a,\n'
                           '    int b) {\n'
                           '  return a +\n'
                           '         b;\n'
                           '};\n',
                           '')

    # Avoid false positives with operator[]
    self.TestLint('table_to_children[&*table].push_back(dependent);', '')

  def testBraceInitializerList(self):
    self.TestLint('MyStruct p = {1, 2};', '')
    self.TestLint('MyStruct p{1, 2};', '')
    self.TestLint('vector<int> p = {1, 2};', '')
    self.TestLint('vector<int> p{1, 2};', '')
    self.TestLint('x = vector<int>{1, 2};', '')
    self.TestLint('x = (struct in_addr){ 0 };', '')
    self.TestLint('Func(vector<int>{1, 2})', '')
    self.TestLint('Func((struct in_addr){ 0 })', '')
    self.TestLint('Func(vector<int>{1, 2}, 3)', '')
    self.TestLint('Func((struct in_addr){ 0 }, 3)', '')
    self.TestLint('LOG(INFO) << char{7};', '')
    self.TestLint('LOG(INFO) << char{7} << "!";', '')
    self.TestLint('int p[2] = {1, 2};', '')
    self.TestLint('return {1, 2};', '')
    self.TestLint('std::unique_ptr<Foo> foo{new Foo{}};', '')
    self.TestLint('auto foo = std::unique_ptr<Foo>{new Foo{}};', '')
    self.TestLint('static_assert(Max7String{}.IsValid(), "");', '')
    self.TestLint('map_of_pairs[{1, 2}] = 3;', '')
    self.TestLint('ItemView{has_offer() ? new Offer{offer()} : nullptr', '')
    self.TestLint('template <class T, EnableIf<::std::is_const<T>{}> = 0>', '')

    self.TestMultiLineLint('std::unique_ptr<Foo> foo{\n'
                           '  new Foo{}\n'
                           '};\n', '')
    self.TestMultiLineLint('std::unique_ptr<Foo> foo{\n'
                           '  new Foo{\n'
                           '    new Bar{}\n'
                           '  }\n'
                           '};\n', '')
    self.TestMultiLineLint('if (true) {\n'
                           '  if (false){ func(); }\n'
                           '}\n',
                           'Missing space before {  [whitespace/braces] [5]')
    self.TestMultiLineLint('MyClass::MyClass()\n'
                           '    : initializer_{\n'
                           '          Func()} {\n'
                           '}\n', '')
    self.TestLint('const pair<string, string> kCL' +
                  ('o' * 41) + 'gStr[] = {\n',
                  'Lines should be <= 80 characters long'
                  '  [whitespace/line_length] [2]')
    self.TestMultiLineLint('const pair<string, string> kCL' +
                           ('o' * 40) + 'ngStr[] =\n'
                           '    {\n'
                           '        {"gooooo", "oooogle"},\n'
                           '};\n', '')
    self.TestMultiLineLint('const pair<string, string> kCL' +
                           ('o' * 39) + 'ngStr[] =\n'
                           '    {\n'
                           '        {"gooooo", "oooogle"},\n'
                           '};\n', '{ should almost always be at the end of '
                           'the previous line  [whitespace/braces] [4]')

  def testSpacingAroundElse(self):
    self.TestLint('}else {', 'Missing space before else'
                  '  [whitespace/braces] [5]')
    self.TestLint('} else{', 'Missing space before {'
                  '  [whitespace/braces] [5]')
    self.TestLint('} else {', '')
    self.TestLint('} else if (foo) {', '')

  def testSpacingWithInitializerLists(self):
    self.TestLint('int v[1][3] = {{1, 2, 3}};', '')
    self.TestLint('int v[1][1] = {{0}};', '')

  def testSpacingForBinaryOps(self):
    self.TestLint('if (foo||bar) {', 'Missing spaces around ||'
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo<=bar) {', 'Missing spaces around <='
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo<bar) {', 'Missing spaces around <'
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo>bar) {', 'Missing spaces around >'
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo<bar->baz) {', 'Missing spaces around <'
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo<bar->bar) {', 'Missing spaces around <'
                  '  [whitespace/operators] [3]')
    self.TestLint('template<typename T = double>', '')
    self.TestLint('std::unique_ptr<No<Spaces>>', '')
    self.TestLint('typedef hash_map<Foo, Bar>', '')
    self.TestLint('10<<20', '')
    self.TestLint('10<<a',
                  'Missing spaces around <<  [whitespace/operators] [3]')
    self.TestLint('a<<20',
                  'Missing spaces around <<  [whitespace/operators] [3]')
    self.TestLint('a<<b',
                  'Missing spaces around <<  [whitespace/operators] [3]')
    self.TestLint('10LL<<20', '')
    self.TestLint('10ULL<<20', '')
    self.TestLint('a>>b',
                  'Missing spaces around >>  [whitespace/operators] [3]')
    self.TestLint('10>>b',
                  'Missing spaces around >>  [whitespace/operators] [3]')
    self.TestLint('LOG(ERROR)<<*foo',
                  'Missing spaces around <<  [whitespace/operators] [3]')
    self.TestLint('LOG(ERROR)<<&foo',
                  'Missing spaces around <<  [whitespace/operators] [3]')
    self.TestLint('StringCoder<vector<string>>::ToString()', '')
    self.TestLint('map<pair<int, int>, map<int, int>>::iterator', '')
    self.TestLint('func<int, pair<int, pair<int, int>>>()', '')
    self.TestLint('MACRO1(list<list<int>>)', '')
    self.TestLint('MACRO2(list<list<int>>, 42)', '')
    self.TestLint('void DoFoo(const set<vector<string>>& arg1);', '')
    self.TestLint('void SetFoo(set<vector<string>>* arg1);', '')
    self.TestLint('foo = new set<vector<string>>;', '')
    self.TestLint('reinterpret_cast<set<vector<string>>*>(a);', '')
    self.TestLint('MACRO(<<)', '')
    self.TestLint('MACRO(<<, arg)', '')
    self.TestLint('MACRO(<<=)', '')
    self.TestLint('MACRO(<<=, arg)', '')

    self.TestLint('using Vector3<T>::operator==;', '')
    self.TestLint('using Vector3<T>::operator!=;', '')

  def testSpacingBeforeLastSemicolon(self):
    self.TestLint('call_function() ;',
                  'Extra space before last semicolon. If this should be an '
                  'empty statement, use {} instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('while (true) ;',
                  'Extra space before last semicolon. If this should be an '
                  'empty statement, use {} instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('default:;',
                  'Semicolon defining empty statement. Use {} instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('      ;',
                  'Line contains only semicolon. If this should be an empty '
                  'statement, use {} instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('for (int i = 0; ;', '')

  def testEmptyBlockBody(self):
    self.TestLint('while (true);',
                  'Empty loop bodies should use {} or continue'
                  '  [whitespace/empty_loop_body] [5]')
    self.TestLint('if (true);',
                  'Empty conditional bodies should use {}'
                  '  [whitespace/empty_conditional_body] [5]')
    self.TestLint('while (true)', '')
    self.TestLint('while (true) continue;', '')
    self.TestLint('for (;;);',
                  'Empty loop bodies should use {} or continue'
                  '  [whitespace/empty_loop_body] [5]')
    self.TestLint('for (;;)', '')
    self.TestLint('for (;;) continue;', '')
    self.TestLint('for (;;) func();', '')
    self.TestLint('if (test) {}',
                  'If statement had no body and no else clause'
                  '  [whitespace/empty_if_body] [4]')
    self.TestLint('if (test) func();', '')
    self.TestLint('if (test) {} else {}', '')
    self.TestMultiLineLint("""while (true &&
                                     false);""",
                           'Empty loop bodies should use {} or continue'
                           '  [whitespace/empty_loop_body] [5]')
    self.TestMultiLineLint("""do {
                           } while (false);""",
                           '')
    self.TestMultiLineLint("""#define MACRO \\
                           do { \\
                           } while (false);""",
                           '')
    self.TestMultiLineLint("""do {
                           } while (false);  // next line gets a warning
                           while (false);""",
                           'Empty loop bodies should use {} or continue'
                           '  [whitespace/empty_loop_body] [5]')
    self.TestMultiLineLint("""if (test) {
                           }""",
                           'If statement had no body and no else clause'
                           '  [whitespace/empty_if_body] [4]')
    self.TestMultiLineLint("""if (test,
                               func({})) {
                           }""",
                           'If statement had no body and no else clause'
                           '  [whitespace/empty_if_body] [4]')
    self.TestMultiLineLint("""if (test)
                             func();""", '')
    self.TestLint('if (test) { hello; }', '')
    self.TestLint('if (test({})) { hello; }', '')
    self.TestMultiLineLint("""if (test) {
                             func();
                           }""", '')
    self.TestMultiLineLint("""if (test) {
                             // multiline
                             // comment
                           }""", '')
    self.TestMultiLineLint("""if (test) {  // comment
                           }""", '')
    self.TestMultiLineLint("""if (test) {
                           } else {
                           }""", '')
    self.TestMultiLineLint("""if (func(p1,
                               p2,
                               p3)) {
                             func();
                           }""", '')
    self.TestMultiLineLint("""if (func({}, p1)) {
                             func();
                           }""", '')

  def testSpacingForRangeBasedFor(self):
    # Basic correctly formatted case:
    self.TestLint('for (int i : numbers) {', '')

    # Missing space before colon:
    self.TestLint('for (int i: numbers) {',
                  'Missing space around colon in range-based for loop'
                  '  [whitespace/forcolon] [2]')
    # Missing space after colon:
    self.TestLint('for (int i :numbers) {',
                  'Missing space around colon in range-based for loop'
                  '  [whitespace/forcolon] [2]')
    # Missing spaces both before and after the colon.
    self.TestLint('for (int i:numbers) {',
                  'Missing space around colon in range-based for loop'
                  '  [whitespace/forcolon] [2]')

    # The scope operator '::' shouldn't cause warnings...
    self.TestLint('for (std::size_t i : sizes) {}', '')
    # ...but it shouldn't suppress them either.
    self.TestLint('for (std::size_t i: sizes) {}',
                  'Missing space around colon in range-based for loop'
                  '  [whitespace/forcolon] [2]')


  # Static or global STL strings.
  def testStaticOrGlobalSTLStrings(self):
    # A template for the error message for a const global/static string.
    error_msg = ('For a static/global string constant, use a C style '
                 'string instead: "%s[]".  [runtime/string] [4]')

    # The error message for a non-const global/static string variable.
    nonconst_error_msg = ('Static/global string variables are not permitted.'
                          '  [runtime/string] [4]')

    self.TestLint('string foo;',
                  nonconst_error_msg)
    self.TestLint('string kFoo = "hello";  // English',
                  nonconst_error_msg)
    self.TestLint('static string foo;',
                  nonconst_error_msg)
    self.TestLint('static const string foo;',
                  error_msg % 'static const char foo')
    self.TestLint('static const std::string foo;',
                  error_msg % 'static const char foo')
    self.TestLint('string Foo::bar;',
                  nonconst_error_msg)

    self.TestLint('std::string foo;',
                  nonconst_error_msg)
    self.TestLint('std::string kFoo = "hello";  // English',
                  nonconst_error_msg)
    self.TestLint('static std::string foo;',
                  nonconst_error_msg)
    self.TestLint('static const std::string foo;',
                  error_msg % 'static const char foo')
    self.TestLint('std::string Foo::bar;',
                  nonconst_error_msg)

    self.TestLint('::std::string foo;',
                  nonconst_error_msg)
    self.TestLint('::std::string kFoo = "hello";  // English',
                  nonconst_error_msg)
    self.TestLint('static ::std::string foo;',
                  nonconst_error_msg)
    self.TestLint('static const ::std::string foo;',
                  error_msg % 'static const char foo')
    self.TestLint('::std::string Foo::bar;',
                  nonconst_error_msg)

    self.TestLint('string* pointer', '')
    self.TestLint('string *pointer', '')
    self.TestLint('string* pointer = Func();', '')
    self.TestLint('string *pointer = Func();', '')
    self.TestLint('const string* pointer', '')
    self.TestLint('const string *pointer', '')
    self.TestLint('const string* pointer = Func();', '')
    self.TestLint('const string *pointer = Func();', '')
    self.TestLint('string const* pointer', '')
    self.TestLint('string const *pointer', '')
    self.TestLint('string const* pointer = Func();', '')
    self.TestLint('string const *pointer = Func();', '')
    self.TestLint('string* const pointer', '')
    self.TestLint('string *const pointer', '')
    self.TestLint('string* const pointer = Func();', '')
    self.TestLint('string *const pointer = Func();', '')
    self.TestLint('string Foo::bar() {}', '')
    self.TestLint('string Foo::operator*() {}', '')
    # Rare case.
    self.TestLint('string foo("foobar");', nonconst_error_msg)
    # Should not catch local or member variables.
    self.TestLint('  string foo', '')
    # Should not catch functions.
    self.TestLint('string EmptyString() { return ""; }', '')
    self.TestLint('string EmptyString () { return ""; }', '')
    self.TestLint('string const& FileInfo::Pathname() const;', '')
    self.TestLint('string const &FileInfo::Pathname() const;', '')
    self.TestLint('string VeryLongNameFunctionSometimesEndsWith(\n'
                  '    VeryLongNameType very_long_name_variable) {}', '')
    self.TestLint('template<>\n'
                  'string FunctionTemplateSpecialization<SomeType>(\n'
                  '      int x) { return ""; }', '')
    self.TestLint('template<>\n'
                  'string FunctionTemplateSpecialization<vector<A::B>* >(\n'
                  '      int x) { return ""; }', '')

    # should not catch methods of template classes.
    self.TestLint('string Class<Type>::Method() const {\n'
                  '  return "";\n'
                  '}\n', '')
    self.TestLint('string Class<Type>::Method(\n'
                  '   int arg) const {\n'
                  '  return "";\n'
                  '}\n', '')

    # Check multiline cases.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['// Copyright 2014 Your Company.',
                             'string Class',
                             '::MemberFunction1();',
                             'string Class::',
                             'MemberFunction2();',
                             'string Class::',
                             'NestedClass::MemberFunction3();',
                             'string TemplateClass<T>::',
                             'NestedClass::MemberFunction4();',
                             'const string Class',
                             '::static_member_variable1;',
                             'const string Class::',
                             'static_member_variable2;',
                             'const string Class',
                             '::static_member_variable3 = "initial value";',
                             'const string Class::',
                             'static_member_variable4 = "initial value";',
                             'string Class::',
                             'static_member_variable5;',
                             ''],
                            error_collector)
    self.assertEquals(error_collector.Results(),
                      [error_msg % 'const char Class::static_member_variable1',
                       error_msg % 'const char Class::static_member_variable2',
                       error_msg % 'const char Class::static_member_variable3',
                       error_msg % 'const char Class::static_member_variable4',
                       nonconst_error_msg])

  def testNoSpacesInFunctionCalls(self):
    self.TestLint('TellStory(1, 3);',
                  '')
    self.TestLint('TellStory(1, 3 );',
                  'Extra space before )'
                  '  [whitespace/parens] [2]')
    self.TestLint('TellStory(1 /* wolf */, 3 /* pigs */);',
                  '')
    self.TestMultiLineLint("""TellStory(1, 3
                                        );""",
                           'Closing ) should be moved to the previous line'
                           '  [whitespace/parens] [2]')
    self.TestMultiLineLint("""TellStory(Wolves(1),
                                        Pigs(3
                                        ));""",
                           'Closing ) should be moved to the previous line'
                           '  [whitespace/parens] [2]')
    self.TestMultiLineLint("""TellStory(1,
                                        3 );""",
                           'Extra space before )'
                           '  [whitespace/parens] [2]')

  def testToDoComments(self):
    start_space = ('Too many spaces before TODO'
                   '  [whitespace/todo] [2]')
    missing_username = ('Missing username in TODO; it should look like '
                        '"// TODO(my_username): Stuff."'
                        '  [readability/todo] [2]')
    end_space = ('TODO(my_username) should be followed by a space'
                 '  [whitespace/todo] [2]')

    self.TestLint('//   TODOfix this',
                  [start_space, missing_username, end_space])
    self.TestLint('//   TODO(ljenkins)fix this',
                  [start_space, end_space])
    self.TestLint('//   TODO fix this',
                  [start_space, missing_username])
    self.TestLint('// TODO fix this', missing_username)
    self.TestLint('// TODO: fix this', missing_username)
    self.TestLint('//TODO(ljenkins): Fix this',
                  'Should have a space between // and comment'
                  '  [whitespace/comments] [4]')
    self.TestLint('// TODO(ljenkins):Fix this', end_space)
    self.TestLint('// TODO(ljenkins):', '')
    self.TestLint('// TODO(ljenkins): fix this', '')
    self.TestLint('// TODO(ljenkins): Fix this', '')
    self.TestLint('#if 1  // TEST_URLTODOCID_WHICH_HAS_THAT_WORD_IN_IT_H_', '')
    self.TestLint('// See also similar TODO above', '')
    self.TestLint(r'EXPECT_EQ("\\", '
                  r'NormalizePath("/./../foo///bar/..//x/../..", ""));',
                  '')

  def testTwoSpacesBetweenCodeAndComments(self):
    self.TestLint('} // namespace foo',
                  'At least two spaces is best between code and comments'
                  '  [whitespace/comments] [2]')
    self.TestLint('}// namespace foo',
                  'At least two spaces is best between code and comments'
                  '  [whitespace/comments] [2]')
    self.TestLint('printf("foo"); // Outside quotes.',
                  'At least two spaces is best between code and comments'
                  '  [whitespace/comments] [2]')
    self.TestLint('int i = 0;  // Having two spaces is fine.', '')
    self.TestLint('int i = 0;   // Having three spaces is OK.', '')
    self.TestLint('// Top level comment', '')
    self.TestLint('  // Line starts with two spaces.', '')
    self.TestMultiLineLint('void foo() {\n'
                           '  { // A scope is opening.\n'
                           '    int a;', '')
    self.TestMultiLineLint('void foo() {\n'
                           '  { // A scope is opening.\n'
                           '#define A a',
                           'At least two spaces is best between code and '
                           'comments  [whitespace/comments] [2]')
    self.TestMultiLineLint('  foo();\n'
                           '  { // An indented scope is opening.\n'
                           '    int a;', '')
    self.TestMultiLineLint('vector<int> my_elements = {// first\n'
                           '                           1,', '')
    self.TestMultiLineLint('vector<int> my_elements = {// my_elements is ..\n'
                           '    1,',
                           'At least two spaces is best between code and '
                           'comments  [whitespace/comments] [2]')
    self.TestLint('if (foo) { // not a pure scope; comment is too close!',
                  'At least two spaces is best between code and comments'
                  '  [whitespace/comments] [2]')
    self.TestLint('printf("// In quotes.")', '')
    self.TestLint('printf("\\"%s // In quotes.")', '')
    self.TestLint('printf("%s", "// In quotes.")', '')

  def testSpaceAfterCommentMarker(self):
    self.TestLint('//', '')
    self.TestLint('//x', 'Should have a space between // and comment'
                  '  [whitespace/comments] [4]')
    self.TestLint('// x', '')
    self.TestLint('///', '')
    self.TestLint('/// x', '')
    self.TestLint('//!', '')
    self.TestLint('//----', '')
    self.TestLint('//====', '')
    self.TestLint('//////', '')
    self.TestLint('////// x', '')
    self.TestLint('///< x', '') # After-member Doxygen comment
    self.TestLint('//!< x', '') # After-member Doxygen comment
    self.TestLint('////x', 'Should have a space between // and comment'
                  '  [whitespace/comments] [4]')
    self.TestLint('//}', '')
    self.TestLint('//}x', 'Should have a space between // and comment'
                  '  [whitespace/comments] [4]')
    self.TestLint('//!<x', 'Should have a space between // and comment'
                  '  [whitespace/comments] [4]')
    self.TestLint('///<x', 'Should have a space between // and comment'
                  '  [whitespace/comments] [4]')

  # Test a line preceded by empty or comment lines.  There was a bug
  # that caused it to print the same warning N times if the erroneous
  # line was preceded by N lines of empty or comment lines.  To be
  # precise, the '// marker so line numbers and indices both start at
  # 1' line was also causing the issue.
  def testLinePrecededByEmptyOrCommentLines(self):
    def DoTest(self, lines):
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData('foo.cc', 'cc', lines, error_collector)
      # The warning appears only once.
      self.assertEquals(
          1,
          error_collector.Results().count(
              'Do not use namespace using-directives.  '
              'Use using-declarations instead.'
              '  [build/namespaces] [5]'))
    DoTest(self, ['using namespace foo;'])
    DoTest(self, ['', '', '', 'using namespace foo;'])
    DoTest(self, ['// hello', 'using namespace foo;'])

  def testNewlineAtEOF(self):
    def DoTest(self, data, is_missing_eof):
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData('foo.cc', 'cc', data.split('\n'),
                              error_collector)
      # The warning appears only once.
      self.assertEquals(
          int(is_missing_eof),
          error_collector.Results().count(
              'Could not find a newline character at the end of the file.'
              '  [whitespace/ending_newline] [5]'))

    DoTest(self, '// Newline\n// at EOF\n', False)
    DoTest(self, '// No newline\n// at EOF', True)

  def testInvalidUtf8(self):
    def DoTest(self, raw_bytes, has_invalid_utf8):
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData(
          'foo.cc', 'cc',
          unicode(raw_bytes, 'utf8', 'replace').split('\n'),
          error_collector)
      # The warning appears only once.
      self.assertEquals(
          int(has_invalid_utf8),
          error_collector.Results().count(
              'Line contains invalid UTF-8'
              ' (or Unicode replacement character).'
              '  [readability/utf8] [5]'))

    DoTest(self, 'Hello world\n', False)
    DoTest(self, '\xe9\x8e\xbd\n', False)
    DoTest(self, '\xe9x\x8e\xbd\n', True)
    # This is the encoding of the replacement character itself (which
    # you can see by evaluating codecs.getencoder('utf8')(u'\ufffd')).
    DoTest(self, '\xef\xbf\xbd\n', True)

  def testBadCharacters(self):
    # Test for NUL bytes only
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('nul.cc', 'cc',
                            ['// Copyright 2014 Your Company.',
                             '\0', ''], error_collector)
    self.assertEquals(
        error_collector.Results(),
        'Line contains NUL byte.  [readability/nul] [5]')

    # Make sure both NUL bytes and UTF-8 are caught if they appear on
    # the same line.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'nul_utf8.cc', 'cc',
        ['// Copyright 2014 Your Company.',
         unicode('\xe9x\0', 'utf8', 'replace'), ''],
        error_collector)
    self.assertEquals(
        error_collector.Results(),
        ['Line contains invalid UTF-8 (or Unicode replacement character).'
         '  [readability/utf8] [5]',
         'Line contains NUL byte.  [readability/nul] [5]'])

  def testIsBlankLine(self):
    self.assert_(cpplint.IsBlankLine(''))
    self.assert_(cpplint.IsBlankLine(' '))
    self.assert_(cpplint.IsBlankLine(' \t\r\n'))
    self.assert_(not cpplint.IsBlankLine('int a;'))
    self.assert_(not cpplint.IsBlankLine('{'))

  def testBlankLinesCheck(self):
    self.TestBlankLinesCheck(['{\n', '\n', '\n', '}\n'], 1, 1)
    self.TestBlankLinesCheck(['  if (foo) {\n', '\n', '  }\n'], 1, 1)
    self.TestBlankLinesCheck(
        ['\n', '// {\n', '\n', '\n', '// Comment\n', '{\n', '}\n'], 0, 0)
    self.TestBlankLinesCheck(['\n', 'run("{");\n', '\n'], 0, 0)
    self.TestBlankLinesCheck(['\n', '  if (foo) { return 0; }\n', '\n'], 0, 0)
    self.TestBlankLinesCheck(
        ['int x(\n', '    int a) {\n', '\n', 'return 0;\n', '}'], 0, 0)
    self.TestBlankLinesCheck(
        ['int x(\n', '    int a) const {\n', '\n', 'return 0;\n', '}'], 0, 0)
    self.TestBlankLinesCheck(
        ['int x(\n', '     int a) {\n', '\n', 'return 0;\n', '}'], 1, 0)
    self.TestBlankLinesCheck(
        ['int x(\n', '   int a) {\n', '\n', 'return 0;\n', '}'], 1, 0)

  def testAllowBlankLineBeforeClosingNamespace(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['namespace {',
                             '',
                             '}  // namespace',
                             'namespace another_namespace {',
                             '',
                             '}',
                             'namespace {',
                             '',
                             'template<class T, ',
                             '         class A = hoge<T>, ',
                             '         class B = piyo<T>, ',
                             '         class C = fuga<T> >',
                             'class D {',
                             ' public:',
                             '};',
                             '', '', '', '',
                             '}'],
                            error_collector)
    self.assertEquals(0, error_collector.Results().count(
        'Redundant blank line at the end of a code block should be deleted.'
        '  [whitespace/blank_line] [3]'))

  def testAllowBlankLineBeforeIfElseChain(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['if (hoge) {',
                             '',  # No warning
                             '} else if (piyo) {',
                             '',  # No warning
                             '} else if (piyopiyo) {',
                             '  hoge = true;',  # No warning
                             '} else {',
                             '',  # Warning on this line
                             '}'],
                            error_collector)
    self.assertEquals(1, error_collector.Results().count(
        'Redundant blank line at the end of a code block should be deleted.'
        '  [whitespace/blank_line] [3]'))

  def testAllowBlankLineAfterExtern(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['extern "C" {',
                             '',
                             'EXPORTAPI void APICALL Some_function() {}',
                             '',
                             '}'],
                            error_collector)
    self.assertEquals(0, error_collector.Results().count(
        'Redundant blank line at the start of a code block should be deleted.'
        '  [whitespace/blank_line] [2]'))
    self.assertEquals(0, error_collector.Results().count(
        'Redundant blank line at the end of a code block should be deleted.'
        '  [whitespace/blank_line] [3]'))

  def testBlankLineBeforeSectionKeyword(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['class A {',
                             ' public:',
                             ' protected:',   # warning 1
                             ' private:',     # warning 2
                             '  struct B {',
                             '   public:',
                             '   private:'] +  # warning 3
                            ([''] * 100) +  # Make A and B longer than 100 lines
                            ['  };',
                             '  struct C {',
                             '   protected:',
                             '   private:',  # C is too short for warnings
                             '  };',
                             '};',
                             'class D',
                             '    : public {',
                             ' public:',  # no warning
                             '};',
                             'class E {\\',
                             ' public:\\'] +
                            (['\\'] * 100) +  # Makes E > 100 lines
                            ['  int non_empty_line;\\',
                             ' private:\\',   # no warning
                             '  int a;\\',
                             '};'],
                            error_collector)
    self.assertEquals(2, error_collector.Results().count(
        '"private:" should be preceded by a blank line'
        '  [whitespace/blank_line] [3]'))
    self.assertEquals(1, error_collector.Results().count(
        '"protected:" should be preceded by a blank line'
        '  [whitespace/blank_line] [3]'))

  def testNoBlankLineAfterSectionKeyword(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['class A {',
                             ' public:',
                             '',  # warning 1
                             ' private:',
                             '',  # warning 2
                             '  struct B {',
                             '   protected:',
                             '',  # warning 3
                             '  };',
                             '};'],
                            error_collector)
    self.assertEquals(1, error_collector.Results().count(
        'Do not leave a blank line after "public:"'
        '  [whitespace/blank_line] [3]'))
    self.assertEquals(1, error_collector.Results().count(
        'Do not leave a blank line after "protected:"'
        '  [whitespace/blank_line] [3]'))
    self.assertEquals(1, error_collector.Results().count(
        'Do not leave a blank line after "private:"'
        '  [whitespace/blank_line] [3]'))

  def testAllowBlankLinesInRawStrings(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['// Copyright 2014 Your Company.',
                             'static const char *kData[] = {R"(',
                             '',
                             ')", R"(',
                             '',
                             ')"};',
                             ''],
                            error_collector)
    self.assertEquals('', error_collector.Results())

  def testElseOnSameLineAsClosingBraces(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['if (hoge) {',
                             '}',
                             'else if (piyo) {',  # Warning on this line
                             '}',
                             ' else {'  # Warning on this line
                             '',
                             '}'],
                            error_collector)
    self.assertEquals(2, error_collector.Results().count(
        'An else should appear on the same line as the preceding }'
        '  [whitespace/newline] [4]'))

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['if (hoge) {',
                             '',
                             '}',
                             'else',  # Warning on this line
                             '{',
                             '',
                             '}'],
                            error_collector)
    self.assertEquals(1, error_collector.Results().count(
        'An else should appear on the same line as the preceding }'
        '  [whitespace/newline] [4]'))

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['if (hoge) {',
                             '',
                             '}',
                             'else_function();'],
                            error_collector)
    self.assertEquals(0, error_collector.Results().count(
        'An else should appear on the same line as the preceding }'
        '  [whitespace/newline] [4]'))

  def testMultipleStatementsOnSameLine(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['for (int i = 0; i < 1; i++) {}',
                             'switch (x) {',
                             '  case 0: func(); break; ',
                             '}',
                             'sum += MathUtil::SafeIntRound(x); x += 0.1;'],
                            error_collector)
    self.assertEquals(0, error_collector.Results().count(
        'More than one command on the same line  [whitespace/newline] [0]'))

    old_verbose_level = cpplint._cpplint_state.verbose_level
    cpplint._cpplint_state.verbose_level = 0
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['sum += MathUtil::SafeIntRound(x); x += 0.1;'],
                            error_collector)
    cpplint._cpplint_state.verbose_level = old_verbose_level

  def testEndOfNamespaceComments(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['namespace {',
                             '',
                             '}',  # No warning (too short)
                             'namespace expected {',
                             '}  // namespace mismatched',  # Warning here
                             'namespace {',
                             '}  // namespace mismatched',  # Warning here
                             'namespace outer { namespace nested {'] +
                            ([''] * 10) +
                            ['}',  # Warning here
                             '}',  # Warning here
                             'namespace {'] +
                            ([''] * 10) +
                            ['}',  # Warning here
                             'namespace {'] +
                            ([''] * 10) +
                            ['}  // namespace some description',  # Anon warning
                             'namespace {'] +
                            ([''] * 10) +
                            ['}  // namespace anonymous',  # Variant warning
                             'namespace {'] +
                            ([''] * 10) +
                            ['}  // anonymous namespace (utils)',  # Variant
                             'namespace {'] +
                            ([''] * 10) +
                            ['}  // anonymous namespace',  # No warning
                             'namespace missing_comment {'] +
                            ([''] * 10) +
                            ['}',  # Warning here
                             'namespace no_warning {'] +
                            ([''] * 10) +
                            ['}  // namespace no_warning',
                             'namespace no_warning {'] +
                            ([''] * 10) +
                            ['};  // end namespace no_warning',
                             '#define MACRO \\',
                             'namespace c_style { \\'] +
                            (['\\'] * 10) +
                            ['}  /* namespace c_style. */ \\',
                             ';'],
                            error_collector)
    self.assertEquals(1, error_collector.Results().count(
        'Namespace should be terminated with "// namespace expected"'
        '  [readability/namespace] [5]'))
    self.assertEquals(1, error_collector.Results().count(
        'Namespace should be terminated with "// namespace outer"'
        '  [readability/namespace] [5]'))
    self.assertEquals(1, error_collector.Results().count(
        'Namespace should be terminated with "// namespace nested"'
        '  [readability/namespace] [5]'))
    self.assertEquals(3, error_collector.Results().count(
        'Anonymous namespace should be terminated with "// namespace"'
        '  [readability/namespace] [5]'))
    self.assertEquals(2, error_collector.Results().count(
        'Anonymous namespace should be terminated with "// namespace" or'
        ' "// anonymous namespace"'
        '  [readability/namespace] [5]'))
    self.assertEquals(1, error_collector.Results().count(
        'Namespace should be terminated with "// namespace missing_comment"'
        '  [readability/namespace] [5]'))
    self.assertEquals(0, error_collector.Results().count(
        'Namespace should be terminated with "// namespace no_warning"'
        '  [readability/namespace] [5]'))

  def testElseClauseNotOnSameLineAsElse(self):
    self.TestLint('  else DoSomethingElse();',
                  'Else clause should never be on same line as else '
                  '(use 2 lines)  [whitespace/newline] [4]')
    self.TestLint('  else ifDoSomethingElse();',
                  'Else clause should never be on same line as else '
                  '(use 2 lines)  [whitespace/newline] [4]')
    self.TestLint('  } else if (blah) {', '')
    self.TestLint('  variable_ends_in_else = true;', '')

  def testComma(self):
    self.TestLint('a = f(1,2);',
                  'Missing space after ,  [whitespace/comma] [3]')
    self.TestLint('int tmp=a,a=b,b=tmp;',
                  ['Missing spaces around =  [whitespace/operators] [4]',
                   'Missing space after ,  [whitespace/comma] [3]'])
    self.TestLint('f(a, /* name */ b);', '')
    self.TestLint('f(a, /* name */b);', '')
    self.TestLint('f(a, /* name */-1);', '')
    self.TestLint('f(a, /* name */"1");', '')
    self.TestLint('f(1, /* empty macro arg */, 2)', '')
    self.TestLint('f(1,, 2)', '')
    self.TestLint('operator,()', '')
    self.TestLint('operator,(a,b)',
                  'Missing space after ,  [whitespace/comma] [3]')

  def testEqualsOperatorSpacing(self):
    self.TestLint('int tmp= a;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('int tmp =a;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('int tmp=a;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('int tmp= 7;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('int tmp =7;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('int tmp=7;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('int* tmp=*p;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('int* tmp= *p;',
                  'Missing spaces around =  [whitespace/operators] [4]')
    self.TestMultiLineLint(
        TrimExtraIndent('''
            lookahead_services_=
              ::strings::Split(FLAGS_ls, ",", ::strings::SkipEmpty());'''),
        'Missing spaces around =  [whitespace/operators] [4]')
    self.TestLint('bool result = a>=42;',
                  'Missing spaces around >=  [whitespace/operators] [3]')
    self.TestLint('bool result = a<=42;',
                  'Missing spaces around <=  [whitespace/operators] [3]')
    self.TestLint('bool result = a==42;',
                  'Missing spaces around ==  [whitespace/operators] [3]')
    self.TestLint('auto result = a!=42;',
                  'Missing spaces around !=  [whitespace/operators] [3]')
    self.TestLint('int a = b!=c;',
                  'Missing spaces around !=  [whitespace/operators] [3]')
    self.TestLint('a&=42;', '')
    self.TestLint('a|=42;', '')
    self.TestLint('a^=42;', '')
    self.TestLint('a+=42;', '')
    self.TestLint('a*=42;', '')
    self.TestLint('a/=42;', '')
    self.TestLint('a%=42;', '')
    self.TestLint('a>>=5;', '')
    self.TestLint('a<<=5;', '')

  def testShiftOperatorSpacing(self):
    self.TestLint('a<<b',
                  'Missing spaces around <<  [whitespace/operators] [3]')
    self.TestLint('a>>b',
                  'Missing spaces around >>  [whitespace/operators] [3]')
    self.TestLint('1<<20', '')
    self.TestLint('1024>>10', '')
    self.TestLint('Kernel<<<1, 2>>>()', '')

  def testIndent(self):
    self.TestLint('static int noindent;', '')
    self.TestLint('  int two_space_indent;', '')
    self.TestLint('    int four_space_indent;', '')
    self.TestLint(' int one_space_indent;',
                  'Weird number of spaces at line-start.  '
                  'Are you using a 2-space indent?  [whitespace/indent] [3]')
    self.TestLint('   int three_space_indent;',
                  'Weird number of spaces at line-start.  '
                  'Are you using a 2-space indent?  [whitespace/indent] [3]')
    self.TestLint(' char* one_space_indent = "public:";',
                  'Weird number of spaces at line-start.  '
                  'Are you using a 2-space indent?  [whitespace/indent] [3]')
    self.TestLint(' public:', '')
    self.TestLint('  protected:', '')
    self.TestLint('   private:', '')
    self.TestLint(' protected: \\', '')
    self.TestLint('  public:      \\', '')
    self.TestLint('   private:   \\', '')
    self.TestMultiLineLint(
        TrimExtraIndent("""
            class foo {
             public slots:
              void bar();
            };"""),
        'Weird number of spaces at line-start.  '
        'Are you using a 2-space indent?  [whitespace/indent] [3]')
    self.TestMultiLineLint(
        TrimExtraIndent('''
            static const char kRawString[] = R"("
             ")";'''),
        '')
    self.TestMultiLineLint(
        TrimExtraIndent('''
            KV<Query,
               Tuple<TaxonomyId, PetacatCategoryId, double>>'''),
        '')
    self.TestMultiLineLint(
        ' static const char kSingleLineRawString[] = R"(...)";',
        'Weird number of spaces at line-start.  '
        'Are you using a 2-space indent?  [whitespace/indent] [3]')

  def testSectionIndent(self):
    self.TestMultiLineLint(
        """
        class A {
         public:  // no warning
          private:  // warning here
        };""",
        'private: should be indented +1 space inside class A'
        '  [whitespace/indent] [3]')
    self.TestMultiLineLint(
        """
        class B {
         public:  // no warning
          template<> struct C {
            public:    // warning here
           protected:  // no warning
          };
        };""",
        'public: should be indented +1 space inside struct C'
        '  [whitespace/indent] [3]')
    self.TestMultiLineLint(
        """
        struct D {
         };""",
        'Closing brace should be aligned with beginning of struct D'
        '  [whitespace/indent] [3]')
    self.TestMultiLineLint(
        """
         template<typename E> class F {
        };""",
        'Closing brace should be aligned with beginning of class F'
        '  [whitespace/indent] [3]')
    self.TestMultiLineLint(
        """
        class G {
          Q_OBJECT
        public slots:
        signals:
        };""",
        ['public slots: should be indented +1 space inside class G'
         '  [whitespace/indent] [3]',
         'signals: should be indented +1 space inside class G'
         '  [whitespace/indent] [3]'])
    self.TestMultiLineLint(
        """
        class H {
          /* comments */ class I {
           public:  // no warning
            private:  // warning here
          };
        };""",
        'private: should be indented +1 space inside class I'
        '  [whitespace/indent] [3]')
    self.TestMultiLineLint(
        """
        class J
            : public ::K {
         public:  // no warning
          protected:  // warning here
        };""",
        'protected: should be indented +1 space inside class J'
        '  [whitespace/indent] [3]')
    self.TestMultiLineLint(
        """
        class L
            : public M,
              public ::N {
        };""",
        '')
    self.TestMultiLineLint(
        """
        template <class O,
                  class P,
                  class Q,
                  typename R>
        static void Func() {
        }""",
        '')

  def testConditionals(self):
    self.TestMultiLineLint(
        """
        if (foo)
          goto fail;
          goto fail;""",
        'If/else bodies with multiple statements require braces'
        '  [readability/braces] [4]')
    self.TestMultiLineLint(
        """
        if (foo)
          goto fail; goto fail;""",
        'If/else bodies with multiple statements require braces'
        '  [readability/braces] [4]')
    self.TestMultiLineLint(
        """
        if (foo)
          foo;
        else
          goto fail;
          goto fail;""",
        'If/else bodies with multiple statements require braces'
        '  [readability/braces] [4]')
    self.TestMultiLineLint(
        """
        if (foo) goto fail;
          goto fail;""",
        'If/else bodies with multiple statements require braces'
        '  [readability/braces] [4]')
    self.TestMultiLineLint(
        """
        if (foo)
          if (bar)
            baz;
          else
            qux;""",
        'Else clause should be indented at the same level as if. Ambiguous'
        ' nested if/else chains require braces.  [readability/braces] [4]')
    self.TestMultiLineLint(
        """
        if (foo)
          if (bar)
            baz;
        else
          qux;""",
        'Else clause should be indented at the same level as if. Ambiguous'
        ' nested if/else chains require braces.  [readability/braces] [4]')
    self.TestMultiLineLint(
        """
        if (foo) {
          bar;
          baz;
        } else
          qux;""",
        'If an else has a brace on one side, it should have it on both'
        '  [readability/braces] [5]')
    self.TestMultiLineLint(
        """
        if (foo)
          bar;
        else {
          baz;
        }""",
        'If an else has a brace on one side, it should have it on both'
        '  [readability/braces] [5]')
    self.TestMultiLineLint(
        """
        if (foo)
          bar;
        else if (baz) {
          qux;
        }""",
        'If an else has a brace on one side, it should have it on both'
        '  [readability/braces] [5]')
    self.TestMultiLineLint(
        """
        if (foo) {
          bar;
        } else if (baz)
          qux;""",
        'If an else has a brace on one side, it should have it on both'
        '  [readability/braces] [5]')
    self.TestMultiLineLint(
        """
        if (foo)
          goto fail;
        bar;""",
        '')
    self.TestMultiLineLint(
        """
        if (foo
            && bar) {
          baz;
          qux;
        }""",
        '')
    self.TestMultiLineLint(
        """
        if (foo)
          goto
            fail;""",
        '')
    self.TestMultiLineLint(
        """
        if (foo)
          bar;
        else
          baz;
        qux;""",
        '')
    self.TestMultiLineLint(
        """
        for (;;) {
          if (foo)
            bar;
          else
            baz;
        }""",
        '')
    self.TestMultiLineLint(
        """
        if (foo)
          bar;
        else if (baz)
          baz;""",
        '')
    self.TestMultiLineLint(
        """
        if (foo)
          bar;
        else
          baz;""",
        '')
    self.TestMultiLineLint(
        """
        if (foo) {
          bar;
        } else {
          baz;
        }""",
        '')
    self.TestMultiLineLint(
        """
        if (foo) {
          bar;
        } else if (baz) {
          qux;
        }""",
        '')
    # Note: this is an error for a different reason, but should not trigger the
    # single-line if error.
    self.TestMultiLineLint(
        """
        if (foo)
        {
          bar;
          baz;
        }""",
        '{ should almost always be at the end of the previous line'
        '  [whitespace/braces] [4]')
    self.TestMultiLineLint(
        """
        if (foo) { \\
          bar; \\
          baz; \\
        }""",
        '')
    self.TestMultiLineLint(
        """
        void foo() { if (bar) baz; }""",
        '')
    self.TestMultiLineLint(
        """
        #if foo
          bar;
        #else
          baz;
          qux;
        #endif""",
        '')
    self.TestMultiLineLint(
        """void F() {
          variable = [] { if (true); };
          variable =
              [] { if (true); };
          Call(
              [] { if (true); },
              [] { if (true); });
        }""",
        '')

  def testTab(self):
    self.TestLint('\tint a;',
                  'Tab found; better to use spaces  [whitespace/tab] [1]')
    self.TestLint('int a = 5;\t\t// set a to 5',
                  'Tab found; better to use spaces  [whitespace/tab] [1]')

  def testParseArguments(self):
    old_usage = cpplint._USAGE
    old_error_categories = cpplint._ERROR_CATEGORIES
    old_output_format = cpplint._cpplint_state.output_format
    old_verbose_level = cpplint._cpplint_state.verbose_level
    old_headers = cpplint._hpp_headers
    old_filters = cpplint._cpplint_state.filters
    old_line_length = cpplint._line_length
    old_valid_extensions = cpplint._valid_extensions
    try:
      # Don't print usage during the tests, or filter categories
      cpplint._USAGE = ''
      cpplint._ERROR_CATEGORIES = ''

      self.assertRaises(SystemExit, cpplint.ParseArguments, [])
      self.assertRaises(SystemExit, cpplint.ParseArguments, ['--badopt'])
      self.assertRaises(SystemExit, cpplint.ParseArguments, ['--help'])
      self.assertRaises(SystemExit, cpplint.ParseArguments, ['--v=0'])
      self.assertRaises(SystemExit, cpplint.ParseArguments, ['--filter='])
      # This is illegal because all filters must start with + or -
      self.assertRaises(SystemExit, cpplint.ParseArguments, ['--filter=foo'])
      self.assertRaises(SystemExit, cpplint.ParseArguments,
                        ['--filter=+a,b,-c'])
      self.assertRaises(SystemExit, cpplint.ParseArguments, ['--headers'])

      self.assertEquals(['foo.cc'], cpplint.ParseArguments(['foo.cc']))
      self.assertEquals(old_output_format, cpplint._cpplint_state.output_format)
      self.assertEquals(old_verbose_level, cpplint._cpplint_state.verbose_level)

      self.assertEquals(['foo.cc'],
                        cpplint.ParseArguments(['--v=1', 'foo.cc']))
      self.assertEquals(1, cpplint._cpplint_state.verbose_level)
      self.assertEquals(['foo.h'],
                        cpplint.ParseArguments(['--v=3', 'foo.h']))
      self.assertEquals(3, cpplint._cpplint_state.verbose_level)
      self.assertEquals(['foo.cpp'],
                        cpplint.ParseArguments(['--verbose=5', 'foo.cpp']))
      self.assertEquals(5, cpplint._cpplint_state.verbose_level)
      self.assertRaises(ValueError,
                        cpplint.ParseArguments, ['--v=f', 'foo.cc'])

      self.assertEquals(['foo.cc'],
                        cpplint.ParseArguments(['--output=emacs', 'foo.cc']))
      self.assertEquals('emacs', cpplint._cpplint_state.output_format)
      self.assertEquals(['foo.h'],
                        cpplint.ParseArguments(['--output=vs7', 'foo.h']))
      self.assertEquals('vs7', cpplint._cpplint_state.output_format)
      self.assertRaises(SystemExit,
                        cpplint.ParseArguments, ['--output=blah', 'foo.cc'])

      filt = '-,+whitespace,-whitespace/indent'
      self.assertEquals(['foo.h'],
                        cpplint.ParseArguments(['--filter='+filt, 'foo.h']))
      self.assertEquals(['-', '+whitespace', '-whitespace/indent'],
                        cpplint._cpplint_state.filters)

      self.assertEquals(['foo.cc', 'foo.h'],
                        cpplint.ParseArguments(['foo.cc', 'foo.h']))

      self.assertEqual(['foo.h'],
                       cpplint.ParseArguments(['--linelength=120', 'foo.h']))
      self.assertEqual(120, cpplint._line_length)

      self.assertEqual(['foo.h'],
                       cpplint.ParseArguments(['--extensions=hpp,cpp,cpp', 'foo.h']))
      self.assertEqual(set(['hpp', 'cpp']), cpplint._valid_extensions)
      
      self.assertEqual(set(['h']), cpplint._hpp_headers)  # Default value
      self.assertEqual(['foo.h'],
                       cpplint.ParseArguments(['--extensions=cpp,cpp', '--headers=hpp,h', 'foo.h']))
      self.assertEqual(set(['hpp', 'h']), cpplint._hpp_headers)
      self.assertEqual(set(['hpp', 'h', 'cpp']), cpplint._valid_extensions)
      
    finally:
      cpplint._USAGE = old_usage
      cpplint._ERROR_CATEGORIES = old_error_categories
      cpplint._cpplint_state.output_format = old_output_format
      cpplint._cpplint_state.verbose_level = old_verbose_level
      cpplint._cpplint_state.filters = old_filters
      cpplint._line_length = old_line_length
      cpplint._valid_extensions = old_valid_extensions
      cpplint._hpp_headers = old_headers

  def testLineLength(self):
    old_line_length = cpplint._line_length
    try:
      cpplint._line_length = 80
      self.TestLint(
          '// H %s' % ('H' * 75),
          '')
      self.TestLint(
          '// H %s' % ('H' * 76),
          'Lines should be <= 80 characters long'
          '  [whitespace/line_length] [2]')
      cpplint._line_length = 120
      self.TestLint(
          '// H %s' % ('H' * 115),
          '')
      self.TestLint(
          '// H %s' % ('H' * 116),
          'Lines should be <= 120 characters long'
          '  [whitespace/line_length] [2]')
    finally:
      cpplint._line_length = old_line_length

  def testFilter(self):
    old_filters = cpplint._cpplint_state.filters
    try:
      cpplint._cpplint_state.SetFilters('-,+whitespace,-whitespace/indent')
      self.TestLint(
          '// Hello there ',
          'Line ends in whitespace.  Consider deleting these extra spaces.'
          '  [whitespace/end_of_line] [4]')
      self.TestLint('int a = (int)1.0;', '')
      self.TestLint(' weird opening space', '')
    finally:
      cpplint._cpplint_state.filters = old_filters

  def testDefaultFilter(self):
    default_filters = cpplint._DEFAULT_FILTERS
    old_filters = cpplint._cpplint_state.filters
    cpplint._DEFAULT_FILTERS = ['-whitespace']
    try:
      # Reset filters
      cpplint._cpplint_state.SetFilters('')
      self.TestLint('// Hello there ', '')
      cpplint._cpplint_state.SetFilters('+whitespace/end_of_line')
      self.TestLint(
          '// Hello there ',
          'Line ends in whitespace.  Consider deleting these extra spaces.'
          '  [whitespace/end_of_line] [4]')
      self.TestLint(' weird opening space', '')
    finally:
      cpplint._cpplint_state.filters = old_filters
      cpplint._DEFAULT_FILTERS = default_filters

  def testDuplicateHeader(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('path/self.cc', 'cc',
                            ['// Copyright 2014 Your Company. All Rights Reserved.',
                             '#include "path/self.h"',
                             '#include "path/duplicate.h"',
                             '#include "path/duplicate.h"',
                             '#ifdef MACRO',
                             '#include "path/unique.h"',
                             '#else',
                             '#include "path/unique.h"',
                             '#endif',
                             ''],
                            error_collector)
    self.assertEquals(
        ['"path/duplicate.h" already included at path/self.cc:3  '
         '[build/include] [4]'],
        error_collector.ResultList())

  def testUnnamedNamespacesInHeaders(self):
    self.TestLanguageRulesCheck(
        'foo.h', 'namespace {',
        'Do not use unnamed namespaces in header files.  See'
        ' https://google-styleguide.googlecode.com/svn/trunk/cppguide.xml#Namespaces'
        ' for more information.  [build/namespaces] [4]')
    # namespace registration macros are OK.
    self.TestLanguageRulesCheck('foo.h', 'namespace {  \\', '')
    # named namespaces are OK.
    self.TestLanguageRulesCheck('foo.h', 'namespace foo {', '')
    self.TestLanguageRulesCheck('foo.h', 'namespace foonamespace {', '')
    self.TestLanguageRulesCheck('foo.cc', 'namespace {', '')
    self.TestLanguageRulesCheck('foo.cc', 'namespace foo {', '')

  def testBuildClass(self):
    # Test that the linter can parse to the end of class definitions,
    # and that it will report when it can't.
    # Use multi-line linter because it performs the ClassState check.
    self.TestMultiLineLint(
        'class Foo {',
        'Failed to find complete declaration of class Foo'
        '  [build/class] [5]')
    # Do the same for namespaces
    self.TestMultiLineLint(
        'namespace Foo {',
        'Failed to find complete declaration of namespace Foo'
        '  [build/namespaces] [5]')
    # Don't warn on forward declarations of various types.
    self.TestMultiLineLint(
        'class Foo;',
        '')
    self.TestMultiLineLint(
        """struct Foo*
             foo = NewFoo();""",
        '')
    # Test preprocessor.
    self.TestMultiLineLint(
        """#ifdef DERIVE_FROM_GOO
          struct Foo : public Goo {
        #else
          struct Foo : public Hoo {
        #endif
          };""",
        '')
    self.TestMultiLineLint(
        """
        class Foo
        #ifdef DERIVE_FROM_GOO
          : public Goo {
        #else
          : public Hoo {
        #endif
        };""",
        '')
    # Test incomplete class
    self.TestMultiLineLint(
        'class Foo {',
        'Failed to find complete declaration of class Foo'
        '  [build/class] [5]')

  def testBuildEndComment(self):
    # The crosstool compiler we currently use will fail to compile the
    # code in this test, so we might consider removing the lint check.
    self.TestMultiLineLint(
        """#if 0
        #endif Not a comment""",
        'Uncommented text after #endif is non-standard.  Use a comment.'
        '  [build/endif_comment] [5]')

  def testBuildForwardDecl(self):
    # The crosstool compiler we currently use will fail to compile the
    # code in this test, so we might consider removing the lint check.
    self.TestLint('class Foo::Goo;',
                  'Inner-style forward declarations are invalid.'
                  '  Remove this line.'
                  '  [build/forward_decl] [5]')

  def GetBuildHeaderGuardPreprocessorSymbol(self, file_path):
    # Figure out the expected header guard by processing an empty file.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h', [], error_collector)
    for error in error_collector.ResultList():
      matched = re.search(
          'No #ifndef header guard found, suggested CPP variable is: '
          '([A-Z0-9_]+)',
          error)
      if matched is not None:
        return matched.group(1)

  def testBuildHeaderGuard(self):
    file_path = 'mydir/foo.h'
    expected_guard = self.GetBuildHeaderGuardPreprocessorSymbol(file_path)
    self.assertTrue(re.search('MYDIR_FOO_H_$', expected_guard))

    # No guard at all: expect one error.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h', [], error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            'No #ifndef header guard found, suggested CPP variable is: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # No header guard, but the error is suppressed.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['// Copyright 2014 Your Company.',
                             '// NOLINT(build/header_guard)', ''],
                            error_collector)
    self.assertEquals([], error_collector.ResultList())

    # Wrong guard
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef FOO_H', '#define FOO_H'], error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            '#ifndef header guard has wrong style, please use: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # No define
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s' % expected_guard], error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            'No #ifndef header guard found, suggested CPP variable is: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # Mismatched define
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s' % expected_guard,
                             '#define FOO_H'],
                            error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            'No #ifndef header guard found, suggested CPP variable is: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # No endif
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s' % expected_guard,
                             '#define %s' % expected_guard,
                             ''],
                            error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            '#endif line should be "#endif  // %s"'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # Commentless endif
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s' % expected_guard,
                             '#define %s' % expected_guard,
                             '#endif'],
                            error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            '#endif line should be "#endif  // %s"'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # Commentless endif for old-style guard
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s_' % expected_guard,
                             '#define %s_' % expected_guard,
                             '#endif'],
                            error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            '#endif line should be "#endif  // %s"'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # No header guard errors
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s' % expected_guard,
                             '#define %s' % expected_guard,
                             '#endif  // %s' % expected_guard],
                            error_collector)
    for line in error_collector.ResultList():
      if line.find('build/header_guard') != -1:
        self.fail('Unexpected error: %s' % line)

    # No header guard errors for old-style guard
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s_' % expected_guard,
                             '#define %s_' % expected_guard,
                             '#endif  // %s_' % expected_guard],
                            error_collector)
    for line in error_collector.ResultList():
      if line.find('build/header_guard') != -1:
        self.fail('Unexpected error: %s' % line)

    old_verbose_level = cpplint._cpplint_state.verbose_level
    try:
      cpplint._cpplint_state.verbose_level = 0
      # Warn on old-style guard if verbosity is 0.
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData(file_path, 'h',
                              ['#ifndef %s_' % expected_guard,
                               '#define %s_' % expected_guard,
                               '#endif  // %s_' % expected_guard],
                              error_collector)
      self.assertEquals(
          1,
          error_collector.ResultList().count(
              '#ifndef header guard has wrong style, please use: %s'
              '  [build/header_guard] [0]' % expected_guard),
          error_collector.ResultList())
    finally:
      cpplint._cpplint_state.verbose_level = old_verbose_level

    # Completely incorrect header guard
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef FOO',
                             '#define FOO',
                             '#endif  // FOO'],
                            error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            '#ifndef header guard has wrong style, please use: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            '#endif line should be "#endif  // %s"'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # incorrect header guard with nolint
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef FOO  // NOLINT',
                             '#define FOO',
                             '#endif  // FOO NOLINT'],
                            error_collector)
    self.assertEquals(
        0,
        error_collector.ResultList().count(
            '#ifndef header guard has wrong style, please use: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())
    self.assertEquals(
        0,
        error_collector.ResultList().count(
            '#endif line should be "#endif  // %s"'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # Special case for flymake
    for test_file in ['mydir/foo_flymake.h', 'mydir/.flymake/foo.h']:
      error_collector = ErrorCollector(self.assert_)
      cpplint.ProcessFileData(test_file, 'h',
                              ['// Copyright 2014 Your Company.', ''],
                              error_collector)
      self.assertEquals(
          1,
          error_collector.ResultList().count(
              'No #ifndef header guard found, suggested CPP variable is: %s'
              '  [build/header_guard] [5]' % expected_guard),
          error_collector.ResultList())

  def testBuildHeaderGuardWithRoot(self):
    # note: Tested file paths must be real, otherwise
    # the repository name lookup will fail.
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'cpplint_test_header.h')
    file_info = cpplint.FileInfo(file_path)
    if file_info.FullName() == file_info.RepositoryName():
      # When FileInfo cannot deduce the root directory of the repository,
      # FileInfo.RepositoryName returns the same value as FileInfo.FullName.
      # This can happen when this source file was obtained without .svn or
      # .git directory. (e.g. using 'svn export' or 'git archive').
      # Skip this test in such a case because --root flag makes sense only
      # when the root directory of the repository is properly deduced.
      return

    self.assertEquals('CPPLINT_CPPLINT_TEST_HEADER_H_',
                      cpplint.GetHeaderGuardCPPVariable(file_path))
    #
    # test --root flags:
    #   this changes the cpp header guard prefix
    #

    # left-strip the header guard by using a root dir inside of the repo dir.
    # relative directory
    cpplint._root = 'cpplint'
    self.assertEquals('CPPLINT_TEST_HEADER_H_',
                      cpplint.GetHeaderGuardCPPVariable(file_path))

    nested_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.path.join('nested',
                                                 'cpplint_test_header.h'))
    cpplint._root = os.path.join('cpplint', 'nested')
    actual = cpplint.GetHeaderGuardCPPVariable(nested_file_path)
    self.assertEquals('CPPLINT_TEST_HEADER_H_',
                      actual)

    # absolute directory
    # (note that CPPLINT.cfg root=setting is always made absolute)
    cpplint._root = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    self.assertEquals('CPPLINT_TEST_HEADER_H_',
                      cpplint.GetHeaderGuardCPPVariable(file_path))

    nested_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.path.join('nested',
                                                 'cpplint_test_header.h'))
    cpplint._root = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'nested')
    self.assertEquals('CPPLINT_TEST_HEADER_H_',
                      cpplint.GetHeaderGuardCPPVariable(nested_file_path))

    # --root flag is ignored if an non-existent directory is specified.
    cpplint._root = 'NON_EXISTENT_DIR'
    self.assertEquals('CPPLINT_CPPLINT_TEST_HEADER_H_',
                      cpplint.GetHeaderGuardCPPVariable(file_path))

    # prepend to the header guard by using a root dir that is more outer
    # than the repo dir

    # (using absolute paths)
    # (note that CPPLINT.cfg root=setting is always made absolute)
    this_files_path = os.path.dirname(os.path.abspath(__file__))
    (styleguide_path, this_files_dir) = os.path.split(this_files_path)
    (styleguide_parent_path, styleguide_dir_name) = os.path.split(styleguide_path)
    # parent dir of styleguide
    cpplint._root = styleguide_parent_path
    self.assertIsNotNone(styleguide_parent_path)
    # do not hardcode the 'styleguide' repository name, it could be anything.
    expected_prefix = re.sub(r'[^a-zA-Z0-9]', '_', styleguide_dir_name).upper() + '_'
    # do not have 'styleguide' repo in '/'
    self.assertEquals('%sCPPLINT_CPPLINT_TEST_HEADER_H_' %(expected_prefix),
                      cpplint.GetHeaderGuardCPPVariable(file_path))

    # To run the 'relative path' tests, we must be in the directory of this test file.
    cur_dir = os.getcwd()
    os.chdir(this_files_path)

    # (using relative paths)
    styleguide_rel_path = os.path.relpath(styleguide_path, this_files_path)
    # '..'
    cpplint._root = styleguide_rel_path
    self.assertEquals('CPPLINT_CPPLINT_TEST_HEADER_H_',
                      cpplint.GetHeaderGuardCPPVariable(file_path))

    styleguide_rel_path = os.path.relpath(styleguide_parent_path,
                                          this_files_path) # '../..'
    cpplint._root = styleguide_rel_path
    self.assertEquals('%sCPPLINT_CPPLINT_TEST_HEADER_H_' %(expected_prefix),
                      cpplint.GetHeaderGuardCPPVariable(file_path))

    cpplint._root = None

    # Restore previous CWD.
    os.chdir(cur_dir)

  def testPathSplitToList(self):
    self.assertEquals([''],
                      cpplint.PathSplitToList(os.path.join('')))

    self.assertEquals(['.'],
                      cpplint.PathSplitToList(os.path.join('.')))

    self.assertEquals(['..'],
                      cpplint.PathSplitToList(os.path.join('..')))

    self.assertEquals(['..', 'a', 'b'],
                      cpplint.PathSplitToList(os.path.join('..', 'a', 'b')))

    self.assertEquals(['a', 'b', 'c', 'd'],
                      cpplint.PathSplitToList(os.path.join('a', 'b', 'c', 'd')))

  def testBuildInclude(self):
    # Test that include statements have slashes in them.
    self.TestLint('#include "foo.h"',
                  'Include the directory when naming .h files'
                  '  [build/include] [4]')
    self.TestLint('#include "Python.h"', '')
    self.TestLint('#include "lua.h"', '')

  def testBuildPrintfFormat(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'foo.cc', 'cc',
        [r'printf("\%%d", value);',
         r'snprintf(buffer, sizeof(buffer), "\[%d", value);',
         r'fprintf(file, "\(%d", value);',
         r'vsnprintf(buffer, sizeof(buffer), "\\\{%d", ap);'],
        error_collector)
    self.assertEquals(
        4,
        error_collector.Results().count(
            '%, [, (, and { are undefined character escapes.  Unescape them.'
            '  [build/printf_format] [3]'))

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        'foo.cc', 'cc',
        ['// Copyright 2014 Your Company.',
         r'printf("\\%%%d", value);',
         r'printf(R"(\[)");',
         r'printf(R"(\[%s)", R"(\])");',
         ''],
        error_collector)
    self.assertEquals('', error_collector.Results())

  def testRuntimePrintfFormat(self):
    self.TestLint(
        r'fprintf(file, "%q", value);',
        '%q in format strings is deprecated.  Use %ll instead.'
        '  [runtime/printf_format] [3]')

    self.TestLint(
        r'aprintf(file, "The number is %12q", value);',
        '%q in format strings is deprecated.  Use %ll instead.'
        '  [runtime/printf_format] [3]')

    self.TestLint(
        r'printf(file, "The number is" "%-12q", value);',
        '%q in format strings is deprecated.  Use %ll instead.'
        '  [runtime/printf_format] [3]')

    self.TestLint(
        r'printf(file, "The number is" "%+12q", value);',
        '%q in format strings is deprecated.  Use %ll instead.'
        '  [runtime/printf_format] [3]')

    self.TestLint(
        r'printf(file, "The number is" "% 12q", value);',
        '%q in format strings is deprecated.  Use %ll instead.'
        '  [runtime/printf_format] [3]')

    self.TestLint(
        r'snprintf(file, "Never mix %d and %1$d parameters!", value);',
        '%N$ formats are unconventional.  Try rewriting to avoid them.'
        '  [runtime/printf_format] [2]')

  def TestLintLogCodeOnError(self, code, expected_message):
    # Special TestLint which logs the input code on error.
    result = self.PerformSingleLineLint(code)
    if result != expected_message:
      self.fail('For code: "%s"\nGot: "%s"\nExpected: "%s"'
                % (code, result, expected_message))

  def testBuildStorageClass(self):
    qualifiers = [None, 'const', 'volatile']
    signs = [None, 'signed', 'unsigned']
    types = ['void', 'char', 'int', 'float', 'double',
             'schar', 'int8', 'uint8', 'int16', 'uint16',
             'int32', 'uint32', 'int64', 'uint64']
    storage_classes = ['extern', 'register', 'static', 'typedef']

    build_storage_class_error_message = (
        'Storage-class specifier (static, extern, typedef, etc) should be '
        'at the beginning of the declaration.  [build/storage_class] [5]')

    # Some explicit cases. Legal in C++, deprecated in C99.
    self.TestLint('const int static foo = 5;',
                  build_storage_class_error_message)

    self.TestLint('char static foo;',
                  build_storage_class_error_message)

    self.TestLint('double const static foo = 2.0;',
                  build_storage_class_error_message)

    self.TestLint('uint64 typedef unsigned_long_long;',
                  build_storage_class_error_message)

    self.TestLint('int register foo = 0;',
                  build_storage_class_error_message)

    # Since there are a very large number of possibilities, randomly
    # construct declarations.
    # Make sure that the declaration is logged if there's an error.
    # Seed generator with an integer for absolute reproducibility.
    random.seed(25)
    for unused_i in range(10):
      # Build up random list of non-storage-class declaration specs.
      other_decl_specs = [random.choice(qualifiers), random.choice(signs),
                          random.choice(types)]
      # remove None
      other_decl_specs = [x for x in other_decl_specs if x is not None]

      # shuffle
      random.shuffle(other_decl_specs)

      # insert storage class after the first
      storage_class = random.choice(storage_classes)
      insertion_point = random.randint(1, len(other_decl_specs))
      decl_specs = (other_decl_specs[0:insertion_point]
                    + [storage_class]
                    + other_decl_specs[insertion_point:])

      self.TestLintLogCodeOnError(
          ' '.join(decl_specs) + ';',
          build_storage_class_error_message)

      # but no error if storage class is first
      self.TestLintLogCodeOnError(
          storage_class + ' ' + ' '.join(other_decl_specs),
          '')

  def testLegalCopyright(self):
    legal_copyright_message = (
        'No copyright message found.  '
        'You should have a line: "Copyright [year] <Copyright Owner>"'
        '  [legal/copyright] [5]')

    copyright_line = '// Copyright 2014 Google Inc. All Rights Reserved.'

    file_path = 'mydir/googleclient/foo.cc'

    # There should be a copyright message in the first 10 lines
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'cc', [], error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(legal_copyright_message))

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        file_path, 'cc',
        ['' for unused_i in range(10)] + [copyright_line],
        error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(legal_copyright_message))

    # Test that warning isn't issued if Copyright line appears early enough.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'cc', [copyright_line], error_collector)
    for message in error_collector.ResultList():
      if message.find('legal/copyright') != -1:
        self.fail('Unexpected error: %s' % message)

    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(
        file_path, 'cc',
        ['' for unused_i in range(9)] + [copyright_line],
        error_collector)
    for message in error_collector.ResultList():
      if message.find('legal/copyright') != -1:
        self.fail('Unexpected error: %s' % message)

  def testInvalidIncrement(self):
    self.TestLint('*count++;',
                  'Changing pointer instead of value (or unused value of '
                  'operator*).  [runtime/invalid_increment] [5]')

  def testSnprintfSize(self):
    self.TestLint('vsnprintf(NULL, 0, format)', '')
    self.TestLint('snprintf(fisk, 1, format)',
                  'If you can, use sizeof(fisk) instead of 1 as the 2nd arg '
                  'to snprintf.  [runtime/printf] [3]')
class Cxx11Test(CpplintTestBase):

  def Helper(self, package, extension, lines, count):
    filename = package + '/foo.' + extension
    lines = lines[:]

    # Header files need to have an ifdef guard wrapped around their code.
    if extension == 'h':
      guard = filename.upper().replace('/', '_').replace('.', '_') + '_'
      lines.insert(0, '#ifndef ' + guard)
      lines.insert(1, '#define ' + guard)
      lines.append('#endif  // ' + guard)

    # All files need a final blank line.
    lines.append('')

    # Process the file and check resulting error count.
    collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(filename, extension, lines, collector)
    error_list = collector.ResultList()
    self.assertEquals(count, len(error_list), error_list)

  def TestCxx11Feature(self, code, expected_error):
    lines = code.split('\n')
    collector = ErrorCollector(self.assert_)
    cpplint.RemoveMultiLineComments('foo.h', lines, collector)
    clean_lines = cpplint.CleansedLines(lines)
    cpplint.FlagCxx11Features('foo.cc', clean_lines, 0, collector)
    self.assertEquals(expected_error, collector.Results())

  def testBlockedHeaders(self):
    self.TestCxx11Feature('#include <tr1/regex>',
                          'C++ TR1 headers such as <tr1/regex> are '
                          'unapproved.  [build/c++tr1] [5]')
    self.TestCxx11Feature('#include <mutex>',
                          '<mutex> is an unapproved C++11 header.'
                          '  [build/c++11] [5]')

  def testBlockedClasses(self):
    self.TestCxx11Feature('std::alignment_of<T>',
                          'std::alignment_of is an unapproved '
                          'C++11 class or function.  Send c-style an example '
                          'of where it would make your code more readable, '
                          'and they may let you use it.'
                          '  [build/c++11] [5]')
    self.TestCxx11Feature('std::alignment_offer', '')
    self.TestCxx11Feature('mystd::alignment_of', '')
    self.TestCxx11Feature('std::binomial_distribution', '')

  def testBlockedFunctions(self):
    self.TestCxx11Feature('std::alignment_of<int>',
                          'std::alignment_of is an unapproved '
                          'C++11 class or function.  Send c-style an example '
                          'of where it would make your code more readable, '
                          'and they may let you use it.'
                          '  [build/c++11] [5]')
    # Missed because of the lack of "std::".  Compiles because ADL
    # looks in the namespace of my_shared_ptr, which (presumably) is
    # std::.  But there will be a lint error somewhere in this file
    # since my_shared_ptr had to be defined.
    self.TestCxx11Feature('static_pointer_cast<Base>(my_shared_ptr)', '')
    self.TestCxx11Feature('std::declval<T>()', '')

  def testExplicitMakePair(self):
    self.TestLint('make_pair', '')
    self.TestLint('make_pair(42, 42)', '')
    self.TestLint('make_pair<',
                  'For C++11-compatibility, omit template arguments from'
                  ' make_pair OR use pair directly OR if appropriate,'
                  ' construct a pair directly'
                  '  [build/explicit_make_pair] [4]')
    self.TestLint('make_pair <',
                  'For C++11-compatibility, omit template arguments from'
                  ' make_pair OR use pair directly OR if appropriate,'
                  ' construct a pair directly'
                  '  [build/explicit_make_pair] [4]')
    self.TestLint('my_make_pair<int, int>', '')

class Cxx14Test(CpplintTestBase):

  def TestCxx14Feature(self, code, expected_error):
    lines = code.split('\n')
    collector = ErrorCollector(self.assert_)
    cpplint.RemoveMultiLineComments('foo.h', lines, collector)
    clean_lines = cpplint.CleansedLines(lines)
    cpplint.FlagCxx14Features('foo.cc', clean_lines, 0, collector)
    self.assertEquals(expected_error, collector.Results())

  def testBlockedHeaders(self):
    self.TestCxx14Feature('#include <scoped_allocator>',
                          '<scoped_allocator> is an unapproved C++14 header.'
                           '  [build/c++14] [5]')
    self.TestCxx14Feature('#include <shared_mutex>',
                          '<shared_mutex> is an unapproved C++14 header.'
                          '  [build/c++14] [5]')


class CleansedLinesTest(unittest.TestCase):

  def testInit(self):
    lines = ['Line 1',
             'Line 2',
             'Line 3 // Comment test',
             'Line 4 /* Comment test */',
             'Line 5 "foo"']

    clean_lines = cpplint.CleansedLines(lines)
    self.assertEquals(lines, clean_lines.raw_lines)
    self.assertEquals(5, clean_lines.NumLines())

    self.assertEquals(['Line 1',
                       'Line 2',
                       'Line 3',
                       'Line 4',
                       'Line 5 "foo"'],
                      clean_lines.lines)

    self.assertEquals(['Line 1',
                       'Line 2',
                       'Line 3',
                       'Line 4',
                       'Line 5 ""'],
                      clean_lines.elided)

  def testInitEmpty(self):
    clean_lines = cpplint.CleansedLines([])
    self.assertEquals([], clean_lines.raw_lines)
    self.assertEquals(0, clean_lines.NumLines())

  def testCollapseStrings(self):
    collapse = cpplint.CleansedLines._CollapseStrings
    self.assertEquals('""', collapse('""'))             # ""     (empty)
    self.assertEquals('"""', collapse('"""'))           # """    (bad)
    self.assertEquals('""', collapse('"xyz"'))          # "xyz"  (string)
    self.assertEquals('""', collapse('"\\\""'))         # "\""   (string)
    self.assertEquals('""', collapse('"\'"'))           # "'"    (string)
    self.assertEquals('"\"', collapse('"\"'))           # "\"    (bad)
    self.assertEquals('""', collapse('"\\\\"'))         # "\\"   (string)
    self.assertEquals('"', collapse('"\\\\\\"'))        # "\\\"  (bad)
    self.assertEquals('""', collapse('"\\\\\\\\"'))     # "\\\\" (string)

    self.assertEquals('\'\'', collapse('\'\''))         # ''     (empty)
    self.assertEquals('\'\'', collapse('\'a\''))        # 'a'    (char)
    self.assertEquals('\'\'', collapse('\'\\\'\''))     # '\''   (char)
    self.assertEquals('\'', collapse('\'\\\''))         # '\'    (bad)
    self.assertEquals('', collapse('\\012'))            # '\012' (char)
    self.assertEquals('', collapse('\\xfF0'))           # '\xfF0' (char)
    self.assertEquals('', collapse('\\n'))              # '\n' (char)
    self.assertEquals(r'\#', collapse('\\#'))           # '\#' (bad)

    self.assertEquals('"" + ""', collapse('"\'" + "\'"'))
    self.assertEquals("'', ''", collapse("'\"', '\"'"))
    self.assertEquals('""[0b10]', collapse('"a\'b"[0b1\'0]'))

    self.assertEquals('42', collapse("4'2"))
    self.assertEquals('0b0101', collapse("0b0'1'0'1"))
    self.assertEquals('1048576', collapse("1'048'576"))
    self.assertEquals('0X100000', collapse("0X10'0000"))
    self.assertEquals('0004000000', collapse("0'004'000'000"))
    self.assertEquals('1.602176565e-19', collapse("1.602'176'565e-19"))
    self.assertEquals('\'\' + 0xffff', collapse("'i' + 0xf'f'f'f"))
    self.assertEquals('sizeof\'\' == 1', collapse("sizeof'x' == 1"))
    self.assertEquals('0x.03p100', collapse('0x.0\'3p1\'0\'0'))
    self.assertEquals('123.45', collapse('1\'23.4\'5'))

    self.assertEquals('StringReplace(body, "", "");',
                      collapse('StringReplace(body, "\\\\", "\\\\\\\\");'))
    self.assertEquals('\'\' ""',
                      collapse('\'"\' "foo"'))


class OrderOfIncludesTest(CpplintTestBase):

  def setUp(self):
    CpplintTestBase.setUp(self)
    self.include_state = cpplint._IncludeState()
    os.path.abspath = lambda value: value

  def testCheckNextIncludeOrder_OtherThenCpp(self):
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._OTHER_HEADER))
    self.assertEqual('Found C++ system header after other header',
                     self.include_state.CheckNextIncludeOrder(
                         cpplint._CPP_SYS_HEADER))

  def testCheckNextIncludeOrder_CppThenC(self):
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._CPP_SYS_HEADER))
    self.assertEqual('Found C system header after C++ system header',
                     self.include_state.CheckNextIncludeOrder(
                         cpplint._C_SYS_HEADER))

  def testCheckNextIncludeOrder_LikelyThenCpp(self):
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._LIKELY_MY_HEADER))
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._CPP_SYS_HEADER))

  def testCheckNextIncludeOrder_PossibleThenCpp(self):
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._POSSIBLE_MY_HEADER))
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._CPP_SYS_HEADER))

  def testCheckNextIncludeOrder_CppThenLikely(self):
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._CPP_SYS_HEADER))
    # This will eventually fail.
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._LIKELY_MY_HEADER))

  def testCheckNextIncludeOrder_CppThenPossible(self):
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._CPP_SYS_HEADER))
    self.assertEqual('', self.include_state.CheckNextIncludeOrder(
        cpplint._POSSIBLE_MY_HEADER))

  def testClassifyInclude(self):
    file_info = cpplint.FileInfo
    classify_include = cpplint._ClassifyInclude
    self.assertEqual(cpplint._C_SYS_HEADER,
                     classify_include(file_info('foo/foo.cc'),
                                      'stdio.h',
                                      True))
    self.assertEqual(cpplint._CPP_SYS_HEADER,
                     classify_include(file_info('foo/foo.cc'),
                                      'string',
                                      True))
    self.assertEqual(cpplint._CPP_SYS_HEADER,
                     classify_include(file_info('foo/foo.cc'),
                                      'typeinfo',
                                      True))
    self.assertEqual(cpplint._OTHER_HEADER,
                     classify_include(file_info('foo/foo.cc'),
                                      'string',
                                      False))

    self.assertEqual(cpplint._LIKELY_MY_HEADER,
                     classify_include(file_info('foo/foo.cc'),
                                      'foo/foo-inl.h',
                                      False))
    self.assertEqual(cpplint._LIKELY_MY_HEADER,
                     classify_include(file_info('foo/internal/foo.cc'),
                                      'foo/public/foo.h',
                                      False))
    self.assertEqual(cpplint._POSSIBLE_MY_HEADER,
                     classify_include(file_info('foo/internal/foo.cc'),
                                      'foo/other/public/foo.h',
                                      False))
    self.assertEqual(cpplint._OTHER_HEADER,
                     classify_include(file_info('foo/internal/foo.cc'),
                                      'foo/other/public/foop.h',
                                      False))

  def testTryDropCommonSuffixes(self):
    self.assertEqual('foo/foo', cpplint._DropCommonSuffixes('foo/foo-inl.h'))
    self.assertEqual('foo/bar/foo',
                     cpplint._DropCommonSuffixes('foo/bar/foo_inl.h'))
    self.assertEqual('foo/foo', cpplint._DropCommonSuffixes('foo/foo.cc'))
    self.assertEqual('foo/foo_unusualinternal',
                     cpplint._DropCommonSuffixes('foo/foo_unusualinternal.h'))
    self.assertEqual('',
                     cpplint._DropCommonSuffixes('_test.cc'))
    self.assertEqual('test',
                     cpplint._DropCommonSuffixes('test.cc'))

  def testRegression(self):
    def Format(includes):
      include_list = []
      for item in includes:
        if item.startswith('"') or item.startswith('<'):
          include_list.append('#include %s\n' % item)
        else:
          include_list.append(item + '\n')
      return ''.join(include_list)

    # Test singleton cases first.
    self.TestLanguageRulesCheck('foo/foo.cc', Format(['"foo/foo.h"']), '')
    self.TestLanguageRulesCheck('foo/foo.cc', Format(['<stdio.h>']), '')
    self.TestLanguageRulesCheck('foo/foo.cc', Format(['<string>']), '')
    self.TestLanguageRulesCheck('foo/foo.cc', Format(['"foo/foo-inl.h"']), '')
    self.TestLanguageRulesCheck('foo/foo.cc', Format(['"bar/bar-inl.h"']), '')
    self.TestLanguageRulesCheck('foo/foo.cc', Format(['"bar/bar.h"']), '')

    # Test everything in a good and new order.
    self.TestLanguageRulesCheck('foo/foo.cc',
                                Format(['"foo/foo.h"',
                                        '"foo/foo-inl.h"',
                                        '<stdio.h>',
                                        '<string>',
                                        '<unordered_map>',
                                        '"bar/bar-inl.h"',
                                        '"bar/bar.h"']),
                                '')

    # Test bad orders.
    self.TestLanguageRulesCheck(
        'foo/foo.cc',
        Format(['<string>', '<stdio.h>']),
        'Found C system header after C++ system header.'
        ' Should be: foo.h, c system, c++ system, other.'
        '  [build/include_order] [4]')
    self.TestLanguageRulesCheck(
        'foo/foo.cc',
        Format(['"foo/bar-inl.h"',
                '"foo/foo-inl.h"']),
        '')
    self.TestLanguageRulesCheck(
        'foo/foo.cc',
        Format(['"foo/e.h"',
                '"foo/b.h"',  # warning here (e>b)
                '"foo/c.h"',
                '"foo/d.h"',
                '"foo/a.h"']),  # warning here (d>a)
        ['Include "foo/b.h" not in alphabetical order'
         '  [build/include_alpha] [4]',
         'Include "foo/a.h" not in alphabetical order'
         '  [build/include_alpha] [4]'])
    # -inl.h headers are no longer special.
    self.TestLanguageRulesCheck('foo/foo.cc',
                                Format(['"foo/foo-inl.h"', '<string>']),
                                '')
    self.TestLanguageRulesCheck('foo/foo.cc',
                                Format(['"foo/bar.h"', '"foo/bar-inl.h"']),
                                '')
    # Test componentized header.  OK to have my header in ../public dir.
    self.TestLanguageRulesCheck('foo/internal/foo.cc',
                                Format(['"foo/public/foo.h"', '<string>']),
                                '')
    # OK to have my header in other dir (not stylistically, but
    # cpplint isn't as good as a human).
    self.TestLanguageRulesCheck('foo/internal/foo.cc',
                                Format(['"foo/other/public/foo.h"',
                                        '<string>']),
                                '')
    self.TestLanguageRulesCheck('foo/foo.cc',
                                Format(['"foo/foo.h"',
                                        '<string>',
                                        '"base/google.h"',
                                        '"base/flags.h"']),
                                'Include "base/flags.h" not in alphabetical '
                                'order  [build/include_alpha] [4]')
    # According to the style, -inl.h should come before .h, but we don't
    # complain about that.
    self.TestLanguageRulesCheck('foo/foo.cc',
                                Format(['"foo/foo-inl.h"',
                                        '"foo/foo.h"',
                                        '"base/google.h"',
                                        '"base/google-inl.h"']),
                                '')
    # Allow project includes to be separated by blank lines
    self.TestLanguageRulesCheck('a/a.cc',
                                Format(['"a/a.h"',
                                        '<string>',
                                        '"base/google.h"',
                                        '',
                                        '"b/c.h"',
                                        '',
                                        'MACRO',
                                        '"a/b.h"']),
                                '')
    self.TestLanguageRulesCheck('a/a.cc',
                                Format(['"a/a.h"',
                                        '<string>',
                                        '"base/google.h"',
                                        '"a/b.h"']),
                                'Include "a/b.h" not in alphabetical '
                                'order  [build/include_alpha] [4]')

    # Test conditional includes
    self.TestLanguageRulesCheck(
        'a/a.cc',
        ''.join(['#include <string.h>\n',
                 '#include "base/port.h"\n',
                 '#include <initializer_list>\n']),
        ('Found C++ system header after other header. '
         'Should be: a.h, c system, c++ system, other.  '
         '[build/include_order] [4]'))
    self.TestLanguageRulesCheck(
        'a/a.cc',
        ''.join(['#include <string.h>\n',
                 '#include "base/port.h"\n',
                 '#ifdef LANG_CXX11\n',
                 '#include <initializer_list>\n',
                 '#endif  // LANG_CXX11\n']),
        '')
    self.TestLanguageRulesCheck(
        'a/a.cc',
        ''.join(['#include <string.h>\n',
                 '#ifdef LANG_CXX11\n',
                 '#include "base/port.h"\n',
                 '#include <initializer_list>\n',
                 '#endif  // LANG_CXX11\n']),
        ('Found C++ system header after other header. '
         'Should be: a.h, c system, c++ system, other.  '
         '[build/include_order] [4]'))

    # Third party headers are exempt from order checks
    self.TestLanguageRulesCheck('foo/foo.cc',
                                Format(['<string>', '"Python.h"', '<vector>']),
                                '')


class CheckForFunctionLengthsTest(CpplintTestBase):

  def setUp(self):
    # Reducing these thresholds for the tests speeds up tests significantly.
    self.old_normal_trigger = cpplint._FunctionState._NORMAL_TRIGGER
    self.old_test_trigger = cpplint._FunctionState._TEST_TRIGGER

    cpplint._FunctionState._NORMAL_TRIGGER = 10
    cpplint._FunctionState._TEST_TRIGGER = 25

  def tearDown(self):
    cpplint._FunctionState._NORMAL_TRIGGER = self.old_normal_trigger
    cpplint._FunctionState._TEST_TRIGGER = self.old_test_trigger

  def TestFunctionLengthsCheck(self, code, expected_message):
    """Check warnings for long function bodies are as expected.

    Args:
      code: C++ source code expected to generate a warning message.
      expected_message: Message expected to be generated by the C++ code.
    """
    self.assertEquals(expected_message,
                      self.PerformFunctionLengthsCheck(code))

  def TriggerLines(self, error_level):
    """Return number of lines needed to trigger a function length warning.

    Args:
      error_level: --v setting for cpplint.

    Returns:
      Number of lines needed to trigger a function length warning.
    """
    return cpplint._FunctionState._NORMAL_TRIGGER * 2**error_level

  def TestLines(self, error_level):
    """Return number of lines needed to trigger a test function length warning.

    Args:
      error_level: --v setting for cpplint.

    Returns:
      Number of lines needed to trigger a test function length warning.
    """
    return cpplint._FunctionState._TEST_TRIGGER * 2**error_level

  def TestFunctionLengthCheckDefinition(self, lines, error_level):
    """Generate long function definition and check warnings are as expected.

    Args:
      lines: Number of lines to generate.
      error_level:  --v setting for cpplint.
    """
    trigger_level = self.TriggerLines(cpplint._VerboseLevel())
    self.TestFunctionLengthsCheck(
        'void test(int x)' + self.FunctionBody(lines),
        ('Small and focused functions are preferred: '
         'test() has %d non-comment lines '
         '(error triggered by exceeding %d lines).'
         '  [readability/fn_size] [%d]'
         % (lines, trigger_level, error_level)))

  def TestFunctionLengthCheckDefinitionOK(self, lines):
    """Generate shorter function definition and check no warning is produced.

    Args:
      lines: Number of lines to generate.
    """
    self.TestFunctionLengthsCheck(
        'void test(int x)' + self.FunctionBody(lines),
        '')

  def TestFunctionLengthCheckAtErrorLevel(self, error_level):
    """Generate and check function at the trigger level for --v setting.

    Args:
      error_level: --v setting for cpplint.
    """
    self.TestFunctionLengthCheckDefinition(self.TriggerLines(error_level),
                                           error_level)

  def TestFunctionLengthCheckBelowErrorLevel(self, error_level):
    """Generate and check function just below the trigger level for --v setting.

    Args:
      error_level: --v setting for cpplint.
    """
    self.TestFunctionLengthCheckDefinition(self.TriggerLines(error_level)-1,
                                           error_level-1)

  def TestFunctionLengthCheckAboveErrorLevel(self, error_level):
    """Generate and check function just above the trigger level for --v setting.

    Args:
      error_level: --v setting for cpplint.
    """
    self.TestFunctionLengthCheckDefinition(self.TriggerLines(error_level)+1,
                                           error_level)

  def FunctionBody(self, number_of_lines):
    return ' {\n' + '    this_is_just_a_test();\n'*number_of_lines + '}'

  def FunctionBodyWithBlankLines(self, number_of_lines):
    return ' {\n' + '    this_is_just_a_test();\n\n'*number_of_lines + '}'

  def FunctionBodyWithNoLints(self, number_of_lines):
    return (' {\n' +
            '    this_is_just_a_test();  // NOLINT\n'*number_of_lines + '}')

  # Test line length checks.
  def testFunctionLengthCheckDeclaration(self):
    self.TestFunctionLengthsCheck(
        'void test();',  # Not a function definition
        '')

  def testFunctionLengthCheckDeclarationWithBlockFollowing(self):
    self.TestFunctionLengthsCheck(
        ('void test();\n'
         + self.FunctionBody(66)),  # Not a function definition
        '')

  def testFunctionLengthCheckClassDefinition(self):
    self.TestFunctionLengthsCheck(  # Not a function definition
        'class Test' + self.FunctionBody(66) + ';',
        '')

  def testFunctionLengthCheckTrivial(self):
    self.TestFunctionLengthsCheck(
        'void test() {}',  # Not counted
        '')

  def testFunctionLengthCheckEmpty(self):
    self.TestFunctionLengthsCheck(
        'void test() {\n}',
        '')

  def testFunctionLengthCheckDefinitionBelowSeverity0(self):
    old_verbosity = cpplint._SetVerboseLevel(0)
    self.TestFunctionLengthCheckDefinitionOK(self.TriggerLines(0)-1)
    cpplint._SetVerboseLevel(old_verbosity)

  def testFunctionLengthCheckDefinitionAtSeverity0(self):
    old_verbosity = cpplint._SetVerboseLevel(0)
    self.TestFunctionLengthCheckDefinitionOK(self.TriggerLines(0))
    cpplint._SetVerboseLevel(old_verbosity)

  def testFunctionLengthCheckDefinitionAboveSeverity0(self):
    old_verbosity = cpplint._SetVerboseLevel(0)
    self.TestFunctionLengthCheckAboveErrorLevel(0)
    cpplint._SetVerboseLevel(old_verbosity)

  def testFunctionLengthCheckDefinitionBelowSeverity1v0(self):
    old_verbosity = cpplint._SetVerboseLevel(0)
    self.TestFunctionLengthCheckBelowErrorLevel(1)
    cpplint._SetVerboseLevel(old_verbosity)

  def testFunctionLengthCheckDefinitionAtSeverity1v0(self):
    old_verbosity = cpplint._SetVerboseLevel(0)
    self.TestFunctionLengthCheckAtErrorLevel(1)
    cpplint._SetVerboseLevel(old_verbosity)

  def testFunctionLengthCheckDefinitionBelowSeverity1(self):
    self.TestFunctionLengthCheckDefinitionOK(self.TriggerLines(1)-1)

  def testFunctionLengthCheckDefinitionAtSeverity1(self):
    self.TestFunctionLengthCheckDefinitionOK(self.TriggerLines(1))

  def testFunctionLengthCheckDefinitionAboveSeverity1(self):
    self.TestFunctionLengthCheckAboveErrorLevel(1)

  def testFunctionLengthCheckDefinitionSeverity1PlusBlanks(self):
    error_level = 1
    error_lines = self.TriggerLines(error_level) + 1
    trigger_level = self.TriggerLines(cpplint._VerboseLevel())
    self.TestFunctionLengthsCheck(
        'void test_blanks(int x)' + self.FunctionBody(error_lines),
        ('Small and focused functions are preferred: '
         'test_blanks() has %d non-comment lines '
         '(error triggered by exceeding %d lines).'
         '  [readability/fn_size] [%d]')
        % (error_lines, trigger_level, error_level))

  def testFunctionLengthCheckComplexDefinitionSeverity1(self):
    error_level = 1
    error_lines = self.TriggerLines(error_level) + 1
    trigger_level = self.TriggerLines(cpplint._VerboseLevel())
    self.TestFunctionLengthsCheck(
        ('my_namespace::my_other_namespace::MyVeryLongTypeName*\n'
         'my_namespace::my_other_namespace::MyFunction(int arg1, char* arg2)'
         + self.FunctionBody(error_lines)),
        ('Small and focused functions are preferred: '
         'my_namespace::my_other_namespace::MyFunction()'
         ' has %d non-comment lines '
         '(error triggered by exceeding %d lines).'
         '  [readability/fn_size] [%d]')
        % (error_lines, trigger_level, error_level))

  def testFunctionLengthCheckDefinitionSeverity1ForTest(self):
    error_level = 1
    error_lines = self.TestLines(error_level) + 1
    trigger_level = self.TestLines(cpplint._VerboseLevel())
    self.TestFunctionLengthsCheck(
        'TEST_F(Test, Mutator)' + self.FunctionBody(error_lines),
        ('Small and focused functions are preferred: '
         'TEST_F(Test, Mutator) has %d non-comment lines '
         '(error triggered by exceeding %d lines).'
         '  [readability/fn_size] [%d]')
        % (error_lines, trigger_level, error_level))

  def testFunctionLengthCheckDefinitionSeverity1ForSplitLineTest(self):
    error_level = 1
    error_lines = self.TestLines(error_level) + 1
    trigger_level = self.TestLines(cpplint._VerboseLevel())
    self.TestFunctionLengthsCheck(
        ('TEST_F(GoogleUpdateRecoveryRegistryProtectedTest,\n'
         '    FixGoogleUpdate_AllValues_MachineApp)'  # note: 4 spaces
         + self.FunctionBody(error_lines)),
        ('Small and focused functions are preferred: '
         'TEST_F(GoogleUpdateRecoveryRegistryProtectedTest, '  # 1 space
         'FixGoogleUpdate_AllValues_MachineApp) has %d non-comment lines '
         '(error triggered by exceeding %d lines).'
         '  [readability/fn_size] [%d]')
        % (error_lines+1, trigger_level, error_level))

  def testFunctionLengthCheckDefinitionSeverity1ForBadTestDoesntBreak(self):
    error_level = 1
    error_lines = self.TestLines(error_level) + 1
    trigger_level = self.TestLines(cpplint._VerboseLevel())
    self.TestFunctionLengthsCheck(
        ('TEST_F('
         + self.FunctionBody(error_lines)),
        ('Small and focused functions are preferred: '
         'TEST_F has %d non-comment lines '
         '(error triggered by exceeding %d lines).'
         '  [readability/fn_size] [%d]')
        % (error_lines, trigger_level, error_level))

  def testFunctionLengthCheckDefinitionSeverity1WithEmbeddedNoLints(self):
    error_level = 1
    error_lines = self.TriggerLines(error_level)+1
    trigger_level = self.TriggerLines(cpplint._VerboseLevel())
    self.TestFunctionLengthsCheck(
        'void test(int x)' + self.FunctionBodyWithNoLints(error_lines),
        ('Small and focused functions are preferred: '
         'test() has %d non-comment lines '
         '(error triggered by exceeding %d lines).'
         '  [readability/fn_size] [%d]')
        % (error_lines, trigger_level, error_level))

  def testFunctionLengthCheckDefinitionSeverity1WithNoLint(self):
    self.TestFunctionLengthsCheck(
        ('void test(int x)' + self.FunctionBody(self.TriggerLines(1))
         + '  // NOLINT -- long function'),
        '')

  def testFunctionLengthCheckDefinitionBelowSeverity2(self):
    self.TestFunctionLengthCheckBelowErrorLevel(2)

  def testFunctionLengthCheckDefinitionSeverity2(self):
    self.TestFunctionLengthCheckAtErrorLevel(2)

  def testFunctionLengthCheckDefinitionAboveSeverity2(self):
    self.TestFunctionLengthCheckAboveErrorLevel(2)

  def testFunctionLengthCheckDefinitionBelowSeverity3(self):
    self.TestFunctionLengthCheckBelowErrorLevel(3)

  def testFunctionLengthCheckDefinitionSeverity3(self):
    self.TestFunctionLengthCheckAtErrorLevel(3)

  def testFunctionLengthCheckDefinitionAboveSeverity3(self):
    self.TestFunctionLengthCheckAboveErrorLevel(3)

  def testFunctionLengthCheckDefinitionBelowSeverity4(self):
    self.TestFunctionLengthCheckBelowErrorLevel(4)

  def testFunctionLengthCheckDefinitionSeverity4(self):
    self.TestFunctionLengthCheckAtErrorLevel(4)

  def testFunctionLengthCheckDefinitionAboveSeverity4(self):
    self.TestFunctionLengthCheckAboveErrorLevel(4)

  def testFunctionLengthCheckDefinitionBelowSeverity5(self):
    self.TestFunctionLengthCheckBelowErrorLevel(5)

  def testFunctionLengthCheckDefinitionAtSeverity5(self):
    self.TestFunctionLengthCheckAtErrorLevel(5)

  def testFunctionLengthCheckDefinitionAboveSeverity5(self):
    self.TestFunctionLengthCheckAboveErrorLevel(5)

  def testFunctionLengthCheckDefinitionHugeLines(self):
    # 5 is the limit
    self.TestFunctionLengthCheckDefinition(self.TriggerLines(10), 5)

  def testFunctionLengthNotDeterminable(self):
    # Macro invocation without terminating semicolon.
    self.TestFunctionLengthsCheck(
        'MACRO(arg)',
        '')

    # Macro with underscores
    self.TestFunctionLengthsCheck(
        'MACRO_WITH_UNDERSCORES(arg1, arg2, arg3)',
        '')

    self.TestFunctionLengthsCheck(
        'NonMacro(arg)',
        'Lint failed to find start of function body.'
        '  [readability/fn_size] [5]')

  def testFunctionLengthCheckWithNamespace(self):
    old_verbosity = cpplint._SetVerboseLevel(1)
    self.TestFunctionLengthsCheck(
        ('namespace {\n'
         'void CodeCoverageCL35256059() {\n' +
         ('  X++;\n' * 3000) +
         '}\n'
         '}  // namespace\n'),
        ('Small and focused functions are preferred: '
         'CodeCoverageCL35256059() has 3000 non-comment lines '
         '(error triggered by exceeding 20 lines).'
         '  [readability/fn_size] [5]'))
    cpplint._SetVerboseLevel(old_verbosity)


def TrimExtraIndent(text_block):
  """Trim a uniform amount of whitespace off of each line in a string.

  Compute the minimum indent on all non blank lines and trim that from each, so
  that the block of text has no extra indentation.

  Args:
    text_block: a multiline string

  Returns:
    text_block with the common whitespace indent of each line removed.
  """

  def CountLeadingWhitespace(s):
    count = 0
    for c in s:
      if not c.isspace():
        break
      count += 1
    return count
  # find the minimum indent (except for blank lines)
  min_indent = min([CountLeadingWhitespace(line)
                    for line in text_block.split('\n') if line])
  return '\n'.join([line[min_indent:] for line in text_block.split('\n')])


class CloseExpressionTest(unittest.TestCase):

  def setUp(self):
    self.lines = cpplint.CleansedLines(
        #           1         2         3         4         5
        # 0123456789012345678901234567890123456789012345678901234567890
        ['// Line 0',
         'inline RCULocked<X>::ReadPtr::ReadPtr(const RCULocked* rcu) {',
         '  DCHECK(!(data & kFlagMask)) << "Error";',
         '}',
         '// Line 4',
         'RCULocked<X>::WritePtr::WritePtr(RCULocked* rcu)',
         '    : lock_(&rcu_->mutex_) {',
         '}',
         '// Line 8',
         'template <typename T, typename... A>',
         'typename std::enable_if<',
         '    std::is_array<T>::value && (std::extent<T>::value > 0)>::type',
         'MakeUnique(A&&... a) = delete;',
         '// Line 13',
         'auto x = []() {};',
         '// Line 15',
         'template <typename U>',
         'friend bool operator==(const reffed_ptr& a,',
         '                       const reffed_ptr<U>& b) {',
         '  return a.get() == b.get();',
         '}',
         '// Line 21'])

  def testCloseExpression(self):
    # List of positions to test:
    # (start line, start position, end line, end position + 1)
    positions = [(1, 16, 1, 19),
                 (1, 37, 1, 59),
                 (1, 60, 3, 1),
                 (2, 8, 2, 29),
                 (2, 30, 22, -1),  # Left shift operator
                 (9, 9, 9, 36),
                 (10, 23, 11, 59),
                 (11, 54, 22, -1),  # Greater than operator
                 (14, 9, 14, 11),
                 (14, 11, 14, 13),
                 (14, 14, 14, 16),
                 (17, 22, 18, 46),
                 (18, 47, 20, 1)]
    for p in positions:
      (_, line, column) = cpplint.CloseExpression(self.lines, p[0], p[1])
      self.assertEquals((p[2], p[3]), (line, column))

  def testReverseCloseExpression(self):
    # List of positions to test:
    # (end line, end position, start line, start position)
    positions = [(1, 18, 1, 16),
                 (1, 58, 1, 37),
                 (2, 27, 2, 10),
                 (2, 28, 2, 8),
                 (6, 18, 0, -1),  # -> operator
                 (9, 35, 9, 9),
                 (11, 54, 0, -1),  # Greater than operator
                 (11, 57, 11, 31),
                 (14, 10, 14, 9),
                 (14, 12, 14, 11),
                 (14, 15, 14, 14),
                 (18, 45, 17, 22),
                 (20, 0, 18, 47)]
    for p in positions:
      (_, line, column) = cpplint.ReverseCloseExpression(self.lines, p[0], p[1])
      self.assertEquals((p[2], p[3]), (line, column))


class NestingStateTest(unittest.TestCase):

  def setUp(self):
    self.nesting_state = cpplint.NestingState()
    self.error_collector = ErrorCollector(self.assert_)

  def UpdateWithLines(self, lines):
    clean_lines = cpplint.CleansedLines(lines)
    for line in xrange(clean_lines.NumLines()):
      self.nesting_state.Update('test.cc',
                                clean_lines, line, self.error_collector)

  def testEmpty(self):
    self.UpdateWithLines([])
    self.assertEquals(self.nesting_state.stack, [])

  def testNamespace(self):
    self.UpdateWithLines(['namespace {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0],
                               cpplint._NamespaceInfo))
    self.assertTrue(self.nesting_state.stack[0].seen_open_brace)
    self.assertEquals(self.nesting_state.stack[0].name, '')

    self.UpdateWithLines(['namespace outer { namespace inner'])
    self.assertEquals(len(self.nesting_state.stack), 3)
    self.assertTrue(self.nesting_state.stack[0].seen_open_brace)
    self.assertTrue(self.nesting_state.stack[1].seen_open_brace)
    self.assertFalse(self.nesting_state.stack[2].seen_open_brace)
    self.assertEquals(self.nesting_state.stack[0].name, '')
    self.assertEquals(self.nesting_state.stack[1].name, 'outer')
    self.assertEquals(self.nesting_state.stack[2].name, 'inner')

    self.UpdateWithLines(['{'])
    self.assertTrue(self.nesting_state.stack[2].seen_open_brace)

    self.UpdateWithLines(['}', '}}'])
    self.assertEquals(len(self.nesting_state.stack), 0)

  def testClass(self):
    self.UpdateWithLines(['class A {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'A')
    self.assertFalse(self.nesting_state.stack[0].is_derived)
    self.assertEquals(self.nesting_state.stack[0].class_indent, 0)

    self.UpdateWithLines(['};',
                          'struct B : public A {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'B')
    self.assertTrue(self.nesting_state.stack[0].is_derived)

    self.UpdateWithLines(['};',
                          'class C',
                          ': public A {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'C')
    self.assertTrue(self.nesting_state.stack[0].is_derived)

    self.UpdateWithLines(['};',
                          'template<T>'])
    self.assertEquals(len(self.nesting_state.stack), 0)

    self.UpdateWithLines(['class D {', '  class E {'])
    self.assertEquals(len(self.nesting_state.stack), 2)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'D')
    self.assertFalse(self.nesting_state.stack[0].is_derived)
    self.assertTrue(isinstance(self.nesting_state.stack[1], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[1].name, 'E')
    self.assertFalse(self.nesting_state.stack[1].is_derived)
    self.assertEquals(self.nesting_state.stack[1].class_indent, 2)
    self.assertEquals(self.nesting_state.InnermostClass().name, 'E')

    self.UpdateWithLines(['}', '}'])
    self.assertEquals(len(self.nesting_state.stack), 0)

  def testClassAccess(self):
    self.UpdateWithLines(['class A {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].access, 'private')

    self.UpdateWithLines([' public:'])
    self.assertEquals(self.nesting_state.stack[0].access, 'public')
    self.UpdateWithLines([' protracted:'])
    self.assertEquals(self.nesting_state.stack[0].access, 'public')
    self.UpdateWithLines([' protected:'])
    self.assertEquals(self.nesting_state.stack[0].access, 'protected')
    self.UpdateWithLines([' private:'])
    self.assertEquals(self.nesting_state.stack[0].access, 'private')

    self.UpdateWithLines(['  struct B {'])
    self.assertEquals(len(self.nesting_state.stack), 2)
    self.assertTrue(isinstance(self.nesting_state.stack[1], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[1].access, 'public')
    self.assertEquals(self.nesting_state.stack[0].access, 'private')

    self.UpdateWithLines(['   protected  :'])
    self.assertEquals(self.nesting_state.stack[1].access, 'protected')
    self.assertEquals(self.nesting_state.stack[0].access, 'private')

    self.UpdateWithLines(['  }', '}'])
    self.assertEquals(len(self.nesting_state.stack), 0)

  def testStruct(self):
    self.UpdateWithLines(['struct A {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'A')
    self.assertFalse(self.nesting_state.stack[0].is_derived)

    self.UpdateWithLines(['}',
                          'void Func(struct B arg) {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertFalse(isinstance(self.nesting_state.stack[0],
                                cpplint._ClassInfo))

    self.UpdateWithLines(['}'])
    self.assertEquals(len(self.nesting_state.stack), 0)

  def testPreprocessor(self):
    self.assertEquals(len(self.nesting_state.pp_stack), 0)
    self.UpdateWithLines(['#if MACRO1'])
    self.assertEquals(len(self.nesting_state.pp_stack), 1)
    self.UpdateWithLines(['#endif'])
    self.assertEquals(len(self.nesting_state.pp_stack), 0)

    self.UpdateWithLines(['#ifdef MACRO2'])
    self.assertEquals(len(self.nesting_state.pp_stack), 1)
    self.UpdateWithLines(['#else'])
    self.assertEquals(len(self.nesting_state.pp_stack), 1)
    self.UpdateWithLines(['#ifdef MACRO3'])
    self.assertEquals(len(self.nesting_state.pp_stack), 2)
    self.UpdateWithLines(['#elif MACRO4'])
    self.assertEquals(len(self.nesting_state.pp_stack), 2)
    self.UpdateWithLines(['#endif'])
    self.assertEquals(len(self.nesting_state.pp_stack), 1)
    self.UpdateWithLines(['#endif'])
    self.assertEquals(len(self.nesting_state.pp_stack), 0)

    self.UpdateWithLines(['#ifdef MACRO5',
                          'class A {',
                          '#elif MACRO6',
                          'class B {',
                          '#else',
                          'class C {',
                          '#endif'])
    self.assertEquals(len(self.nesting_state.pp_stack), 0)
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'A')
    self.UpdateWithLines(['};'])
    self.assertEquals(len(self.nesting_state.stack), 0)

    self.UpdateWithLines(['class D',
                          '#ifdef MACRO7'])
    self.assertEquals(len(self.nesting_state.pp_stack), 1)
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'D')
    self.assertFalse(self.nesting_state.stack[0].is_derived)

    self.UpdateWithLines(['#elif MACRO8',
                          ': public E'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[0].name, 'D')
    self.assertTrue(self.nesting_state.stack[0].is_derived)
    self.assertFalse(self.nesting_state.stack[0].seen_open_brace)

    self.UpdateWithLines(['#else',
                          '{'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[0].name, 'D')
    self.assertFalse(self.nesting_state.stack[0].is_derived)
    self.assertTrue(self.nesting_state.stack[0].seen_open_brace)

    self.UpdateWithLines(['#endif'])
    self.assertEquals(len(self.nesting_state.pp_stack), 0)
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[0].name, 'D')
    self.assertFalse(self.nesting_state.stack[0].is_derived)
    self.assertFalse(self.nesting_state.stack[0].seen_open_brace)

    self.UpdateWithLines([';'])
    self.assertEquals(len(self.nesting_state.stack), 0)

  def testTemplate(self):
    self.UpdateWithLines(['template <T,',
                          '          class Arg1 = tmpl<T> >'])
    self.assertEquals(len(self.nesting_state.stack), 0)
    self.UpdateWithLines(['class A {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'A')

    self.UpdateWithLines(['};',
                          'template <T,',
                          '  template <typename, typename> class B>',
                          'class C'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'C')
    self.UpdateWithLines([';'])
    self.assertEquals(len(self.nesting_state.stack), 0)

    self.UpdateWithLines(['class D : public Tmpl<E>'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'D')

    self.UpdateWithLines(['{', '};'])
    self.assertEquals(len(self.nesting_state.stack), 0)

    self.UpdateWithLines(['template <class F,',
                          '          class G,',
                          '          class H,',
                          '          typename I>',
                          'static void Func() {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertFalse(isinstance(self.nesting_state.stack[0],
                                cpplint._ClassInfo))
    self.UpdateWithLines(['}',
                          'template <class J> class K {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'K')

  def testTemplateInnerClass(self):
    self.UpdateWithLines(['class A {',
                          ' public:'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))

    self.UpdateWithLines(['  template <class B>',
                          '  class C<alloc<B> >',
                          '      : public A {'])
    self.assertEquals(len(self.nesting_state.stack), 2)
    self.assertTrue(isinstance(self.nesting_state.stack[1], cpplint._ClassInfo))

  def testArguments(self):
    self.UpdateWithLines(['class A {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'A')
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 0)

    self.UpdateWithLines(['  void Func(',
                          '    struct X arg1,'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)
    self.UpdateWithLines(['    struct X *arg2);'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 0)

    self.UpdateWithLines(['};'])
    self.assertEquals(len(self.nesting_state.stack), 0)

    self.UpdateWithLines(['struct B {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertTrue(isinstance(self.nesting_state.stack[0], cpplint._ClassInfo))
    self.assertEquals(self.nesting_state.stack[0].name, 'B')

    self.UpdateWithLines(['#ifdef MACRO',
                          '  void Func(',
                          '    struct X arg1'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)
    self.UpdateWithLines(['#else'])

    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 0)
    self.UpdateWithLines(['  void Func(',
                          '    struct X arg1'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)

    self.UpdateWithLines(['#endif'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)
    self.UpdateWithLines(['    struct X *arg2);'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 0)

    self.UpdateWithLines(['};'])
    self.assertEquals(len(self.nesting_state.stack), 0)

  def testInlineAssembly(self):
    self.UpdateWithLines(['void CopyRow_SSE2(const uint8* src, uint8* dst,',
                          '                  int count) {'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 0)
    self.assertEquals(self.nesting_state.stack[-1].inline_asm, cpplint._NO_ASM)

    self.UpdateWithLines(['  asm volatile ('])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)
    self.assertEquals(self.nesting_state.stack[-1].inline_asm,
                      cpplint._INSIDE_ASM)

    self.UpdateWithLines(['    "sub        %0,%1                         \\n"',
                          '  "1:                                         \\n"',
                          '    "movdqa    (%0),%%xmm0                    \\n"',
                          '    "movdqa    0x10(%0),%%xmm1                \\n"',
                          '    "movdqa    %%xmm0,(%0,%1)                 \\n"',
                          '    "movdqa    %%xmm1,0x10(%0,%1)             \\n"',
                          '    "lea       0x20(%0),%0                    \\n"',
                          '    "sub       $0x20,%2                       \\n"',
                          '    "jg        1b                             \\n"',
                          '  : "+r"(src),   // %0',
                          '    "+r"(dst),   // %1',
                          '    "+r"(count)  // %2',
                          '  :',
                          '  : "memory", "cc"'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)
    self.assertEquals(self.nesting_state.stack[-1].inline_asm,
                      cpplint._INSIDE_ASM)

    self.UpdateWithLines(['#if defined(__SSE2__)',
                          '    , "xmm0", "xmm1"'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)
    self.assertEquals(self.nesting_state.stack[-1].inline_asm,
                      cpplint._INSIDE_ASM)

    self.UpdateWithLines(['#endif'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 1)
    self.assertEquals(self.nesting_state.stack[-1].inline_asm,
                      cpplint._INSIDE_ASM)

    self.UpdateWithLines(['  );'])
    self.assertEquals(len(self.nesting_state.stack), 1)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 0)
    self.assertEquals(self.nesting_state.stack[-1].inline_asm, cpplint._END_ASM)

    self.UpdateWithLines(['__asm {'])
    self.assertEquals(len(self.nesting_state.stack), 2)
    self.assertEquals(self.nesting_state.stack[-1].open_parentheses, 0)
    self.assertEquals(self.nesting_state.stack[-1].inline_asm,
                      cpplint._BLOCK_ASM)

    self.UpdateWithLines(['}'])
    self.assertEquals(len(self.nesting_state.stack), 1)

    self.UpdateWithLines(['}'])
    self.assertEquals(len(self.nesting_state.stack), 0)


class QuietTest(unittest.TestCase):

  def setUp(self):
    self.this_dir_path = os.path.dirname(os.path.abspath(__file__))
    self.python_executable = sys.executable or 'python'
    self.cpplint_test_h = os.path.join(self.this_dir_path,
                                       'cpplint_test_header.h')

  def _runCppLint(self, *args):
    cpplint_abspath = os.path.join(self.this_dir_path, 'cpplint.py')

    cmd_line = [self.python_executable, cpplint_abspath] +                     \
        list(args) +                                                           \
        [ self.cpplint_test_h ]

    return_code = 0
    try:
      output = subprocess.check_output(cmd_line,
                                       stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
      return_code = err.returncode
      output = err.output

    return (return_code, output)

  def testNonQuietWithErrors(self):
    # This will fail: the test header is missing a copyright and header guard.
    (return_code, output) = self._runCppLint()
    self.assertEquals(1, return_code)
    # Always-on behavior: Print error messages as they come up.
    self.assertIn("[legal/copyright]", output)
    self.assertIn("[build/header_guard]", output)
    # If --quiet was unspecified: Print 'Done processing' and 'Total errors..'
    self.assertIn("Done processing", output)
    self.assertIn("Total errors found:", output)

  def testQuietWithErrors(self):
    # When there are errors, behavior is identical to not passing --quiet.
    (return_code, output) = self._runCppLint('--quiet')
    self.assertEquals(1, return_code)
    self.assertIn("[legal/copyright]", output)
    self.assertIn("[build/header_guard]", output)
    # Even though --quiet was used, print these since there were errors.
    self.assertIn("Done processing", output)
    self.assertIn("Total errors found:", output)

  def testNonQuietWithoutErrors(self):
    # This will succeed. We filtered out all the known errors for that file.
    (return_code, output) = self._runCppLint('--filter=' +
                                                '-legal/copyright,' +
                                                '-build/header_guard')
    self.assertEquals(0, return_code, output)
    # No cpplint errors are printed since there were no errors.
    self.assertNotIn("[legal/copyright]", output)
    self.assertNotIn("[build/header_guard]", output)
    # Print 'Done processing' and 'Total errors found' since
    # --quiet was not specified.
    self.assertIn("Done processing", output)
    self.assertIn("Total errors found:", output)

  def testQuietWithoutErrors(self):
    # This will succeed. We filtered out all the known errors for that file.
    (return_code, output) = self._runCppLint('--quiet',
                                             '--filter=' +
                                                 '-legal/copyright,' +
                                                 '-build/header_guard')
    self.assertEquals(0, return_code, output)
    # No cpplint errors are printed since there were no errors.
    self.assertNotIn("[legal/copyright]", output)
    self.assertNotIn("[build/header_guard]", output)
    # --quiet was specified and there were no errors:
    # skip the printing of 'Done processing' and 'Total errors..'
    self.assertNotIn("Done processing", output)
    self.assertNotIn("Total errors found:", output)
    # Output with no errors must be completely blank!
    self.assertEquals("", output)

# pylint: disable-msg=C6409
def setUp():
  """Runs before all tests are executed.
  """
  # Enable all filters, so we don't miss anything that is off by default.
  cpplint._DEFAULT_FILTERS = []
  cpplint._cpplint_state.SetFilters('')


# pylint: disable-msg=C6409
def tearDown():
  """A global check to make sure all error-categories have been tested.

  The main tearDown() routine is the only code we can guarantee will be
  run after all other tests have been executed.
  """
  try:
    if _run_verifyallcategoriesseen:
      ErrorCollector(None).VerifyAllCategoriesAreSeen()
  except NameError:
    # If nobody set the global _run_verifyallcategoriesseen, then
    # we assume we should silently not run the test
    pass


if __name__ == '__main__':
  # We don't want to run the VerifyAllCategoriesAreSeen() test unless
  # we're running the full test suite: if we only run one test,
  # obviously we're not going to see all the error categories.  So we
  # only run VerifyAllCategoriesAreSeen() when no commandline flags
  # are passed in.
  global _run_verifyallcategoriesseen
  _run_verifyallcategoriesseen = (len(sys.argv) == 1)

  setUp()
  unittest.main()
  tearDown()
