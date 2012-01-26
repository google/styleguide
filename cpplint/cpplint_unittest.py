#!/usr/bin/python2.4
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
import unittest
import cpplint


# This class works as an error collector and replaces cpplint.Error
# function for the unit tests.  We also verify each category we see
# is in cpplint._ERROR_CATEGORIES, to help keep that list up to date.
class ErrorCollector:
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
    """Fails if there's a category in _ERROR_CATEGORIES - _SEEN_ERROR_CATEGORIES.

    This should only be called after all tests are run, so
    _SEEN_ERROR_CATEGORIES has had a chance to fully populate.  Since
    this isn't called from within the normal unittest framework, we
    can't use the normal unittest assert macros.  Instead we just exit
    when we see an error.  Good thing this test is always run last!
    """
    for category in self._ERROR_CATEGORIES:
      if category not in self._SEEN_ERROR_CATEGORIES:
        import sys
        sys.exit('FATAL ERROR: There are no tests for category "%s"' % category)

  def RemoveIfPresent(self, substr):
    for (index, error) in enumerate(self._errors):
      if error.find(substr) != -1:
        self._errors = self._errors[0:index] + self._errors[(index + 1):]
        break


# This class is a lame mock of codecs. We do not verify filename, mode, or
# encoding, but for the current use case it is not needed.
class MockIo:
  def __init__(self, mock_file):
    self.mock_file = mock_file

  def open(self, unused_filename, unused_mode, unused_encoding, _):  # NOLINT
    # (lint doesn't like open as a method name)
    return self.mock_file


class CpplintTestBase(unittest.TestCase):
  """Provides some useful helper functions for cpplint tests."""

  # Perform lint on single line of input and return the error message.
  def PerformSingleLineLint(self, code):
    error_collector = ErrorCollector(self.assert_)
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments('foo.h', lines, error_collector)
    clean_lines = cpplint.CleansedLines(lines)
    include_state = cpplint._IncludeState()
    function_state = cpplint._FunctionState()
    class_state = cpplint._ClassState()
    cpplint.ProcessLine('foo.cc', 'cc', clean_lines, 0,
                        include_state, function_state,
                        class_state, error_collector)
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
    class_state = cpplint._ClassState()
    for i in xrange(lines.NumLines()):
      cpplint.CheckStyle('foo.h', lines, i, 'h', class_state,
                         error_collector)
      cpplint.CheckForNonStandardConstructs('foo.h', lines, i, class_state,
                                            error_collector)
    class_state.CheckFinished('foo.h', error_collector)
    return error_collector.Results()

  # Similar to PerformMultiLineLint, but calls CheckLanguage instead of
  # CheckForNonStandardConstructs
  def PerformLanguageRulesCheck(self, file_name, code):
    error_collector = ErrorCollector(self.assert_)
    include_state = cpplint._IncludeState()
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments(file_name, lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    ext = file_name[file_name.rfind('.') + 1:]
    for i in xrange(lines.NumLines()):
      cpplint.CheckLanguage(file_name, lines, i, ext, include_state,
                            error_collector)
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
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments(filename, lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    for i in xrange(lines.NumLines()):
      cpplint.CheckLanguage(filename, lines, i, '.h', include_state,
                            error_collector)
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
            'Blank line at the start of a code block.  Is this needed?'
            '  [whitespace/blank_line] [2]'))
    self.assertEquals(
        end_errors,
        error_collector.Results().count(
            'Blank line at the end of a code block.  Is this needed?'
            '  [whitespace/blank_line] [3]'))


