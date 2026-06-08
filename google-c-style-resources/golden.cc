// Copyright 2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Golden file to test indentation.  The commented-out snippets aren't correct
// yet.

ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
  DoSomething();
  // ...
}

ReturnType ClassName::ReallyLongFunctionName(Type par_name1, Type par_name2,
                                             Type par_name3) {
  DoSomething();
  // ...
}

ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
    Type par_name1,  // 4 space indent
    Type par_name2,
    Type par_name3) {
  DoSomething();  // 2 space indent
  // ...
}

class Foo {
 public:
  Foo(const Foo&) = delete;
  Foo& operator=(const Foo&) = delete;
};

class Shape {
 public:
  virtual void Rotate(double radians) = 0;
};

class Circle : public Shape {
 public:
  void Rotate(double radians) override;
};

void Function() {
  // std::set<int> to_remove = {7, 8, 9};
  // std::vector<int> digits = {3, 9, 1, 8, 4, 7, 1};
  // digits.erase(std::remove_if(digits.begin(), digits.end(), [&to_remove](int i) {
  //                return to_remove.find(i) != to_remove.end();
  //              }),
  //              digits.end());

  bool result = DoSomething(averyveryveryverylongargument1,
                            argument2, argument3);

  if (...) {
    // ...
    // ...
    if (...) {
      bool result = DoSomething(
          argument1, argument2,  // 4 space indent
          argument3, argument4);
      // ...
    }
  }

  // When you have to wrap.
  SomeFunction(
      {"assume a zero-length name before {"},
      some_other_function_parameter);
  // SomeType variable{
  //     some, other, values,
  //     {"assume a zero-length name before {"},
  //     SomeOtherType{
  //         "Very long string requiring the surrounding breaks.",
  //         some, other, values},
  //     SomeOtherType{"Slightly shorter string",
  //                   some, other, values}};
  // SomeType variable{
  //     "This is too long to fit all in one line"};
  // MyType m = {  // Here, you could also break before {.
  //     superlongvariablename1,
  //     superlongvariablename2,
  //     {short, interior, list},
  //     {interiorwrappinglist,
  //      interiorwrappinglist2}};

  if (condition) {                   // no spaces inside parentheses, space before brace
    DoOneThing();                    // two space indent
    DoAnotherThing();
  } else if (int a = f(); a != 3) {  // closing brace on new line, else on same line
    DoAThirdThing(a);
  } else {
    DoNothing();
  }

  if (x == kBar)
    return new Bar(arg1, arg2, arg3);

  switch (var) {
    case 0: {  // 2 space indent
      // ...   // 4 space indent
      break;
    }
    case 1: {
      // ...
      break;
    }
    default: {
      assert(false);
    }
  }

  for (int i = 0; i < kSomeNumber; ++i)
    printf("I love you\n");

  for (int i = 0; i < kSomeNumber; ++i) {
    printf("I take it back\n");
  }

  while (condition) {
    // Repeat test until it returns false.
  }

  if (this_one_thing > this_other_thing &&
      a_third_thing == a_fourth_thing &&
      yet_another && last_one) {
    // ...
  }

  return result;                  // No parentheses in the simple case.
  // Parentheses OK to make a complex expression more readable.
  return (some_long_condition &&
          another_condition);

  // Good - directives at beginning of line
  if (lopsided_score) {
#if DISASTER_PENDING      // Correct -- Starts at beginning of line
    DropEverything();
# if NOTIFY               // OK but not required -- Spaces after #
    NotifyClient();
# endif
#endif
    BackToNormal();
  }
}

class MyClass : public OtherClass {
 public:      // Note the 1 space indent!
  MyClass();  // Regular 2 space indent.
  explicit MyClass(int var);
  ~MyClass() {}

  void SomeFunction();
  void SomeFunctionThatDoesNothing() {
  }

  void set_some_var(int var) { some_var_ = var; }
  int some_var() const { return some_var_; }

 private:
  bool SomeInternalFunction();

  int some_var_;
  int some_other_var_;
};

// When everything fits on one line:
MyClass::MyClass(int var) : some_var_(var) {
  DoSomething();
}

// If the signature and initializer list are not all on one line,
// you must wrap before the colon and indent 4 spaces:
MyClass::MyClass(int var)
    : some_var_(var), some_other_var_(var + 1) {
  DoSomething();
}

// When the list spans multiple lines, put each member on its own line
// and align them:
MyClass::MyClass(int var)
    : some_var_(var),             // 4 space indent
      some_other_var_(var + 1) {  // lined up
  DoSomething();
}

// As with any other code block, the close curly can be on the same
// line as the open curly, if it fits.
MyClass::MyClass(int var)
    : some_var_(var) {}

namespace {

void foo() {  // Correct.  No extra indentation within namespace.
  // ...
}

}  // namespace
