#include <vector>

#include <gtest/test.h>


class Date {
    // ...
public:
    Month month() const;  // do
    int month();          // don't
    // ...
};

void do_something(vector<string>& v)
{
    string val;
    cin >> val;
    // ...
    int index = 0;            // bad
    for (int i = 0; i < v.size(); ++i)
        if (v[i] == val) {
            index = i;
            break;
        }
    // ...
}

struct X {
    char ch;
    int i;
    string s;
    char ch2;

    X& operator=(const X& a);
    X(const X&);
};

X waste(const char* p)
{
	if (p == nullptr) throw Nullptr_error{};
    int n = strlen(p);
    auto buf = new char[n];
    if (buf == nullptr) throw Allocation_error{};
    for (int i = 0; i < n; ++i) buf[i] = p[i];
    // ... manipulate buffer ...
    X x;
    x.ch = 'a';
    x.s = string(n);    // give x.s space for *ps
    for (int i = 0; i < x.s.size(); ++i) x.s[i] = buf[i];	// copy buf into x.s
    delete buf;
    return x;
}

void driver()
{
    X x = waste("Typical argument");
    // ...
}

class X {	// BAD
    int i;
    string s;
    int j;
public:
    X() :i{666}, s{"qqq"} { }	// j is uninitialized
    X(int ii) :i{ii} {}			// s is "" and j is uninitialized
    // ...
};

class X2 {
    int i {666};
    string s {"qqq"};
    int j {0};
public:
    X2() = default;			// all members are initialized to their defaults
    X2(int ii) :i{ii} {}		// s and j initialized to their defaults
    // ...
};

class X3 {	// BAD: inexplicit, argument passing overhead
    int i;
    string s;
    int j;
public:
    X3(int ii = 666, const string& ss = "qqq", int jj = 0)
        :i{ii}, s{ss}, j{jj} { }		// all members are initialized to their defaults
    // ...
};


class Foo {
    string s;
    int i;
public:
    Foo& operator=(Foo&& a);
    // ...
};

Foo& Foo::operator=(Foo&& a)       // OK, but there is a cost
{
    if (this == &a) return *this;  // this line is redundant
    s = std::move(a.s);
    i = a.i;
    return *this;
}

template<typename T>
class Vector2 {
    // ...
    Vector2(Vector2&& a) { *this = a; }				// just use the copy
    Vector2& operator=(Vector2&& a) { *this = a; }	// just use the copy
    //...
public:
    T* elem;
    int sz;
};

void f2(N::X& a, N::X& b)
{
	swap(a,b);		// calls N::swap
}
 
void f3(N::X& a, N::X& b)
{
	using std::swap;	// make std::swap available
	swap(a,b);			// calls N::swap if it exists, otherwise std::swap
}


// webcolors.h (third party header)
#define RED   0xFF0000
#define GREEN 0x00FF00
#define BLUE  0x0000FF

// productinfo.h
// The following define product subtypes based on color
#define RED    0
#define PURPLE 1
#define BLUE   2

int webby = BLUE;   // webby==2; probably not what was desired

enum class Webcolor { red=0xFF0000, green=0x00FF00, blue=0x0000FF };
enum class Productinfo { red=0, purple=1, blue=2 };

int webby = blue;   // error: be specific
Webcolor webby = Webcolor::blue;

enum Webcolor { red=0xFF0000, green=0x00FF00, blue=0x0000FF };
enum Productinfo { red=0, purple=1, blue=2 };

int webby = blue;   // error, ambiguous: be specific
Webcolor webby = Webcolor::blue;

enum class Webcolor { red=0xFF0000, green=0x00FF00, blue=0x0000FF };
enum class Productinfo { red=0, purple=1, blue=2 };

int webby = blue;   // error: blue undefined in this scope
Webcolor webby = Webcolor::blue;


void sink(unique_ptr<widget>); // consumes the widget

void sink(widget*); 			// just uses the widget

void thinko(const unique_ptr<widget>&); // usually not what you want

void reseat(unique_ptr<widget>&); // "will" or "might" reseat pointer

constexpr int max = 8*1024;
int buf[max];					// OK, but suspicious: uninitialized
f.read(buf, max);

constexpr int max = 8*1024;
int buf[max] = {0};				// better in some situations
f.read(buf, max);

string s;	// s is default initialized to ""
cin >> s;	// s expands to hold the string


error_code ec;
Value v = [&] {
    auto p = get_value();	// get_value() returns a pair<error_code, Value>
    ec = p.first;
    return p.second;
}();

Value v = [] {
    auto p = get_value();	// get_value() returns a pair<error_code, Value>
    if (p.first) throw Bad_value{p.first};
    return p.second;
}();

SomeLargeType var;	// ugly CaMeLcAsEvArIaBlE

if (cond)	// some non-trivial condition
    Set(&var);
else if (cond2 || !cond3) {
    var = Set2(3.14);
}
else {
    var = 0;
    for (auto& e : something)
        var += e;
}

string var = [&]{
    if (!in) return "";	// default
    string s;
    for (char c : in >> c)
        s += toupper(c);
    return s;
}(); // note ()

void use(int n)
{
    switch (n) {	// good
    case 0:	// ...
    case 7:	// ...
    }
}

int n = numeric_limits<int>::max();
int m = n + 1;	// bad

std::string s = "hello world";
double* p = (double*)(&s); // BAD

class base { public: virtual ~base() = 0; };

class derived1 : public base { };

class derived2 : public base {
    std::string s;
public:
    std::string get_s() { return s; }
};

derived1 d1;
base* p = &d1; // ok, implicit conversion to pointer to base is fine

derived2* p2 = (derived2*)(p); // BAD, tries to treat d1 as a derived2, which it is not
cout << p2.get_s(); // tries to access d1's nonexistent string member, instead sees arbitrary bytes near d1

void f(const int& i) {
    (int&)(i) = 42;   // BAD
}

static int i = 0;
static const int j = 0;

f(i); // silent side effect
f(j); // undefined behavior


auto x = m*v1 + vv;	// multiply m with v1 and add the result to vv

int i;
for (i = 0; i < max; ++i); // bug waiting to happen
if (i == j)
    return i;