class CpplintTest(CpplintTestBase):

  # Test get line width.
  def testGetLineWidth(self):
    self.assertEquals(0, cpplint.GetLineWidth(''))
    self.assertEquals(10, cpplint.GetLineWidth(u'x' * 10))
    self.assertEquals(16, cpplint.GetLineWidth(u'都|道|府|県|支庁'))

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
    # '^' matches the beggining of each line.
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
    self.assertEquals(['a', '// dummy', '// dummy', '// dummy', 'b'], lines)

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
        '// ' + 'x' * 80,
        'Lines should be <= 80 characters long'
        '  [whitespace/line_length] [2]')
    self.TestLint(
        '// ' + 'x' * 100,
        'Lines should very rarely be longer than 100 characters'
        '  [whitespace/line_length] [4]')
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
        '// Read https://g' + ('o' * 60) + 'gle.com/' ,
        '')
    self.TestLint(
        '// $Id: g' + ('o' * 80) + 'gle.cc#1 $',
        '')
    self.TestLint(
        '// $Id: g' + ('o' * 80) + 'gle.cc#1',
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

  # Test taking address of casts (runtime/casting)
  def testRuntimeCasting(self):
    self.TestLint(
        'int* x = &static_cast<int*>(foo);',
        'Are you taking an address of a cast?  '
        'This is dangerous: could be a temp var.  '
        'Take the address before doing the cast, rather than after'
        '  [runtime/casting] [4]')

    self.TestLint(
        'int* x = &dynamic_cast<int *>(foo);',
        ['Are you taking an address of a cast?  '
         'This is dangerous: could be a temp var.  '
         'Take the address before doing the cast, rather than after'
         '  [runtime/casting] [4]',
         'Do not use dynamic_cast<>.  If you need to cast within a class '
         'hierarchy, use static_cast<> to upcast.  Google doesn\'t support '
         'RTTI.  [runtime/rtti] [5]'])

    self.TestLint(
        'int* x = &reinterpret_cast<int *>(foo);',
        'Are you taking an address of a cast?  '
        'This is dangerous: could be a temp var.  '
        'Take the address before doing the cast, rather than after'
        '  [runtime/casting] [4]')

    # It's OK to cast an address.
    self.TestLint(
        'int* x = reinterpret_cast<int *>(&foo);',
        '')

  def testRuntimeSelfinit(self):
    self.TestLint(
        'Foo::Foo(Bar r, Bel l) : r_(r_), l_(l_) { }',
        'You seem to be initializing a member variable with itself.'
        '  [runtime/init] [4]')
    self.TestLint(
        'Foo::Foo(Bar r, Bel l) : r_(r), l_(l) { }',
        '')
    self.TestLint(
        'Foo::Foo(Bar r) : r_(r), l_(r_), ll_(l_) { }',
        '')

  def testRuntimeRTTI(self):
    statement = 'int* x = dynamic_cast<int*>(&foo);'
    error_message = (
        'Do not use dynamic_cast<>.  If you need to cast within a class '
        'hierarchy, use static_cast<> to upcast.  Google doesn\'t support '
        'RTTI.  [runtime/rtti] [5]')
    # dynamic_cast is disallowed in most files.
    self.TestLanguageRulesCheck('foo.cc', statement, error_message)
    self.TestLanguageRulesCheck('foo.h', statement, error_message)
    # It is explicitly allowed in tests, however.
    self.TestLanguageRulesCheck('foo_test.cc', statement, '')
    self.TestLanguageRulesCheck('foo_unittest.cc', statement, '')
    self.TestLanguageRulesCheck('foo_regtest.cc', statement, '')

  # Test for unnamed arguments in a method.
  def testCheckForUnnamedParams(self):
    message = ('All parameters should be named in a function'
               '  [readability/function] [3]')
    self.TestLint('virtual void A(int*) const;', message)
    self.TestLint('virtual void B(void (*fn)(int*));', message)
    self.TestLint('virtual void C(int*);', message)
    self.TestLint('void *(*f)(void *) = x;', message)
    self.TestLint('void Method(char*) {', message)
    self.TestLint('void Method(char*);', message)
    self.TestLint('void Method(char* /*x*/);', message)
    self.TestLint('typedef void (*Method)(int32);', message)
    self.TestLint('static void operator delete[](void*) throw();', message)

    self.TestLint('virtual void D(int* p);', '')
    self.TestLint('void operator delete(void* x) throw();', '')
    self.TestLint('void Method(char* x) {', '')
    self.TestLint('void Method(char* /*x*/) {', '')
    self.TestLint('void Method(char* x);', '')
    self.TestLint('typedef void (*Method)(int32 x);', '')
    self.TestLint('static void operator delete[](void* x) throw();', '')
    self.TestLint('static void operator delete[](void* /*x*/) throw();', '')

    # This one should technically warn, but doesn't because the function
    # pointer is confusing.
    self.TestLint('virtual void E(void (*fn)(int* p));', '')

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
    self.TestLint(
        'int a = int();  // Constructor, o.k.',
        '')
    self.TestLint(
        'X::X() : a(int()) {}  // default Constructor, o.k.',
        '')
    self.TestLint(
        'operator bool();  // Conversion operator, o.k.',
        '')
    self.TestLint(
        'new int64(123);  // "new" operator on basic type, o.k.',
        '')
    self.TestLint(
        'new   int64(123);  // "new" operator on basic type, weird spacing',
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

  # Like gMock method definitions, MockCallback instantiations look very similar
  # to bad casts.
  def testMockCallback(self):
    self.TestLint(
        'MockCallback<bool(int)>',
        '')
    self.TestLint(
        'MockCallback<int(float, char)>',
        '')

  # Test sizeof(type) cases.
  def testSizeofType(self):
    self.TestLint(
        'sizeof(int);',
        'Using sizeof(type).  Use sizeof(varname) instead if possible'
        '  [runtime/sizeof] [1]')
    self.TestLint(
        'sizeof(int *);',
        'Using sizeof(type).  Use sizeof(varname) instead if possible'
        '  [runtime/sizeof] [1]')

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
        'Add #include <algorithm> for swap  [build/include_what_you_use] [4]')
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

  def testMultilineStrings(self):
    multiline_string_error_message = (
        'Multi-line string ("...") found.  This lint script doesn\'t '
        'do well with such strings, and may give bogus warnings.  They\'re '
        'ugly and unnecessary, and you should use concatenation instead".'
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
    # missing explicit is bad
    self.TestMultiLineLint(
        """class Foo {
             Foo(int f);
           };""",
        'Single-argument constructors should be marked explicit.'
        '  [runtime/explicit] [5]')
    # missing explicit is bad, even with whitespace
    self.TestMultiLineLint(
        """class Foo {
             Foo (int f);
           };""",
        ['Extra space before ( in function call  [whitespace/parens] [4]',
         'Single-argument constructors should be marked explicit.'
         '  [runtime/explicit] [5]'])
    # missing explicit, with distracting comment, is still bad
    self.TestMultiLineLint(
        """class Foo {
             Foo(int f);  // simpler than Foo(blargh, blarg)
           };""",
        'Single-argument constructors should be marked explicit.'
        '  [runtime/explicit] [5]')
    # missing explicit, with qualified classname
    self.TestMultiLineLint(
        """class Qualifier::AnotherOne::Foo {
             Foo(int f);
           };""",
        'Single-argument constructors should be marked explicit.'
        '  [runtime/explicit] [5]')
    # missing explicit for inline constructors is bad as well
    self.TestMultiLineLint(
        """class Foo {
             inline Foo(int f);
           };""",
        'Single-argument constructors should be marked explicit.'
        '  [runtime/explicit] [5]')
    # structs are caught as well.
    self.TestMultiLineLint(
        """struct Foo {
             Foo(int f);
           };""",
        'Single-argument constructors should be marked explicit.'
        '  [runtime/explicit] [5]')
    # Templatized classes are caught as well.
    self.TestMultiLineLint(
        """template<typename T> class Foo {
             Foo(int f);
           };""",
        'Single-argument constructors should be marked explicit.'
        '  [runtime/explicit] [5]')
    # inline case for templatized classes.
    self.TestMultiLineLint(
        """template<typename T> class Foo {
             inline Foo(int f);
           };""",
        'Single-argument constructors should be marked explicit.'
        '  [runtime/explicit] [5]')
    # proper style is okay
    self.TestMultiLineLint(
        """class Foo {
             explicit Foo(int f);
           };""",
        '')
    # two argument constructor is okay
    self.TestMultiLineLint(
        """class Foo {
             Foo(int f, int b);
           };""",
        '')
    # two argument constructor, across two lines, is okay
    self.TestMultiLineLint(
        """class Foo {
             Foo(int f,
                 int b);
           };""",
        '')
    # non-constructor (but similar name), is okay
    self.TestMultiLineLint(
        """class Foo {
             aFoo(int f);
           };""",
        '')
    # constructor with void argument is okay
    self.TestMultiLineLint(
        """class Foo {
             Foo(void);
           };""",
        '')
    # single argument method is okay
    self.TestMultiLineLint(
        """class Foo {
             Bar(int b);
           };""",
        '')
    # comments should be ignored
    self.TestMultiLineLint(
        """class Foo {
           // Foo(int f);
           };""",
        '')
    # single argument function following class definition is okay
    # (okay, it's not actually valid, but we don't want a false positive)
    self.TestMultiLineLint(
        """class Foo {
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
        """class Foo {
             Foo(const Foo&);
           };""",
        '')
    self.TestMultiLineLint(
        """class Foo {
             Foo(Foo&);
           };""",
        '')
    # templatized copy constructor is okay.
    self.TestMultiLineLint(
        """template<typename T> class Foo {
             Foo(const Foo<T>&);
           };""",
        '')

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

  def testCheckDeprecated(self):
    self.TestLanguageRulesCheck('foo.cc', '#include <iostream>',
                                'Streams are highly discouraged.'
                                '  [readability/streams] [3]')
    self.TestLanguageRulesCheck('foo_test.cc', '#include <iostream>', '')
    self.TestLanguageRulesCheck('foo_unittest.cc', '#include <iostream>', '')

  def testCheckPosixThreading(self):
    self.TestLint('sctime_r()', '')
    self.TestLint('strtok_r()', '')
    self.TestLint('  strtok_r(foo, ba, r)', '')
    self.TestLint('brand()', '')
    self.TestLint('_rand()', '')
    self.TestLint('.rand()', '')
    self.TestLint('>rand()', '')
    self.TestLint('rand()',
                  'Consider using rand_r(...) instead of rand(...)'
                  ' for improved thread safety.'
                  '  [runtime/threadsafe_fn] [2]')
    self.TestLint('strtok()',
                  'Consider using strtok_r(...) '
                  'instead of strtok(...)'
                  ' for improved thread safety.'
                  '  [runtime/threadsafe_fn] [2]')

  # Test potential format string bugs like printf(foo).
  def testFormatStrings(self):
    self.TestLint('printf("foo")', '')
    self.TestLint('printf("foo: %s", foo)', '')
    self.TestLint('DocidForPrintf(docid)', '')  # Should not trigger.
    self.TestLint('printf(format, value)', '')  # Should not trigger.
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
                  ['Extra space after (  [whitespace/parens] [2]',
                   errmsg
                   ])

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

  # DISALLOW_EVIL_CONSTRUCTORS should be at end of class if present.
  # Same with DISALLOW_COPY_AND_ASSIGN and DISALLOW_IMPLICIT_CONSTRUCTORS.
  def testDisallowEvilConstructors(self):
    for macro_name in (
        'DISALLOW_EVIL_CONSTRUCTORS',
        'DISALLOW_COPY_AND_ASSIGN',
        'DISALLOW_IMPLICIT_CONSTRUCTORS'):
      self.TestLanguageRulesCheck(
          'some_class.h',
          """%s(SomeClass);
          int foo_;
          };""" % macro_name,
          ('%s should be the last thing in the class' % macro_name) +
          '  [readability/constructors] [3]')
      self.TestLanguageRulesCheck(
          'some_class.h',
          """%s(SomeClass);
          };""" % macro_name,
          '')
      self.TestLanguageRulesCheck(
          'some_class.h',
          """%s(SomeClass);
          int foo_;
          } instance, *pointer_to_instance;""" % macro_name,
          ('%s should be the last thing in the class' % macro_name) +
          '  [readability/constructors] [3]')
      self.TestLanguageRulesCheck(
          'some_class.h',
          """%s(SomeClass);
          } instance, *pointer_to_instance;""" % macro_name,
          '')

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
    self.TestLint('CHECK(x == 42)',
                  'Consider using CHECK_EQ instead of CHECK(a == b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x != 42)',
                  'Consider using CHECK_NE instead of CHECK(a != b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x >= 42)',
                  'Consider using CHECK_GE instead of CHECK(a >= b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x > 42)',
                  'Consider using CHECK_GT instead of CHECK(a > b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x <= 42)',
                  'Consider using CHECK_LE instead of CHECK(a <= b)'
                  '  [readability/check] [2]')
    self.TestLint('CHECK(x < 42)',
                  'Consider using CHECK_LT instead of CHECK(a < b)'
                  '  [readability/check] [2]')

    self.TestLint('DCHECK(x == 42)',
                  'Consider using DCHECK_EQ instead of DCHECK(a == b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x != 42)',
                  'Consider using DCHECK_NE instead of DCHECK(a != b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x >= 42)',
                  'Consider using DCHECK_GE instead of DCHECK(a >= b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x > 42)',
                  'Consider using DCHECK_GT instead of DCHECK(a > b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x <= 42)',
                  'Consider using DCHECK_LE instead of DCHECK(a <= b)'
                  '  [readability/check] [2]')
    self.TestLint('DCHECK(x < 42)',
                  'Consider using DCHECK_LT instead of DCHECK(a < b)'
                  '  [readability/check] [2]')

    self.TestLint(
        'EXPECT_TRUE("42" == x)',
        'Consider using EXPECT_EQ instead of EXPECT_TRUE(a == b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE("42" != x)',
        'Consider using EXPECT_NE instead of EXPECT_TRUE(a != b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE(+42 >= x)',
        'Consider using EXPECT_GE instead of EXPECT_TRUE(a >= b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE_M(-42 > x)',
        'Consider using EXPECT_GT_M instead of EXPECT_TRUE_M(a > b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE_M(42U <= x)',
        'Consider using EXPECT_LE_M instead of EXPECT_TRUE_M(a <= b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE_M(42L < x)',
        'Consider using EXPECT_LT_M instead of EXPECT_TRUE_M(a < b)'
        '  [readability/check] [2]')

    self.TestLint(
        'EXPECT_FALSE(x == 42)',
        'Consider using EXPECT_NE instead of EXPECT_FALSE(a == b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_FALSE(x != 42)',
        'Consider using EXPECT_EQ instead of EXPECT_FALSE(a != b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_FALSE(x >= 42)',
        'Consider using EXPECT_LT instead of EXPECT_FALSE(a >= b)'
        '  [readability/check] [2]')
    self.TestLint(
        'ASSERT_FALSE(x > 42)',
        'Consider using ASSERT_LE instead of ASSERT_FALSE(a > b)'
        '  [readability/check] [2]')
    self.TestLint(
        'ASSERT_FALSE(x <= 42)',
        'Consider using ASSERT_GT instead of ASSERT_FALSE(a <= b)'
        '  [readability/check] [2]')
    self.TestLint(
        'ASSERT_FALSE_M(x < 42)',
        'Consider using ASSERT_GE_M instead of ASSERT_FALSE_M(a < b)'
        '  [readability/check] [2]')

    self.TestLint('CHECK(some_iterator == obj.end())', '')
    self.TestLint('EXPECT_TRUE(some_iterator == obj.end())', '')
    self.TestLint('EXPECT_FALSE(some_iterator == obj.end())', '')
    self.TestLint('CHECK(some_pointer != NULL)', '')
    self.TestLint('EXPECT_TRUE(some_pointer != NULL)', '')
    self.TestLint('EXPECT_FALSE(some_pointer != NULL)', '')

    self.TestLint('CHECK(CreateTestFile(dir, (1 << 20)));', '')
    self.TestLint('CHECK(CreateTestFile(dir, (1 >> 20)));', '')

    self.TestLint('CHECK(x<42)',
                  ['Missing spaces around <'
                   '  [whitespace/operators] [3]',
                   'Consider using CHECK_LT instead of CHECK(a < b)'
                   '  [readability/check] [2]'])
    self.TestLint('CHECK(x>42)',
                  'Consider using CHECK_GT instead of CHECK(a > b)'
                  '  [readability/check] [2]')

    self.TestLint(
        '  EXPECT_TRUE(42 < x)  // Random comment.',
        'Consider using EXPECT_LT instead of EXPECT_TRUE(a < b)'
        '  [readability/check] [2]')
    self.TestLint(
        'EXPECT_TRUE( 42 < x )',
        ['Extra space after ( in function call'
         '  [whitespace/parens] [4]',
         'Consider using EXPECT_LT instead of EXPECT_TRUE(a < b)'
         '  [readability/check] [2]'])
    self.TestLint(
        'CHECK("foo" == "foo")',
        'Consider using CHECK_EQ instead of CHECK(a == b)'
        '  [readability/check] [2]')

    self.TestLint('CHECK_EQ("foo", "foo")', '')

  # Passing and returning non-const references
  def testNonConstReference(self):
    # Passing a non-const reference as function parameter is forbidden.
    operand_error_message = ('Is this a non-const reference? '
                             'If so, make const or use a pointer.'
                             '  [runtime/references] [2]')
    # Warn of use of a non-const reference in operators and functions
    self.TestLint('bool operator>(Foo& s, Foo& f);', operand_error_message)
    self.TestLint('bool operator+(Foo& s, Foo& f);', operand_error_message)
    self.TestLint('int len(Foo& s);', operand_error_message)
    # Allow use of non-const references in a few specific cases
    self.TestLint('stream& operator>>(stream& s, Foo& f);', '')
    self.TestLint('stream& operator<<(stream& s, Foo& f);', '')
    self.TestLint('void swap(Bar& a, Bar& b);', '')
    # Returning a non-const reference from a function is OK.
    self.TestLint('int& g();', '')
    # Passing a const reference to a struct (using the struct keyword) is OK.
    self.TestLint('void foo(const struct tm& tm);', '')
    # Passing a const reference to a typename is OK.
    self.TestLint('void foo(const typename tm& tm);', '')
    # Returning an address of something is not prohibited.
    self.TestLint('return &something;', '')
    self.TestLint('if (condition) {return &something; }', '')
    self.TestLint('if (condition) return &something;', '')
    self.TestLint('if (condition) address = &something;', '')
    self.TestLint('if (condition) result = lhs&rhs;', '')
    self.TestLint('if (condition) result = lhs & rhs;', '')
    self.TestLint('a = (b+c) * sizeof &f;', '')
    self.TestLint('a = MySize(b) * sizeof &f;', '')

  def testBraceAtBeginOfLine(self):
    self.TestLint('{',
                  '{ should almost always be at the end of the previous line'
                  '  [whitespace/braces] [4]')

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
    self.TestLint('typedef foo (*foo)(foo)', '')
    self.TestLint('typedef foo (*foo12bar_)(foo)', '')
    self.TestLint('typedef foo (Foo::*bar)(foo)', '')
    self.TestLint('foo (Foo::*bar)(',
                  'Extra space before ( in function call'
                  '  [whitespace/parens] [4]')
    self.TestLint('typedef foo (Foo::*bar)(', '')
    self.TestLint('(foo)(bar)', '')
    self.TestLint('Foo (*foo)(bar)', '')
    self.TestLint('Foo (*foo)(Bar bar,', '')
    self.TestLint('char (*p)[sizeof(foo)] = &foo', '')
    self.TestLint('char (&ref)[sizeof(foo)] = &foo', '')
    self.TestLint('const char32 (*table[])[6];', '')

  def testSpacingBeforeBraces(self):
    self.TestLint('if (foo){', 'Missing space before {'
                  '  [whitespace/braces] [5]')
    self.TestLint('for{', 'Missing space before {'
                  '  [whitespace/braces] [5]')
    self.TestLint('for {', '')
    self.TestLint('EXPECT_DEBUG_DEATH({', '')

  def testSpacingAroundElse(self):
    self.TestLint('}else {', 'Missing space before else'
                  '  [whitespace/braces] [5]')
    self.TestLint('} else{', 'Missing space before {'
                  '  [whitespace/braces] [5]')
    self.TestLint('} else {', '')
    self.TestLint('} else if', '')

  def testSpacingWithInitializerLists(self):
    self.TestLint('int v[1][3] = {{1, 2, 3}};', '')
    self.TestLint('int v[1][1] = {{0}};', '')

  def testSpacingForBinaryOps(self):
    self.TestLint('if (foo<=bar) {', 'Missing spaces around <='
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo<bar) {', 'Missing spaces around <'
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo<bar->baz) {', 'Missing spaces around <'
                  '  [whitespace/operators] [3]')
    self.TestLint('if (foo<bar->bar) {', 'Missing spaces around <'
                  '  [whitespace/operators] [3]')
    self.TestLint('typedef hash_map<Foo, Bar', 'Missing spaces around <'
                  '  [whitespace/operators] [3]')
    self.TestLint('typedef hash_map<FoooooType, BaaaaarType,', '')

  def testSpacingBeforeLastSemicolon(self):
    self.TestLint('call_function() ;',
                  'Extra space before last semicolon. If this should be an '
                  'empty statement, use { } instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('while (true) ;',
                  'Extra space before last semicolon. If this should be an '
                  'empty statement, use { } instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('default:;',
                  'Semicolon defining empty statement. Use { } instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('      ;',
                  'Line contains only semicolon. If this should be an empty '
                  'statement, use { } instead.'
                  '  [whitespace/semicolon] [5]')
    self.TestLint('for (int i = 0; ;', '')

  # Static or global STL strings.
  def testStaticOrGlobalSTLStrings(self):
    self.TestLint('string foo;',
                  'For a static/global string constant, use a C style '
                  'string instead: "char foo[]".'
                  '  [runtime/string] [4]')
    self.TestLint('string kFoo = "hello";  // English',
                  'For a static/global string constant, use a C style '
                  'string instead: "char kFoo[]".'
                  '  [runtime/string] [4]')
    self.TestLint('static string foo;',
                  'For a static/global string constant, use a C style '
                  'string instead: "static char foo[]".'
                  '  [runtime/string] [4]')
    self.TestLint('static const string foo;',
                  'For a static/global string constant, use a C style '
                  'string instead: "static const char foo[]".'
                  '  [runtime/string] [4]')
    self.TestLint('string Foo::bar;',
                  'For a static/global string constant, use a C style '
                  'string instead: "char Foo::bar[]".'
                  '  [runtime/string] [4]')
    # Rare case.
    self.TestLint('string foo("foobar");',
                  'For a static/global string constant, use a C style '
                  'string instead: "char foo[]".'
                  '  [runtime/string] [4]')
    # Should not catch local or member variables.
    self.TestLint('  string foo', '')
    # Should not catch functions.
    self.TestLint('string EmptyString() { return ""; }', '')
    self.TestLint('string EmptyString () { return ""; }', '')
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
    self.TestLint('#endif  // TEST_URLTODOCID_WHICH_HAS_THAT_WORD_IN_IT_H_', '')
    self.TestLint('// See also similar TODO above', '')

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
    self.TestLint('foo();\n'
                  '{ // A scope is opening.', '')
    self.TestLint('  foo();\n'
                  '  { // An indented scope is opening.', '')
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
    self.TestLint('//----', '')
    self.TestLint('//====', '')
    self.TestLint('//////', '')
    self.TestLint('////// x', '')
    self.TestLint('/// x', '')
    self.TestLint('///', '') # Empty Doxygen comment
    self.TestLint('////x', 'Should have a space between // and comment'
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

  def testAllowBlankLineBeforeClosingNamespace(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['namespace {', '', '}  // namespace'],
                            error_collector)
    self.assertEquals(0, error_collector.Results().count(
        'Blank line at the end of a code block.  Is this needed?'
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
        'Blank line at the end of a code block.  Is this needed?'
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

  def testElseOnSameLineAsClosingBraces(self):
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('foo.cc', 'cc',
                            ['if (hoge) {',
                             '',
                             '}',
                             ' else {'  # Warning on this line
                             '',
                             '}'],
                            error_collector)
    self.assertEquals(1, error_collector.Results().count(
        'An else should appear on the same line as the preceding }'
        '  [whitespace/newline] [4]'))

  def testElseClauseNotOnSameLineAsElse(self):
    self.TestLint('  else DoSomethingElse();',
                  'Else clause should never be on same line as else '
                  '(use 2 lines)  [whitespace/newline] [4]')
    self.TestLint('  else ifDoSomethingElse();',
                  'Else clause should never be on same line as else '
                  '(use 2 lines)  [whitespace/newline] [4]')
    self.TestLint('  else if (blah) {', '')
    self.TestLint('  variable_ends_in_else = true;', '')

  def testComma(self):
    self.TestLint('a = f(1,2);',
                  'Missing space after ,  [whitespace/comma] [3]')
    self.TestLint('int tmp=a,a=b,b=tmp;',
                  ['Missing spaces around =  [whitespace/operators] [4]',
                   'Missing space after ,  [whitespace/comma] [3]'])
    self.TestLint('f(a, /* name */ b);', '')
    self.TestLint('f(a, /* name */b);', '')

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
    self.TestLint('  public:', '')
    self.TestLint('   public:', '')

  def testLabel(self):
    self.TestLint('public:',
                  'Labels should always be indented at least one space.  '
                  'If this is a member-initializer list in a constructor or '
                  'the base class list in a class definition, the colon should '
                  'be on the following line.  [whitespace/labels] [4]')
    self.TestLint('  public:', '')
    self.TestLint('   public:', '')
    self.TestLint(' public:', '')
    self.TestLint('  public:', '')
    self.TestLint('   public:', '')

  def testNotALabel(self):
    self.TestLint('MyVeryLongNamespace::MyVeryLongClassName::', '')

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
    old_filters = cpplint._cpplint_state.filters
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
    finally:
      cpplint._USAGE = old_usage
      cpplint._ERROR_CATEGORIES = old_error_categories
      cpplint._cpplint_state.output_format = old_output_format
      cpplint._cpplint_state.verbose_level = old_verbose_level
      cpplint._cpplint_state.filters = old_filters

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

  def testUnnamedNamespacesInHeaders(self):
    self.TestLanguageRulesCheck(
        'foo.h', 'namespace {',
        'Do not use unnamed namespaces in header files.  See'
        ' http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml#Namespaces'
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
    # Don't warn on forward declarations of various types.
    self.TestMultiLineLint(
        'class Foo;',
        '')
    self.TestMultiLineLint(
        """struct Foo*
             foo = NewFoo();""",
        '')
    # Here is an example where the linter gets confused, even though
    # the code doesn't violate the style guide.
    self.TestMultiLineLint(
        """class Foo
        #ifdef DERIVE_FROM_GOO
          : public Goo {
        #else
          : public Hoo {
        #endif
          };""",
        'Failed to find complete declaration of class Foo'
        '  [build/class] [5]')

  def testBuildEndComment(self):
    # The crosstool compiler we currently use will fail to compile the
    # code in this test, so we might consider removing the lint check.
    self.TestLint('#endif Not a comment',
                  'Uncommented text after #endif is non-standard.'
                  '  Use a comment.'
                  '  [build/endif_comment] [5]')

  def testBuildForwardDecl(self):
    # The crosstool compiler we currently use will fail to compile the
    # code in this test, so we might consider removing the lint check.
    self.TestLint('class Foo::Goo;',
                  'Inner-style forward declarations are invalid.'
                  '  Remove this line.'
                  '  [build/forward_decl] [5]')

  def testBuildHeaderGuard(self):
    file_path = 'mydir/foo.h'

    # We can't rely on our internal stuff to get a sane path on the open source
    # side of things, so just parse out the suggested header guard. This
    # doesn't allow us to test the suggested header guard, but it does let us
    # test all the other header tests.
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h', [], error_collector)
    expected_guard = ''
    matcher = re.compile(
      'No \#ifndef header guard found\, suggested CPP variable is\: ([A-Z_]+) ')
    for error in error_collector.ResultList():
      matches = matcher.match(error)
      if matches:
        expected_guard = matches.group(1)
        break

    # Make sure we extracted something for our header guard.
    self.assertNotEqual(expected_guard, '')

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
            'No #define header guard found, suggested CPP variable is: %s'
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
            '#ifndef and #define don\'t match, suggested CPP variable is: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

    # No endif
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData(file_path, 'h',
                            ['#ifndef %s' % expected_guard,
                             '#define %s' % expected_guard],
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
    error_collector = ErrorCollector(self.assert_)
    cpplint.ProcessFileData('mydir/foo_flymake.h',
                            'h', [], error_collector)
    self.assertEquals(
        1,
        error_collector.ResultList().count(
            'No #ifndef header guard found, suggested CPP variable is: %s'
            '  [build/header_guard] [5]' % expected_guard),
        error_collector.ResultList())

  def testBuildInclude(self):
    # Test that include statements have slashes in them.
    self.TestLint('#include "foo.h"',
                  'Include the directory when naming .h files'
                  '  [build/include] [4]')

  def testBuildPrintfFormat(self):
    self.TestLint(
        r'printf("\%%d", value);',
        '%, [, (, and { are undefined character escapes.  Unescape them.'
        '  [build/printf_format] [3]')

    self.TestLint(
        r'snprintf(buffer, sizeof(buffer), "\[%d", value);',
        '%, [, (, and { are undefined character escapes.  Unescape them.'
        '  [build/printf_format] [3]')

    self.TestLint(
        r'fprintf(file, "\(%d", value);',
        '%, [, (, and { are undefined character escapes.  Unescape them.'
        '  [build/printf_format] [3]')

    self.TestLint(
        r'vsnprintf(buffer, sizeof(buffer), "\\\{%d", ap);',
        '%, [, (, and { are undefined character escapes.  Unescape them.'
        '  [build/printf_format] [3]')

    # Don't warn if double-slash precedes the symbol
    self.TestLint(r'printf("\\%%%d", value);',
                  '')

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
    storage_classes = ['auto', 'extern', 'register', 'static', 'typedef']

    build_storage_class_error_message = (
        'Storage class (static, extern, typedef, etc) should be first.'
        '  [build/storage_class] [5]')

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
      other_decl_specs = filter(lambda x: x is not None, other_decl_specs)

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

    copyright_line = '// Copyright 2008 Google Inc. All Rights Reserved.'

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
    self.assertEquals('\#', collapse('\\#'))            # '\#' (bad)

    self.assertEquals('StringReplace(body, "", "");',
                      collapse('StringReplace(body, "\\\\", "\\\\\\\\");'))
    self.assertEquals('\'\' ""',
                      collapse('\'"\' "foo"'))


class OrderOfIncludesTest(CpplintTestBase):
  def setUp(self):
    self.include_state = cpplint._IncludeState()
    # Cheat os.path.abspath called in FileInfo class.
    self.os_path_abspath_orig = os.path.abspath
    os.path.abspath = lambda value: value

  def tearDown(self):
    os.path.abspath = self.os_path_abspath_orig

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
      return ''.join(['#include %s\n' % include for include in includes])

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


class NoNonVirtualDestructorsTest(CpplintTestBase):

  def testNoError(self):
    self.TestMultiLineLint(
        """class Foo {
             virtual ~Foo();
             virtual void foo();
           };""",
        '')

    self.TestMultiLineLint(
        """class Foo {
             virtual inline ~Foo();
             virtual void foo();
           };""",
        '')

    self.TestMultiLineLint(
        """class Foo {
             inline virtual ~Foo();
             virtual void foo();
           };""",
        '')

    self.TestMultiLineLint(
        """class Foo::Goo {
             virtual ~Goo();
             virtual void goo();
           };""",
        '')
    self.TestMultiLineLint(
        'class Foo { void foo(); };',
        'More than one command on the same line  [whitespace/newline] [4]')

    self.TestMultiLineLint(
        """class Qualified::Goo : public Foo {
              virtual void goo();
           };""",
        '')

    self.TestMultiLineLint(
        # Line-ending :
        """class Goo :
           public Foo {
              virtual void goo();
           };""",
        'Labels should always be indented at least one space.  '
        'If this is a member-initializer list in a constructor or '
        'the base class list in a class definition, the colon should '
        'be on the following line.  [whitespace/labels] [4]')

  def testNoDestructorWhenVirtualNeeded(self):
    self.TestMultiLineLintRE(
        """class Foo {
             virtual void foo();
           };""",
        'The class Foo probably needs a virtual destructor')

  def testDestructorNonVirtualWhenVirtualNeeded(self):
    self.TestMultiLineLintRE(
        """class Foo {
             ~Foo();
             virtual void foo();
           };""",
        'The class Foo probably needs a virtual destructor')

  def testNoWarnWhenDerived(self):
    self.TestMultiLineLint(
        """class Foo : public Goo {
             virtual void foo();
           };""",
        '')

  def testNoDestructorWhenVirtualNeededClassDecorated(self):
    self.TestMultiLineLintRE(
        """class LOCKABLE API Foo {
             virtual void foo();
           };""",
        'The class Foo probably needs a virtual destructor')

  def testDestructorNonVirtualWhenVirtualNeededClassDecorated(self):
    self.TestMultiLineLintRE(
        """class LOCKABLE API Foo {
             ~Foo();
             virtual void foo();
           };""",
        'The class Foo probably needs a virtual destructor')

  def testNoWarnWhenDerivedClassDecorated(self):
    self.TestMultiLineLint(
        """class LOCKABLE API Foo : public Goo {
             virtual void foo();
           };""",
        '')

  def testInternalBraces(self):
    self.TestMultiLineLintRE(
        """class Foo {
             enum Goo {
                GOO
             };
             virtual void foo();
           };""",
        'The class Foo probably needs a virtual destructor')

  def testInnerClassNeedsVirtualDestructor(self):
    self.TestMultiLineLintRE(
        """class Foo {
             class Goo {
               virtual void goo();
             };
           };""",
        'The class Goo probably needs a virtual destructor')

  def testOuterClassNeedsVirtualDestructor(self):
    self.TestMultiLineLintRE(
        """class Foo {
             class Goo {
             };
             virtual void foo();
           };""",
        'The class Foo probably needs a virtual destructor')

  def testQualifiedClassNeedsVirtualDestructor(self):
    self.TestMultiLineLintRE(
        """class Qualified::Foo {
             virtual void foo();
           };""",
        'The class Qualified::Foo probably needs a virtual destructor')

  def testMultiLineDeclarationNoError(self):
    self.TestMultiLineLintRE(
        """class Foo
             : public Goo {
            virtual void foo();
           };""",
        '')

  def testMultiLineDeclarationWithError(self):
    self.TestMultiLineLint(
        """class Foo
           {
            virtual void foo();
           };""",
        ['{ should almost always be at the end of the previous line  '
         '[whitespace/braces] [4]',
         'The class Foo probably needs a virtual destructor due to having '
         'virtual method(s), one declared at line 2.  [runtime/virtual] [4]'])

  def testSnprintfSize(self):
    self.TestLint('vsnprintf(NULL, 0, format)', '')
    self.TestLint('snprintf(fisk, 1, format)',
                  'If you can, use sizeof(fisk) instead of 1 as the 2nd arg '
                  'to snprintf.  [runtime/printf] [3]')

  def testExplicitMakePair(self):
    self.TestLint('make_pair', '')
    self.TestLint('make_pair(42, 42)', '')
    self.TestLint('make_pair<',
                  'Omit template arguments from make_pair OR use pair directly'
                  ' OR if appropriate, construct a pair directly'
                  '  [build/explicit_make_pair] [4]')
    self.TestLint('make_pair <',
                  'Omit template arguments from make_pair OR use pair directly'
                  ' OR if appropriate, construct a pair directly'
                  '  [build/explicit_make_pair] [4]')
    self.TestLint('my_make_pair<int, int>', '')

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
    # we assume we shouldn't run the test
    pass


if __name__ == '__main__':
  import sys
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
