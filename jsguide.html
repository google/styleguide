<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Google JavaScript Style Guide</title>
<link rel="stylesheet" href="javaguide.css">
<script src="include/styleguide.js"></script>
<link rel="shortcut icon" href="https://www.google.com/favicon.ico">
<script src="include/jsguide.js"></script>
</head>
<body onload="initStyleGuide();">
<div id="content">
<h1>Google JavaScript Style Guide</h1>
<h2 id="introduction">1 Introduction</h2>

<p>This document serves as the <strong>complete</strong> definition of Google&#8217;s coding standards
for source code in the JavaScript programming language. A JavaScript source file
is described as being <em>in Google Style</em> if and only if it adheres to the rules
herein.</p>

<p>Like other programming style guides, the issues covered span not only aesthetic
issues of formatting, but other types of conventions or coding standards as
well. However, this document focuses primarily on the hard-and-fast rules that
we follow universally, and avoids giving advice that isn't clearly enforceable
(whether by human or tool). </p>

<h3 id="terminology-notes">1.1 Terminology notes</h3>

<p>In this document, unless otherwise clarified:</p>

<ol>
<li><p>The term <em>comment</em> always refers to <em>implementation</em> comments. We do not use
the phrase <q>documentation comments</q>, instead using the common term &#8220;JSDoc&#8221;
for both human-readable text and machine-readable annotations within
<code>/** &#8230; */</code>.</p></li>
<li><p>This Style Guide uses <a href="http://tools.ietf.org/html/rfc2119">RFC 2119</a> terminology when using the phrases <em>must</em>,
<em>must not</em>, <em>should</em>, <em>should not</em>, and <em>may</em>.  The terms <em>prefer</em> and
<em>avoid</em> correspond to <em>should</em> and <em>should not</em>, respectively.  Imperative
and declarative statements are prescriptive and correspond to <em>must</em>.</p></li>
</ol>

<p>Other <q>terminology notes</q> will appear occasionally throughout the document.</p>

<h3 id="guide-notes">1.2 Guide notes</h3>

<p>Example code in this document is <strong>non-normative</strong>. That is, while the examples
are in Google Style, they may not illustrate the <em>only</em> stylish way to represent
the code. Optional formatting choices made in examples must not be enforced as
rules.</p>

<h2 id="source-file-basics">2 Source file basics</h2>

<h3 id="file-name">2.1 File name</h3>

<p>File names must be all lowercase and may include underscores (<code>_</code>) or dashes
(<code>-</code>), but no additional punctuation. Follow the convention that your project
uses. Filenames&#8217; extension must be <code>.js</code>.</p>

<h3 id="file-encoding">2.2 File encoding: UTF-8</h3>

<p>Source files are encoded in <strong>UTF-8</strong>.</p>

<h3 id="special-characters">2.3 Special characters</h3>

<h4 id="whitespace-characters">2.3.1 Whitespace characters</h4>

<p>Aside from the line terminator sequence, the ASCII horizontal space character
(0x20) is the only whitespace character that appears anywhere in a source
file. This implies that</p>

<ol>
<li><p>All other whitespace characters in string literals are escaped, and</p></li>
<li><p>Tab characters are <strong>not</strong> used for indentation.</p></li>
</ol>

<h4 id="special-escape-sequences">2.3.2 Special escape sequences</h4>

<p>For any character that has a special escape sequence (<code>\'</code>, <code>\"</code>, <code>\\</code>, <code>\b</code>,
<code>\f</code>, <code>\n</code>, <code>\r</code>, <code>\t</code>, <code>\v</code>), that sequence is used rather than the
corresponding numeric escape (e.g <code>\x0a</code>, <code>\u000a</code>, or <code>\u{a}</code>). Legacy octal
escapes are never used.</p>

<h4 id="non-ascii-characters">2.3.3 Non-ASCII characters</h4>

<p>For the remaining non-ASCII characters, either the actual Unicode character
(e.g. <code>&#8734;</code>) or the equivalent hex or Unicode escape (e.g. <code>\u221e</code>) is used,
depending only on which makes the code <strong>easier to read and understand</strong>.</p>

<p>Tip: In the Unicode escape case, and occasionally even when actual Unicode
characters are used, an explanatory comment can be very helpful.</p>

<pre><code class="language-js prettyprint">/* Best: perfectly clear even without a comment. */
const units = '&#956;s';

/* Allowed: but unnecessary as &#956; is a printable character. */
const units = '\u03bcs'; // '&#956;s'

/* Good: use escapes for non-printable characters with a comment for clarity. */
return '\ufeff' + content;  // Prepend a byte order mark.
</code></pre>

<pre><code class="language-js prettyprint badcode">/* Poor: the reader has no idea what character this is. */
const units = '\u03bcs';
</code></pre>

<p>Tip: Never make your code less readable simply out of fear that some programs
might not handle non-ASCII characters properly. If that happens, those programs
are <strong>broken</strong> and they must be <strong>fixed</strong>.</p>

<h2 id="source-file-structure">3 Source file structure</h2>

<p>All new source files should either be a <code>goog.module</code> file (a file containing a
<code>goog.module</code> call) or an ECMAScript (ES) module (uses <code>import</code> and <code>export</code>
statements). Files consist of the following, <strong>in order</strong>:</p>

<ol>
<li>License or copyright information, if present</li>
<li><code>@fileoverview</code> JSDoc, if present</li>
<li><code>goog.module</code> statement, if a <code>goog.module</code> file</li>
<li>ES <code>import</code> statements, if an ES module</li>
<li><code>goog.require</code> and <code>goog.requireType</code> statements</li>
<li>The file&#8217;s implementation</li>
</ol>

<p><strong>Exactly one blank line</strong> separates each section that is present, except the
file's implementation, which may be preceded by 1 or 2 blank lines.</p>

<h3 id="file-copyright">3.1 License or copyright information, if present</h3>

<p>If license or copyright information belongs in a file, it belongs here.</p>

<h3 id="file-fileoverview">3.2 <code>@fileoverview</code> JSDoc, if present</h3>

<p>See <a href="#jsdoc-top-file-level-comments">??</a> for formatting rules.</p>

<h3 id="file-goog-module">3.3 <code>goog.module</code> statement</h3>

<p>All <code>goog.module</code> files must declare exactly one <code>goog.module</code> name on a single
line: lines containing a <code>goog.module</code> declaration must not be wrapped, and are
therefore an exception to the 80-column limit.</p>

<p>The entire argument to goog.module is what defines a namespace.  It is the
package name (an identifier that reflects the fragment of the directory
structure where the code lives) plus, optionally, the main class/enum/interface
that it defines concatenated to the end.</p>

<p>Example</p>

<pre><code class="language-js prettyprint">goog.module('search.urlHistory.UrlHistoryService');
</code></pre>

<h4 id="naming-hierarchy">3.3.1 Hierarchy</h4>

<p>Module namespaces may never be named as a <em>direct</em> child of another module's
namespace.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">goog.module('foo.bar');   // 'foo.bar.qux' would be fine, though
goog.module('foo.bar.baz');
</code></pre>

<p>The directory hierarchy reflects the namespace hierarchy, so that deeper-nested
children are subdirectories of higher-level parent directories.  Note that this
implies that owners of &#8220;parent&#8221; namespace groups are necessarily aware of all
child namespaces, since they exist in the same directory.</p>

<h4 id="file-declare-legacy-namespace">3.3.2 <code>goog.module.declareLegacyNamespace</code></h4>

<p>The single <code>goog.module</code> statement may optionally be followed by a call to
<code>goog.module.declareLegacyNamespace();</code>. Avoid
<code>goog.module.declareLegacyNamespace()</code> when possible.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">goog.module('my.test.helpers');
goog.module.declareLegacyNamespace();
goog.setTestOnly();
</code></pre>

<p><code>goog.module.declareLegacyNamespace</code> exists to ease the transition from
traditional object hierarchy-based namespaces but comes with some naming
restrictions. As the child module name must be created after the parent
namespace, this name <strong>must not</strong> be a child or parent of any other
<code>goog.module</code> (for example, <code>goog.module('parent');</code> and
<code>goog.module('parent.child');</code> cannot both exist safely, nor can
<code>goog.module('parent');</code> and <code>goog.module('parent.child.grandchild');</code>).</p>

<h3 id="file-goog-module-exports">3.3.3 <code>goog.module</code> Exports</h3>

<p>Classes, enums, functions, constants, and other symbols are exported using the
<code>exports</code> object. Exported symbols may be defined directly on the <code>exports</code>
object, or else declared locally and exported separately. Symbols are only
exported if they are meant to be used outside the module. Non-exported
module-local symbols are not declared <code>@private</code> nor do their names end with an
underscore. There is no prescribed ordering for exported and module-local
symbols.</p>

<p>Examples:</p>

<pre><code class="language-js prettyprint">const /** !Array&lt;number&gt; */ exportedArray = [1, 2, 3];

const /** !Array&lt;number&gt; */ moduleLocalArray = [4, 5, 6];

/** @return {number} */
function moduleLocalFunction() {
  return moduleLocalArray.length;
}

/** @return {number} */
function exportedFunction() {
  return moduleLocalFunction() * 2;
}

exports = {exportedArray, exportedFunction};
</code></pre>

<pre><code class="language-js prettyprint">/** @const {number} */
exports.CONSTANT_ONE = 1;

/** @const {string} */
exports.CONSTANT_TWO = 'Another constant';
</code></pre>

<p>Do not annotate the <code>exports</code> object as <code>@const</code> as it is already treated as a
constant by the compiler.</p>

<pre><code class="language-js badcode prettyprint">/** @const */
exports = {exportedFunction};
</code></pre>

<p><span id="file-es6-modules"></span></p>

<h3 id="file-es-modules">3.4 ES modules</h3>

<p><span id="es6-module-imports"></span></p>

<h4 id="es-module-imports">3.4.1 Imports</h4>

<p>Import statements must not be line wrapped and are therefore an exception to the
80-column limit.</p>

<p><span id="es6-import-paths"></span></p>

<h5 id="esm-import-paths">3.4.1.1 Import paths</h5>

<p>ES module files must use the <code>import</code> statement to import other ES module
files. Do not <code>goog.require</code> another ES module.</p>

<pre><code class="language-js prettyprint external">import './sideeffects.js';

import * as goog from '../closure/goog/goog.js';
import * as parent from '../parent.js';

import {name} from './sibling.js';
</code></pre>

<p><span id="es6-import-paths-file-extension"></span></p>

<h6 id="esm-import-paths-file-extension">3.4.1.1.1 File extensions in import paths</h6>

<p>The <code>.js</code> file extension is not optional in import paths and must always be
included.</p>

<pre><code class="language-js badcode prettyprint">import '../directory/file';
</code></pre>

<pre><code class="language-js good prettyprint">import '../directory/file.js';
</code></pre>

<h5 id="importing-the-same-file-multiple-times">3.4.1.2 Importing the same file multiple times</h5>

<p>Do not import the same file multiple times. This can make it hard to determine
the aggregate imports of a file.</p>

<pre><code class="language-js badcode prettyprint">// Imports have the same path, but since it doesn't align it can be hard to see.
import {short} from './long/path/to/a/file.js';
import {aLongNameThatBreaksAlignment} from './long/path/to/a/file.js';
</code></pre>

<p><span id="naming-es6-imports"></span></p>

<h5 id="naming-esm-imports">3.4.1.3 Naming imports</h5>

<h6 id="naming-module-imports">3.4.1.3.1 Naming module imports</h6>

<p>Module import names (<code>import * as name</code>) are <code>lowerCamelCase</code> names that are
derived from the imported file name.</p>

<pre><code class="language-js prettyprint">import * as fileOne from '../file-one.js';
import * as fileTwo from '../file_two.js';
import * as fileThree from '../filethree.js';
</code></pre>

<pre><code class="language-js prettyprint">import * as libString from './lib/string.js';
import * as math from './math/math.js';
import * as vectorMath from './vector/math.js';
</code></pre>

<h6 id="naming-default-imports">3.4.1.3.2 Naming default imports</h6>

<p>Default import names are derived from the imported file name and follow the
rules in <a href="#naming-rules-by-identifier-type">??</a>.</p>

<pre><code class="language-js prettyprint">import MyClass from '../my-class.js';
import myFunction from '../my_function.js';
import SOME_CONSTANT from '../someconstant.js';
</code></pre>

<p>Note: In general this should not happen as default exports are banned by this
style guide, see <a href="#named-vs-default-exports">??</a>. Default imports are only used
to import modules that do not conform to this style guide.</p>

<h6 id="naming-named-imports">3.4.1.3.3 Naming named imports</h6>

<p>In general symbols imported via the named import (<code>import {name}</code>) should keep
the same name. Avoid aliasing imports (<code>import {SomeThing as SomeOtherThing}</code>).
Prefer fixing name collisions by using a module import (<code>import *</code>) or renaming
the exports themselves.</p>

<pre><code class="language-js prettyprint">import * as bigAnimals from './biganimals.js';
import * as domesticatedAnimals from './domesticatedanimals.js';

new bigAnimals.Cat();
new domesticatedAnimals.Cat();
</code></pre>

<p>If renaming a named import is needed then use components of the imported
module's file name or path in the resulting alias.</p>

<pre><code class="language-js prettyprint">import {Cat as BigCat} from './biganimals.js';
import {Cat as DomesticatedCat} from './domesticatedanimals.js';

new BigCat();
new DomesticatedCat();
</code></pre>

<p><span id="es6-module-exports"></span></p>

<h4 id="es-module-exports">3.4.2 Exports</h4>

<p>Symbols are only exported if they are meant to be used outside the module.
Non-exported module-local symbols are not declared <code>@private</code> nor do their names
end with an underscore. There is no prescribed ordering for exported and
module-local symbols.</p>

<h5 id="named-vs-default-exports">3.4.2.1 Named vs default exports</h5>

<p>Use named exports in all code. You can apply the <code>export</code> keyword to a
declaration, or use the <code>export {name};</code> syntax.</p>

<p>Do not use default exports. Importing modules must give a name to these values,
which can lead to inconsistencies in naming across modules.</p>

<pre><code class="language-js badcode prettyprint">// Do not use default exports:
export default class Foo { ... } // BAD!
</code></pre>

<pre><code class="language-js good prettyprint">// Use named exports:
export class Foo { ... }
</code></pre>

<pre><code class="language-js good prettyprint">// Alternate style named exports:
class Foo { ... }

export {Foo};
</code></pre>

<h5 id="exporting-static-containers">3.4.2.2 Exporting static container classes and objects</h5>

<p>Do not export container classes or objects with static methods or properties for
the sake of namespacing.</p>

<pre><code class="language-js badcode prettyprint">// container.js
// Bad: Container is an exported class that has only static methods and fields.
export class Container {
  /** @return {number} */
  static bar() {
    return 1;
  }
}

/** @const {number} */
Container.FOO = 1;
</code></pre>

<p>Instead, export individual constants and functions:</p>

<pre><code class="language-js good prettyprint">/** @return {number} */
export function bar() {
  return 1;
}

export const /** number */ FOO = 1;
</code></pre>

<p><span id="es6-exports-mutability"></span></p>

<h5 id="esm-exports-mutability">3.4.2.3 Mutability of exports</h5>

<p>Exported variables must not be mutated outside of module initialization.</p>

<p>There are alternatives if mutation is needed, including exporting a constant
reference to an object that has mutable fields or exporting accessor functions for
mutable data.</p>

<pre><code class="language-js badcode prettyprint">// Bad: both foo and mutateFoo are exported and mutated.
export let /** number */ foo = 0;

/**
 * Mutates foo.
 */
export function mutateFoo() {
  ++foo;
}

/**
 * @param {function(number): number} newMutateFoo
 */
export function setMutateFoo(newMutateFoo) {
  // Exported classes and functions can be mutated!
  mutateFoo = () =&gt; {
    foo = newMutateFoo(foo);
  };
}
</code></pre>

<pre><code class="language-js good prettyprint">// Good: Rather than export the mutable variables foo and mutateFoo directly,
// instead make them module scoped and export a getter for foo and a wrapper for
// mutateFooFunc.
let /** number */ foo = 0;
let /** function(number): number */ mutateFooFunc = foo =&gt; foo + 1;

/** @return {number} */
export function getFoo() {
  return foo;
}

export function mutateFoo() {
  foo = mutateFooFunc(foo);
}

/** @param {function(number): number} mutateFoo */
export function setMutateFoo(mutateFoo) {
  mutateFooFunc = mutateFoo;
}
</code></pre>

<p><span id="es6-module-circular-dependencies"></span></p>

<h5 id="es-module-export-from">3.4.2.4 export from</h5>

<p><code>export from</code> statements must not be line wrapped and are therefore an
exception to the 80-column limit. This applies to both <code>export from</code> flavors.</p>

<pre><code class="language-js">export {specificName} from './other.js';
export * from './another.js';
</code></pre>

<h4 id="es-module-circular-dependencies">3.4.3 Circular Dependencies in ES modules</h4>

<p>Do not create cycles between ES modules, even though the ECMAScript
specification allows this. Note that it is possible to create cycles with both
the <code>import</code> and <code>export</code> statements.</p>

<pre><code class="language-js badcode prettyprint">// a.js
import './b.js';
</code></pre>

<pre><code class="language-js badcode prettyprint">// b.js
import './a.js';

// `export from` can cause circular dependencies too!
export {x} from './c.js';
</code></pre>

<pre><code class="language-js badcode prettyprint">// c.js
import './b.js';

export let x;
</code></pre>

<p><span id="es6-module-closure-interop"></span></p>

<h4 id="es-module-closure-interop">3.4.4 Interoperating with Closure</h4>

<p><span id="es6-module-referencing-goog"></span></p>

<h5 id="es-module-referencing-goog">3.4.4.1 Referencing goog</h5>

<p>To reference the Closure <code>goog</code> namespace, import Closure's <code>goog.js</code>.</p>

<pre><code class="language-js good prettyprint external">import * as goog from '../closure/goog/goog.js';

const name = goog.require('a.name');

export const CONSTANT = name.compute();
</code></pre>

<p><code>goog.js</code> exports only a subset of properties from the global <code>goog</code> that can be
used in ES modules.</p>

<p><span id="goog-require-in-es6-module"></span></p>

<h5 id="goog-require-in-es-module">3.4.4.2 goog.require in ES modules</h5>

<p><code>goog.require</code> in ES modules works as it does in <code>goog.module</code> files. You can
require any Closure namespace symbol (i.e., symbols created by <code>goog.provide</code> or
<code>goog.module</code>) and <code>goog.require</code> will return the value.</p>

<pre><code class="language-js prettyprint external">import * as goog from '../closure/goog/goog.js';
import * as anEsModule from './anEsModule.js';

const GoogPromise = goog.require('goog.Promise');
const myNamespace = goog.require('my.namespace');
</code></pre>

<p><span id="closure-module-id-in-es6-module"></span></p>

<h5 id="closure-module-id-in-es-module">3.4.4.3 Declaring Closure Module IDs in ES modules</h5>

<p><code>goog.declareModuleId</code> can be used within ES modules to declare a
<code>goog.module</code>-like module ID. This means that this module ID can be
<code>goog.require</code>d, <code>goog.module.get</code>d, <code>goog.forwardDeclare</code>'d, etc. as if it were
a <code>goog.module</code> that did not call <code>goog.module.declareLegacyNamespace</code>. It does
not create the module ID as a globally available JavaScript symbol.</p>

<p>A <code>goog.require</code> (or <code>goog.module.get</code>) for a module ID from
<code>goog.declareModuleId</code> will always return the module object (as if it was
<code>import *</code>'d). As a result, the argument to <code>goog.declareModuleId</code> should always
end with a <code>lowerCamelCaseName</code>.</p>

<p>Note: It is an error to call <code>goog.module.declareLegacyNamespace</code> in an ES
module, it can only be called from <code>goog.module</code> files. There is no direct way
to associate a <q>legacy</q> namespace with an ES module.</p>

<p><code>goog.declareModuleId</code> should only be used to upgrade Closure files to ES
modules in place, where named exports are used.</p>

<pre><code class="language-js prettyprint external">import * as goog from '../closure/goog.js';

goog.declareModuleId('my.esm');

export class Class {};
</code></pre>

<h3 id="file-set-test-only">3.5 <code>goog.setTestOnly</code></h3>

<p>In a <code>goog.module</code> file the <code>goog.module</code> statement may optionally be followed
by a call to <code>goog.setTestOnly()</code>.</p>

<p>In an ES module the <code>import</code> statements may optionally be followed by a call to
<code>goog.setTestOnly()</code>.</p>

<h3 id="file-goog-require">3.6 <code>goog.require</code> and <code>goog.requireType</code> statements</h3>

<p>Imports are done with <code>goog.require</code> and <code>goog.requireType</code> statements. The
names imported by a <code>goog.require</code> statement may be used both in code and in
type annotations, while those imported by a <code>goog.requireType</code> may be used
in type annotations only.</p>

<p>The <code>goog.require</code> and <code>goog.requireType</code> statements form a contiguous block
with no empty lines. This block follows the <code>goog.module</code> declaration separated
<a href="#source-file-structure">by a single empty line</a>. The entire argument to
<code>goog.require</code> or <code>goog.requireType</code> is a namespace defined by a <code>goog.module</code>
in a separate file. <code>goog.require</code> and <code>goog.requireType</code> statements may not
appear anywhere else in the file.</p>

<p>Each <code>goog.require</code> or <code>goog.requireType</code> is assigned to a single constant
alias, or else destructured into several constant aliases. These aliases are the
only acceptable way to refer to dependencies in type annotations or code. Fully
qualified namespaces must not be used anywhere, except as an argument to
<code>goog.require</code> or <code>goog.requireType</code>.</p>

<p><strong>Exception</strong>: Types, variables, and functions declared in externs files have to
use their fully qualified name in type annotations and code.</p>

<p>Aliases must match the final dot-separated component of the imported module's
namespace.</p>

<p><strong>Exception</strong>: In certain cases, additional components of the namespace can be
used to form a longer alias. The resulting alias must retain the original
identifier's casing such that it still correctly identifies its type. Longer
aliases may be used to disambiguate otherwise identical aliases, or if it
significantly improves readability. In addition, a longer alias must be used to
prevent masking native types such as <code>Element</code>, <code>Event</code>, <code>Error</code>, <code>Map</code>, and
<code>Promise</code> (for a more complete list, see <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects">Standard Built-in Objects</a> and <a href="https://developer.mozilla.org/en-US/docs/Web/API">Web
APIs</a> at MDN). When renaming destructured aliases, a space must follow the colon
as required in <a href="#formatting-horizontal-whitespace">??</a>.</p>

<p>A file should not contain both a <code>goog.require</code> and a <code>goog.requireType</code>
statement for the same namespace. If the imported name is used both in code and
in type annotations, it should be imported by a single <code>goog.require</code> statement.</p>

<p>If a module is imported only for its side effects, the call must be a
<code>goog.require</code> (not a <code>goog.requireType</code>) and assignment may be omitted. A
comment is required to explain why this is needed and suppress a compiler
warning.</p>



<p>The lines are sorted according to the following rules: All requires with a name
on the left hand side come first, sorted alphabetically by those names. Then
destructuring requires, again sorted by the names on the left hand side.
Finally, any require calls that are standalone (generally these are for modules
imported just for their side effects).</p>

<p>Tip: There&#8217;s no need to memorize this order and enforce it manually. You can
rely on your IDE to report requires
that are not sorted correctly.</p>

<p>If a long alias or module name would cause a line to exceed the 80-column limit,
it <strong>must not</strong> be wrapped: require lines are an exception to the 80-column
limit.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">// Standard alias style.
const MyClass = goog.require('some.package.MyClass');
const MyType = goog.requireType('some.package.MyType');
// Namespace-based alias used to disambiguate.
const NsMyClass = goog.require('other.ns.MyClass');
// Namespace-based alias used to prevent masking native type.
const RendererElement = goog.require('web.renderer.Element');
// Out of sequence namespace-based aliases used to improve readability.
// Also, require lines longer than 80 columns must not be wrapped.
const SomeDataStructureModel = goog.requireType('identical.package.identifiers.models.SomeDataStructure');
const SomeDataStructureProto = goog.require('proto.identical.package.identifiers.SomeDataStructure');
// Standard alias style.
const asserts = goog.require('goog.asserts');
// Namespace-based alias used to disambiguate.
const testingAsserts = goog.require('goog.testing.asserts');
// Standard destructuring into aliases.
const {clear, clone} = goog.require('goog.array');
const {Rgb} = goog.require('goog.color');
// Namespace-based destructuring into aliases in order to disambiguate.
const {SomeType: FooSomeType} = goog.requireType('foo.types');
const {clear: objectClear, clone: objectClone} = goog.require('goog.object');
// goog.require without an alias in order to trigger side effects.
/** @suppress {extraRequire} Initializes MyFramework. */
goog.require('my.framework.initialization');
</code></pre>

<p>Discouraged:</p>

<pre><code class="language-js badcode prettyprint">// If necessary to disambiguate, prefer PackageClass over SomeClass as it is
// closer to the format of the module name.
const SomeClass = goog.require('some.package.Class');
</code></pre>

<p>Disallowed:</p>

<pre><code class="language-js badcode prettyprint">// Extra terms must come from the namespace.
const MyClassForBizzing = goog.require('some.package.MyClass');
// Alias must include the entire final namespace component.
const MyClass = goog.require('some.package.MyClassForBizzing');
// Alias must not mask native type (should be `const JspbMap` here).
const Map = goog.require('jspb.Map');
// Don't break goog.require lines over 80 columns.
const SomeDataStructure =
    goog.require('proto.identical.package.identifiers.SomeDataStructure');
// Alias must be based on the namespace.
const randomName = goog.require('something.else');
// Missing a space after the colon.
const {Foo:FooProto} = goog.require('some.package.proto.Foo');
// goog.requireType without an alias.
goog.requireType('some.package.with.a.Type');


/**
 * @param {!some.unimported.Dependency} param All external types used in JSDoc
 *     annotations must be goog.require'd, unless declared in externs.
 */
function someFunction(param) {
  // goog.require lines must be at the top level before any other code.
  const alias = goog.require('my.long.name.alias');
  // ...
}
</code></pre>

<h3 id="file-implementation">3.7 The file&#8217;s implementation</h3>

<p>The actual implementation follows after all dependency information is declared
(separated by at least one blank line).</p>

<p>This may consist of any module-local declarations (constants, variables,
classes, functions, etc), as well as any exported symbols.
</p>

<h2 id="formatting">4 Formatting</h2>

<p><strong>Terminology Note</strong>: <em>block-like construct</em> refers to the body of a class,
function, method, or brace-delimited block of code.  Note that, by
<a href="#features-array-literals">??</a> and <a href="#features-object-literals">??</a>, any array or
object literal may optionally be treated as if it were a block-like construct.</p>

<p>Tip: Use <code>clang-format</code>. The JavaScript community has invested effort to make
sure clang-format <q>does the right thing</q> on JavaScript files. <code>clang-format</code> has
integration with several popular
editors.</p>

<h3 id="formatting-braces">4.1 Braces</h3>

<h4 id="formatting-braces-all">4.1.1 Braces are used for all control structures</h4>

<p>Braces are required for all control structures (i.e. <code>if</code>, <code>else</code>, <code>for</code>, <code>do</code>,
<code>while</code>, as well as any others), even if the body contains only a single
statement.  The first statement of a non-empty block must begin on its own line.</p>

<p>Disallowed:</p>

<pre><code class="language-js badcode prettyprint">if (someVeryLongCondition())
  doSomething();

for (let i = 0; i &lt; foo.length; i++) bar(foo[i]);
</code></pre>

<p><strong>Exception</strong>: A simple if statement that can fit entirely on a single line with
no wrapping (and that doesn&#8217;t have an else) may be kept on a single line with no
braces when it improves readability.  This is the only case in which a control
structure may omit braces and newlines.</p>

<pre><code class="language-js prettyprint">if (shortCondition()) foo();
</code></pre>

<h4 id="formatting-nonempty-blocks">4.1.2 Nonempty blocks: K&amp;R style</h4>

<p>Braces follow the Kernighan and Ritchie style (<q><a href="http://www.codinghorror.com/blog/2012/07/new-programming-jargon.html">Egyptian brackets</a></q>) for
<em>nonempty</em> blocks and block-like constructs:</p>

<ul>
<li>No line break before the opening brace.</li>
<li>Line break after the opening brace.</li>
<li>Line break before the closing brace.</li>
<li>Line break after the closing brace <em>if</em> that brace terminates a statement or
the body of a function or class statement, or a class method. Specifically,
there is <em>no</em> line break after the brace if it is followed by <code>else</code>, <code>catch</code>,
<code>while</code>, or a comma, semicolon, or right-parenthesis.</li>
</ul>

<p>Example:</p>

<pre><code class="language-js prettyprint">class InnerClass {
  constructor() {}

  /** @param {number} foo */
  method(foo) {
    if (condition(foo)) {
      try {
        // Note: this might fail.
        something();
      } catch (err) {
        recover();
      }
    }
  }
}
</code></pre>

<h4 id="formatting-empty-blocks">4.1.3 Empty blocks: may be concise</h4>

<p>An empty block or block-like construct <em>may</em> be closed immediately after it is
opened, with no characters, space, or line break in between (i.e. <code>{}</code>),
<strong>unless</strong> it is a part of a <em>multi-block statement</em> (one that directly contains
multiple blocks: <code>if</code>/<code>else</code> or <code>try</code>/<code>catch</code>/<code>finally</code>).</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">function doNothing() {}
</code></pre>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">if (condition) {
  // &#8230;
} else if (otherCondition) {} else {
  // &#8230;
}

try {
  // &#8230;
} catch (e) {}
</code></pre>

<h3 id="formatting-block-indentation">4.2 Block indentation: +2 spaces</h3>

<p>Each time a new block or block-like construct is opened, the indent increases by
two spaces. When the block ends, the indent returns to the previous indent
level. The indent level applies to both code and comments throughout the
block. (See the example in <a href="#formatting-nonempty-blocks">??</a>).</p>

<h4 id="formatting-array-literals">4.2.1 Array literals: optionally <q>block-like</q></h4>

<p>Any array literal may optionally be formatted as if it were a &#8220;block-like
construct.&#8221; For example, the following are all valid (<strong>not</strong> an exhaustive
list):</p>

<pre><code class="language-js prettyprint columns">const a = [
  0,
  1,
  2,
];

const b =
    [0, 1, 2];

</code></pre>

<pre><code class="language-js prettyprint columns">const c = [0, 1, 2];

someMethod(foo, [
  0, 1, 2,
], bar);
</code></pre>

<p>Other combinations are allowed, particularly when emphasizing semantic groupings
between elements, but should not be used only to reduce the vertical size of
larger arrays.</p>

<h4 id="formatting-object-literals">4.2.2 Object literals: optionally <q>block-like</q></h4>

<p>Any object literal may optionally be formatted as if it were a &#8220;block-like
construct.&#8221; The same examples apply as <a href="#formatting-array-literals">??</a>. For
example, the following are all valid (<strong>not</strong> an exhaustive list):</p>

<pre><code class="language-js prettyprint columns">const a = {
  a: 0,
  b: 1,
};

const b =
    {a: 0, b: 1};
</code></pre>

<pre><code class="language-js prettyprint columns">const c = {a: 0, b: 1};

someMethod(foo, {
  a: 0, b: 1,
}, bar);
</code></pre>

<h4 id="formatting-class-literals">4.2.3 Class literals</h4>

<p>Class literals (whether declarations or expressions) are indented as blocks. Do
not add semicolons after methods, or after the closing brace of a class
<em>declaration</em> (statements&#8212;such as assignments&#8212;that contain class <em>expressions</em>
are still terminated with a semicolon). Use the <code>extends</code> keyword, but not the
<code>@extends</code> JSDoc annotation unless the class extends a templatized type.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint columns">class Foo {
  constructor() {
    /** @type {number} */
    this.x = 42;
  }

  /** @return {number} */
  method() {
    return this.x;
  }
}
Foo.Empty = class {};
</code></pre>

<pre><code class="language-js prettyprint columns">/** @extends {Foo&lt;string&gt;} */
foo.Bar = class extends Foo {
  /** @override */
  method() {
    return super.method() / 2;
  }
};

/** @interface */
class Frobnicator {
  /** @param {string} message */
  frobnicate(message) {}
}
</code></pre>

<h4 id="formatting-function-expressions">4.2.4 Function expressions</h4>

<p>When declaring an anonymous function in the list of arguments for a function
call, the body of the function is indented two spaces more than the preceding
indentation depth.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">prefix.something.reallyLongFunctionName('whatever', (a1, a2) =&gt; {
  // Indent the function body +2 relative to indentation depth
  // of the 'prefix' statement one line above.
  if (a1.equals(a2)) {
    someOtherLongFunctionName(a1);
  } else {
    andNowForSomethingCompletelyDifferent(a2.parrot);
  }
});

some.reallyLongFunctionCall(arg1, arg2, arg3)
    .thatsWrapped()
    .then((result) =&gt; {
      // Indent the function body +2 relative to the indentation depth
      // of the '.then()' call.
      if (result) {
        result.use();
      }
    });
</code></pre>

<h4 id="formatting-switch-statements">4.2.5 Switch statements</h4>

<p>As with any other block, the contents of a switch block are indented +2.</p>



<p>After a switch label, a newline appears, and the indentation level is increased
+2, exactly as if a block were being opened. An explicit block may be used if
required by lexical scoping. The following switch label returns to the previous
indentation level, as if a block had been closed.</p>

<p>A blank line is optional between a <code>break</code> and the following case.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">switch (animal) {
  case Animal.BANDERSNATCH:
    handleBandersnatch();
    break;

  case Animal.JABBERWOCK:
    handleJabberwock();
    break;

  default:
    throw new Error('Unknown animal');
}
</code></pre>

<h3 id="formatting-statements">4.3 Statements</h3>

<h4 id="formatting-one-statement-perline">4.3.1 One statement per line</h4>

<p>Each statement is followed by a line-break.</p>

<h4 id="formatting-semicolons-are-required">4.3.2 Semicolons are required</h4>

<p>Every statement must be terminated with a semicolon. Relying on automatic
semicolon insertion is forbidden.</p>

<h3 id="formatting-column-limit">4.4 Column limit: 80</h3>

<p>JavaScript code has a column limit of 80 characters. Except as noted below, any
line that would exceed this limit must be line-wrapped, as explained in
<a href="#formatting-line-wrapping">??</a>.</p>

<p><strong>Exceptions:</strong></p>

<ol>
<li><code>goog.module</code>, <code>goog.require</code> and <code>goog.requireType</code> statements (see
<a href="#file-goog-module">??</a> and <a href="#file-goog-require">??</a>).</li>
<li>ES module <code>import</code> and <code>export from</code> statements (see
<a href="#es-module-imports">??</a> and <a href="#es-module-export-from">??</a>).</li>
<li>Lines where obeying the column limit is not possible or would hinder
discoverability. Examples include:
<ul>
<li>A long URL which should be clickable in source.</li>
<li>A shell command intended to be copied-and-pasted.</li>
<li>A long string literal which may need to be copied or searched for wholly
(e.g., a long file path).</li>
</ul></li>
</ol>

<h3 id="formatting-line-wrapping">4.5 Line-wrapping</h3>

<p><strong>Terminology Note</strong>: <em>Line wrapping</em> is breaking a chunk of code into multiple
lines to obey column limit, where the chunk could otherwise legally fit in a
single line.</p>

<p>There is no comprehensive, deterministic formula showing <em>exactly</em> how to
line-wrap in every situation. Very often there are several valid ways to
line-wrap the same piece of code.</p>

<p>Note: While the typical reason for line-wrapping is to avoid overflowing the
column limit, even code that would in fact fit within the column limit may be
line-wrapped at the author's discretion.</p>

<p>Tip: Extracting a method or local variable may solve the problem without the
need to line-wrap.</p>

<h4 id="formatting-where-to-break">4.5.1 Where to break</h4>

<p>The prime directive of line-wrapping is: prefer to break at a <strong>higher syntactic
level</strong>. </p>

<p>Preferred:</p>

<pre><code class="language-js prettyprint">currentEstimate =
    calc(currentEstimate + x * currentEstimate) /
        2.0;
</code></pre>

<p>Discouraged:</p>

<pre><code class="language-js prettyprint badcode">currentEstimate = calc(currentEstimate + x *
    currentEstimate) / 2.0;
</code></pre>

<p>In the preceding example, the syntactic levels from highest to lowest are as
follows: assignment, division, function call, parameters, number constant.</p>

<p>Operators are wrapped as follows:</p>

<ol>
<li>When a line is broken at an operator the break comes after the symbol. (Note
that this is not the same practice used in Google style for Java.)
<ol>
<li>This does not apply to the <q>dot</q> (<code>.</code>), which is not actually an
operator.</li>
</ol></li>
<li>A method or constructor name stays attached to the open parenthesis (<code>(</code>)
that follows it.</li>
<li>A comma (<code>,</code>) stays attached to the token that precedes it.</li>
</ol>

<blockquote>
<p>Note: The primary goal for line wrapping is to have clear code, not
necessarily code that fits in the smallest number of lines.</p>
</blockquote>

<h4 id="formatting-indent">4.5.2 Indent continuation lines at least +4 spaces</h4>

<p>When line-wrapping, each line after the first (each <em>continuation line</em>) is
indented at least +4 from the original line, unless it falls under the rules of
block indentation.</p>

<p>When there are multiple continuation lines, indentation may be varied beyond +4
as appropriate.  In general, continuation lines at a deeper syntactic level are
indented by larger multiples of 4, and two lines use the same indentation level
if and only if they begin with syntactically parallel elements.</p>

<p><a href="#formatting-horizontal-alignment">??</a> addresses the discouraged practice of
using a variable number of spaces to align certain tokens with previous lines.</p>

<h3 id="formatting-whitespace">4.6 Whitespace</h3>

<h4 id="formatting-vertical-whitespace">4.6.1 Vertical whitespace</h4>

<p>A single blank line appears:</p>

<ol>
<li>Between consecutive methods in a class or object literal
<ol>
<li>Exception: A blank line between two consecutive properties definitions in
an object literal (with no other code between them) is optional. Such
blank lines are used as needed to create <em>logical groupings</em> of fields.</li>
</ol></li>
<li>Within method bodies, sparingly to create <em>logical groupings</em> of statements.
Blank lines at the start or end of a function body are not allowed.</li>
<li><em>Optionally</em> before the first or after the last method in a class or object
literal (neither encouraged nor discouraged).</li>
<li>As required by other sections of this document (e.g.
<a href="#file-goog-require">??</a>).</li>
</ol>

<p><em>Multiple</em> consecutive blank lines are permitted, but never required (nor
encouraged).</p>

<h4 id="formatting-horizontal-whitespace">4.6.2 Horizontal whitespace</h4>

<p>Use of horizontal whitespace depends on location, and falls into three broad
categories: <em>leading</em> (at the start of a line), <em>trailing</em> (at the end of a
line), and <em>internal</em>.  Leading whitespace (i.e., indentation) is addressed
elsewhere.  Trailing whitespace is forbidden.</p>

<p>Beyond where required by the language or other style rules, and apart from
literals, comments, and JSDoc, a single internal ASCII space also appears in the
following places <strong>only</strong>.</p>

<ol>
<li>Separating any reserved word (such as <code>if</code>, <code>for</code>, or <code>catch</code>) except for
<code>function</code> and <code>super</code>, from an open parenthesis (<code>(</code>) that follows it on
that line.</li>
<li>Separating any reserved word (such as <code>else</code> or <code>catch</code>) from a closing
curly brace (<code>}</code>) that precedes it on that line.</li>
<li>Before any open curly brace (<code>{</code>), with two exceptions:
<ol>
<li>Before an object literal that is the first argument of a function or the
first element in an array literal (e.g. <code>foo({a: [{c: d}]})</code>).</li>
<li>In a template expansion, as it is forbidden by the language (e.g. valid:
<code>`ab${1 + 2}cd`</code>, invalid: <code class="badcode">`xy$ {3}z`</code>).</li>
</ol></li>
<li>On both sides of any binary or ternary operator.</li>
<li>After a comma (<code>,</code>) or semicolon (<code>;</code>). Note that spaces are <em>never</em> allowed
before these characters.</li>
<li>After the colon (<code>:</code>) in an object literal.</li>
<li>On both sides of the double slash (<code>//</code>) that begins an end-of-line comment.
Here, multiple spaces are allowed, but not required.</li>
<li>After an open-block comment character and on both sides of close characters
(e.g. for short-form type declarations, casts, and parameter name comments:
<code>this.foo = /** @type {number} */ (bar)</code>; or <code>function(/** string */ foo)
{</code>; or <code>baz(/* buzz= */ true)</code>).</li>
</ol>

<h4 id="formatting-horizontal-alignment">4.6.3 Horizontal alignment: discouraged</h4>

<p><strong>Terminology Note</strong>: <em>Horizontal alignment</em> is the practice of adding a
variable number of additional spaces in your code with the goal of making
certain tokens appear directly below certain other tokens on previous lines.</p>

<p>This practice is permitted, but it is <strong>generally discouraged</strong> by Google
Style. It is not even required to <em>maintain</em> horizontal alignment in places
where it was already used.</p>

<p>Here is an example without alignment, followed by one with alignment.  Both are
allowed, but the latter is discouraged:</p>

<pre><code class="language-js prettyprint">{
  tiny: 42, // this is great
  longer: 435, // this too
};

{
  tiny:   42,  // permitted, but future edits
  longer: 435, // may leave it unaligned
};
</code></pre>

<p>Tip: Alignment can aid readability, but it creates problems for future
maintenance. Consider a future change that needs to touch just one line. This
change may leave the formerly-pleasing formatting mangled, and that is
allowed. More often it prompts the coder (perhaps you) to adjust whitespace on
nearby lines as well, possibly triggering a cascading series of
reformattings. That one-line change now has a <q>blast radius.</q> This can at worst
result in pointless busywork, but at best it still corrupts version history
information, slows down reviewers and exacerbates merge conflicts.</p>

<h4 id="formatting-function-arguments">4.6.4 Function arguments</h4>

<p>Prefer to put all function arguments on the same line as the function name. If doing so would exceed the 80-column limit, the arguments must be line-wrapped in a readable way. To save space, you may wrap as close to 80 as possible, or put each argument on its own line to enhance readability. Indentation should be four spaces. Aligning to the parenthesis is allowed, but discouraged. Below are the most common patterns for argument wrapping:</p>

<pre><code class="language-js prettyprint">// Arguments start on a new line, indented four spaces. Preferred when the
// arguments don't fit on the same line with the function name (or the keyword
// "function") but fit entirely on the second line. Works with very long
// function names, survives renaming without reindenting, low on space.
doSomething(
    descriptiveArgumentOne, descriptiveArgumentTwo, descriptiveArgumentThree) {
  // &#8230;
}

// If the argument list is longer, wrap at 80. Uses less vertical space,
// but violates the rectangle rule and is thus not recommended.
doSomething(veryDescriptiveArgumentNumberOne, veryDescriptiveArgumentTwo,
    tableModelEventHandlerProxy, artichokeDescriptorAdapterIterator) {
  // &#8230;
}

// Four-space, one argument per line.  Works with long function names,
// survives renaming, and emphasizes each argument.
doSomething(
    veryDescriptiveArgumentNumberOne,
    veryDescriptiveArgumentTwo,
    tableModelEventHandlerProxy,
    artichokeDescriptorAdapterIterator) {
  // &#8230;
}
</code></pre>

<h3 id="formatting-grouping-parentheses">4.7 Grouping parentheses: recommended</h3>

<p>Optional grouping parentheses are omitted only when the author and reviewer
agree that there is no reasonable chance that the code will be misinterpreted
without them, nor would they have made the code easier to read. It is <em>not</em>
reasonable to assume that every reader has the entire operator precedence table
memorized.</p>

<p>Do not use unnecessary parentheses around the entire expression following
<code>delete</code>, <code>typeof</code>, <code>void</code>, <code>return</code>, <code>throw</code>, <code>case</code>, <code>in</code>, <code>of</code>, or <code>yield</code>.</p>

<p>Parentheses are required for type casts: <code>/** @type {!Foo} */ (foo)</code>.</p>

<h3 id="formatting-comments">4.8 Comments</h3>

<p>This section addresses <em>implementation comments</em>. JSDoc is addressed separately
in <a href="#jsdoc">??</a>.</p>

<h4 id="formatting-block-comment-style">4.8.1 Block comment style</h4>

<p>Block comments are indented at the same level as the surrounding code. They may
be in <code>/* &#8230; */</code> or <code>//</code>-style. For multi-line <code>/* &#8230; */</code> comments, subsequent
lines must start with * aligned with the <code>*</code> on the previous line, to make
comments obvious with no extra context.</p>

<pre><code class="language-js prettyprint">/*
 * This is
 * okay.
 */

// And so
// is this.

/* This is fine, too. */
</code></pre>

<p>Comments are not enclosed in boxes drawn with asterisks or other characters.</p>

<p>Do not use JSDoc (<code>/** &#8230; */</code>) for implementation comments.</p>

<h4 id="formatting-param-name-comments">4.8.2 Parameter Name Comments</h4>

<p>&#8220;Parameter name&#8221; comments should be used whenever the value and method name do
not sufficiently convey the meaning, and refactoring the method to be clearer is
infeasible .
Their preferred format is before the value with <q>=</q>:</p>

<pre><code class="language-js prettyprint">someFunction(obviousParam, /* shouldRender= */ true, /* name= */ 'hello');
</code></pre>

<p>For consistency with surrounding code you may put them after the value without
<q>=</q>:</p>

<pre><code class="language-js prettyprint">someFunction(obviousParam, true /* shouldRender */, 'hello' /* name */);
</code></pre>

<h2 id="language-features">5 Language features</h2>

<p>JavaScript includes many dubious (and even dangerous) features.  This section
delineates which features may or may not be used, and any additional constraints
on their use.</p>

<h3 id="features-local-variable-declarations">5.1 Local variable declarations</h3>

<h4 id="features-use-const-and-let">5.1.1 Use <code>const</code> and <code>let</code></h4>

<p>Declare all local variables with either <code>const</code> or <code>let</code>. Use const by default,
unless a variable needs to be reassigned. The <code class="badcode">var</code>
keyword must not be used.</p>

<h4 id="features-one-variable-per-declaration">5.1.2 One variable per declaration</h4>

<p>Every local variable declaration declares only one variable: declarations such
as <code class="badcode">let a = 1, b = 2;</code> are not used.</p>

<h4 id="features-declared-when-needed">5.1.3 Declared when needed, initialized as soon as possible</h4>

<p>Local variables are <strong>not</strong> habitually declared at the start of their containing
block or block-like construct. Instead, local variables are declared close to
the point they are first used (within reason), to minimize their scope.</p>

<h4 id="features-declare-types-as-needed">5.1.4 Declare types as needed</h4>

<p>JSDoc type annotations may be added either on the line above the declaration, or
else inline before the variable name if no other JSDoc is present.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">const /** !Array&lt;number&gt; */ data = [];

/**
 * Some description.
 * @type {!Array&lt;number&gt;}
 */
const data = [];
</code></pre>

<p>Mixing inline and JSDoc styles is not allowed: the compiler will only process
the first JsDoc and the inline annotations will be lost.</p>

<pre><code class="language-js prettyprint badcode">/** Some description. */
const /** !Array&lt;number&gt; */ data = [];
</code></pre>

<p>Tip: There are many cases where the compiler can infer a templatized type but
not its parameters.  This is particularly the case when the initializing literal
or constructor call does not include any values of the template parameter type
(e.g., empty arrays, objects, <code>Map</code>s, or <code>Set</code>s), or if the variable is modified
in a closure.  Local variable type annotations are particularly helpful in these
cases since otherwise the compiler will infer the template parameter as unknown.</p>

<h3 id="features-array-literals">5.2 Array literals</h3>

<h4 id="features-arrays-trailing-comma">5.2.1 Use trailing commas</h4>



<p>Include a trailing comma whenever there is a line break between the final
element and the closing bracket.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">const values = [
  'first value',
  'second value',
];
</code></pre>

<h4 id="features-arrays-ctor">5.2.2 Do not use the variadic <code>Array</code> constructor</h4>

<p>The constructor is error-prone if arguments are added or removed. Use a literal
instead.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">const a1 = new Array(x1, x2, x3);
const a2 = new Array(x1, x2);
const a3 = new Array(x1);
const a4 = new Array();
</code></pre>

<p>This works as expected except for the third case: if <code>x1</code> is a whole number then
<code>a3</code> is an array of size <code>x1</code> where all elements are <code>undefined</code>. If <code>x1</code> is any
other number, then an exception will be thrown, and if it is anything else then
it will be a single-element array.</p>

<p>Instead, write</p>

<pre><code class="language-js prettyprint">const a1 = [x1, x2, x3];
const a2 = [x1, x2];
const a3 = [x1];
const a4 = [];
</code></pre>

<p>Explicitly allocating an array of a given length using <code>new Array(length)</code> is
allowed when appropriate.</p>

<h4 id="features-arrays-non-numeric-properties">5.2.3 Non-numeric properties</h4>

<p>Do not define or use non-numeric properties on an array (other than
<code>length</code>). Use a <code>Map</code> (or <code>Object</code>) instead.</p>

<h4 id="features-arrays-destructuring">5.2.4 Destructuring</h4>

<p>Array literals may be used on the left-hand side of an assignment to perform
destructuring (such as when unpacking multiple values from a single array or
iterable).  A final <q>rest</q> element may be included (with no space between the
<code>...</code> and the variable name). Elements should be omitted if they are unused.</p>

<pre><code class="language-js prettyprint">const [a, b, c, ...rest] = generateResults();
let [, b,, d] = someArray;
</code></pre>

<p>Destructuring may also be used for function parameters (note that a parameter
name is required but ignored). Always specify <code>[]</code> as the default value if a
destructured array parameter is optional, and provide default values on the left
hand side:</p>

<pre><code class="language-js prettyprint">/** @param {!Array&lt;number&gt;=} param1 */
function optionalDestructuring([a = 4, b = 2] = []) { &#8230; };
</code></pre>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">function badDestructuring([a, b] = [4, 2]) { &#8230; };
</code></pre>

<p>Tip: For (un)packing multiple values into a function&#8217;s parameter or return,
prefer object destructuring to array destructuring when possible, as it allows
naming the individual elements and specifying a different type for each.</p>

<h4 id="features-arrays-spread-operator">5.2.5 Spread operator</h4>

<p>Array literals may include the spread operator (<code>...</code>) to flatten elements out
of one or more other iterables.  The spread operator should be used instead of
more awkward constructs with <code>Array.prototype</code>.  There is no space after the
<code>...</code>.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">[...foo]   // preferred over Array.prototype.slice.call(foo)
[...foo, ...bar]   // preferred over foo.concat(bar)
</code></pre>

<h3 id="features-object-literals">5.3 Object literals</h3>

<h4 id="features-objects-use-trailing-comma">5.3.1 Use trailing commas</h4>

<p>Include a trailing comma whenever there is a line break between the final
property and the closing brace.</p>

<h4 id="features-objects-ctor">5.3.2 Do not use the <code>Object</code> constructor</h4>

<p>While <code>Object</code> does not have the same problems as <code>Array</code>, it is still
disallowed for consistency. Use an object literal (<code>{}</code> or <code>{a: 0, b: 1, c: 2}</code>)
instead.</p>

<h4 id="features-objects-mixing-keys">5.3.3 Do not mix quoted and unquoted keys</h4>

<p>Object literals may represent either <em>structs</em> (with unquoted keys and/or
symbols) or <em>dicts</em> (with quoted and/or computed keys). Do not mix these key
types in a single object literal.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">{
  width: 42, // struct-style unquoted key
  'maxWidth': 43, // dict-style quoted key
}
</code></pre>

<p>This also extends to passing the property name to functions, like
<code>hasOwnProperty</code>. In particular, doing so will break in compiled code because
the compiler cannot rename/obfuscate the string literal.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">/** @type {{width: number, maxWidth: (number|undefined)}} */
const o = {width: 42};
if (o.hasOwnProperty('maxWidth')) {
  ...
}
</code></pre>

<p>This is best implemented as:</p>

<pre><code class="language-js prettyprint">/** @type {{width: number, maxWidth: (number|undefined)}} */
const o = {width: 42};
if (o.maxWidth != null) {
  ...
}
</code></pre>

<h4 id="features-objects-computed-property-names">5.3.4 Computed property names</h4>

<p>Computed property names (e.g., <code>{['key' + foo()]: 42}</code>) are allowed, and are
considered dict-style (quoted) keys (i.e., must not be mixed with non-quoted
keys) unless the computed property is a
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol">symbol</a>
(e.g., <code>[Symbol.iterator]</code>). Enum values may also be used for computed keys, but
should not be mixed with non-enum keys in the same literal.</p>

<h4 id="features-objects-method-shorthand">5.3.5 Method shorthand</h4>

<p>Methods can be defined on object literals using the method shorthand (<code>{method()
{&#8230; }}</code>) in place of a colon immediately followed by a <code>function</code> or arrow
function literal.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">return {
  stuff: 'candy',
  method() {
    return this.stuff;  // Returns 'candy'
  },
};
</code></pre>

<p>Note that <code>this</code> in a method shorthand or <code>function</code> refers to the object
literal itself whereas <code>this</code> in an arrow function refers to the scope outside
the object literal.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">class {
  getObjectLiteral() {
    this.stuff = 'fruit';
    return {
      stuff: 'candy',
      method: () =&gt; this.stuff,  // Returns 'fruit'
    };
  }
}
</code></pre>

<h4 id="features-objects-shorthand-properties">5.3.6 Shorthand properties</h4>

<p>Shorthand properties are allowed on object literals.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">const foo = 1;
const bar = 2;
const obj = {
  foo,
  bar,
  method() { return this.foo + this.bar; },
};
assertEquals(3, obj.method());
</code></pre>

<h4 id="features-objects-destructuring">5.3.7 Destructuring</h4>

<p>Object destructuring patterns may be used on the left-hand side of an assignment
to perform destructuring and unpack multiple values from a single object.</p>

<p>Destructured objects may also be used as function parameters, but should be kept
as simple as possible: a single level of unquoted shorthand properties. Deeper
levels of nesting and computed properties may not be used in parameter
destructuring.  Specify any default values in the left-hand-side of the
destructured parameter (<code>{str = 'some default'} = {}</code>, rather than <code class="badcode">{str} = {str: 'some default'}</code>), and if a destructured
object is itself optional, it must default to <code>{}</code>.  The JSDoc for the
destructured parameter may be given any name (the name is unused but is required
by the compiler).</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">/**
 * @param {string} ordinary
 * @param {{num: (number|undefined), str: (string|undefined)}=} param1
 *     num: The number of times to do something.
 *     str: A string to do stuff to.
 */
function destructured(ordinary, {num, str = 'some default'} = {})
</code></pre>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">/** @param {{x: {num: (number|undefined), str: (string|undefined)}}} param1 */
function nestedTooDeeply({x: {num, str}}) {};
/** @param {{num: (number|undefined), str: (string|undefined)}=} param1 */
function nonShorthandProperty({num: a, str: b} = {}) {};
/** @param {{a: number, b: number}} param1 */
function computedKey({a, b, [a + b]: c}) {};
/** @param {{a: number, b: string}=} param1 */
function nontrivialDefault({a, b} = {a: 2, b: 4}) {};
</code></pre>

<p>Destructuring may also be used for <code>goog.require</code> statements, and in this case
must not be wrapped: the entire statement occupies one line, regardless of how
long it is (see <a href="#file-goog-require">??</a>).</p>

<h4 id="features-objects-enums">5.3.8 Enums</h4>

<p>Enumerations are defined by adding the <code>@enum</code> annotation to an object literal.
Additional properties may not be added to an enum after it is defined.  Enums
must be constant, and all enum values must be deeply immutable.</p>

<pre><code class="language-js prettyprint">/**
 * Supported temperature scales.
 * @enum {string}
 */
const TemperatureScale = {
  CELSIUS: 'celsius',
  FAHRENHEIT: 'fahrenheit',
};

/**
 * An enum with two options.
 * @enum {number}
 */
const Option = {
  /** The option used shall have been the first. */
  FIRST_OPTION: 1,
  /** The second among two options. */
  SECOND_OPTION: 2,
};
</code></pre>

<h3 id="features-classes">5.4 Classes</h3>

<h4 id="features-classes-constructors">5.4.1 Constructors</h4>

<p>Constructors are optional. Subclass constructors must call <code>super()</code> before
setting any fields or otherwise accessing <code>this</code>. Interfaces should declare
non-method properties in the constructor.</p>

<h4 id="features-classes-fields">5.4.2 Fields</h4>

<p>Set all of a concrete object&#8217;s fields (i.e. all properties other than methods)
in the constructor. Annotate fields that are never reassigned with <code>@const</code>
(these need not be deeply immutable). Annotate non-public fields with the proper
visibility annotation (<code>@private</code>, <code>@protected</code>, <code>@package</code>), and end all
<code>@private</code> fields' names with an underscore. Fields are never set on a concrete
class' <code>prototype</code>.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">class Foo {
  constructor() {
    /** @private @const {!Bar} */
    this.bar_ = computeBar();

    /** @protected @const {!Baz} */
    this.baz = computeBaz();
  }
}
</code></pre>

<p>Tip: Properties should never be added to or removed from an instance after the
constructor is finished, since it significantly hinders VMs&#8217; ability to
optimize.  If necessary, fields that are initialized later should be explicitly
set to <code>undefined</code> in the constructor to prevent later shape changes. Adding
<code>@struct</code> to an object will check that undeclared properties are not
added/accessed.  Classes have this added by default.</p>

<h4 id="features-classes-computed-properties">5.4.3 Computed properties</h4>



<p>Computed properties may only be used in classes when the property is a
symbol. Dict-style properties (that is, quoted or computed non-symbol keys, as
defined in <a href="#features-objects-mixing-keys">??</a>) are not allowed.  A
<code>[Symbol.iterator]</code> method should be defined for any classes that are logically
iterable.  Beyond this, <code>Symbol</code> should be used sparingly.</p>

<p>Tip: be careful of using any other built-in symbols (e.g., <code>Symbol.isConcatSpreadable</code>) as they are not polyfilled by the compiler and will therefore not work in older browsers.</p>

<h4 id="features-classes-static-methods">5.4.4 Static methods</h4>



<p>Where it does not interfere with readability, prefer module-local functions over
private static methods.</p>

<p>Static methods should only be called on the base class itself. Static methods
should not be called on variables containing a dynamic instance that may be
either the constructor or a subclass constructor (and must be defined with
<code>@nocollapse</code> if this is done), and must not be called directly on a subclass
that doesn&#8217;t define the method itself.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">class Base { /** @nocollapse */ static foo() {} }
class Sub extends Base {}
function callFoo(cls) { cls.foo(); }  // discouraged: don't call static methods dynamically
Sub.foo();  // Disallowed: don't call static methods on subclasses that don't define it themselves
</code></pre>

<h4 id="features-classes-old-style">5.4.5 Old-style class declarations</h4>

<p>While ES6 classes are preferred, there are cases where ES6 classes may not be
feasible.  For example:</p>

<ol>
<li><p>If there exist or will exist subclasses, including frameworks that create
subclasses, that cannot be immediately changed to use ES6 class syntax. If
such a class were to use ES6 syntax, all downstream subclasses not using ES6
class syntax would need to be modified.</p></li>
<li><p>Frameworks that require a known <code>this</code> value before calling the superclass
constructor, since constructors with ES6 super classes do not have
access to the instance <code>this</code> value until the call to <code>super</code> returns.</p></li>
</ol>

<p>In all other ways the style guide still applies to this code: <code>let</code>, <code>const</code>,
default parameters, rest, and arrow functions should all be used when
appropriate.</p>

<p><code>goog.defineClass</code> allows for a class-like definition similar to ES6 class
syntax:</p>

<pre><code class="language-javascript">let C = goog.defineClass(S, {
  /**
   * @param {string} value
   */
  constructor(value) {
    S.call(this, 2);
    /** @const */
    this.prop = value;
  },

  /**
   * @param {string} param
   * @return {number}
   */
  method(param) {
    return 0;
  },
});
</code></pre>

<p>Alternatively, while <code>goog.defineClass</code> should be preferred for all new code,
more traditional syntax is also allowed.</p>

<pre><code class="language-javascript">/**
  * @constructor @extends {S}
  * @param {string} value
  */
function C(value) {
  S.call(this, 2);
  /** @const */
  this.prop = value;
}
goog.inherits(C, S);

/**
 * @param {string} param
 * @return {number}
 */
C.prototype.method = function(param) {
  return 0;
};
</code></pre>

<p>Per-instance properties should be defined in the constructor after the call to the super class constructor, if there is a super class.  Methods should be defined on the prototype of the constructor.</p>

<p>Defining constructor prototype hierarchies correctly is harder than it first appears!  For that reason, it is best to use <code>goog.inherits</code> from <a href="http://code.google.com/closure/library/">the Closure Library </a>.</p>

<h4 id="features-classes-prototypes">5.4.6 Do not manipulate <code>prototype</code>s directly</h4>

<p>The <code>class</code> keyword allows clearer and more readable class definitions than
defining <code>prototype</code> properties. Ordinary implementation code has no business
manipulating these objects, though they are still useful for defining classes as
defined in <a href="#features-classes-old-style">??</a>. Mixins and modifying the
prototypes of builtin objects are explicitly forbidden.</p>

<p><strong>Exception</strong>: Framework code (such as Polymer, or Angular) may need to use <code>prototype</code>s, and should not
resort to even-worse workarounds to avoid doing so.</p>

<h4 id="features-classes-getters-and-setters">5.4.7 Getters and Setters</h4>

<p>Do not use <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get">JavaScript getter and setter properties</a>.  They are potentially
surprising and difficult to reason about, and have limited support in the
compiler.  Provide ordinary methods instead.</p>

<p><strong>Exception</strong>: there are situations where defining a getter or setter is
unavoidable (e.g. data binding frameworks such as Angular and Polymer, or for
compatibility with external APIs that cannot be adjusted).  In these cases only,
getters and setters may be used <em>with caution</em>, provided they are defined with
the <code>get</code> and <code>set</code> shorthand method keywords or <code>Object.defineProperties</code> (not
<code>Object.defineProperty</code>, which interferes with property renaming).  Getters
<strong>must not</strong> change observable state.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">class Foo {
  get next() { return this.nextId++; }
}
</code></pre>

<h4 id="features-classes-overriding-tostring">5.4.8 Overriding toString</h4>

<p>The <code>toString</code> method may be overridden, but must always succeed and never have
visible side effects.</p>

<p>Tip: Beware, in particular, of calling other methods from toString, since
exceptional conditions could lead to infinite loops.</p>

<h4 id="features-classes-interfaces">5.4.9 Interfaces</h4>

<p>Interfaces may be declared with <code>@interface</code> or <code>@record</code>. Interfaces declared
with <code>@record</code> can be explicitly (i.e. via <code>@implements</code>) or implicitly
implemented by a class or object literal.</p>

<p>All non-static method bodies on an interface must be empty blocks. Fields must
be declared as uninitialized members in the class constructor.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">/**
 * Something that can frobnicate.
 * @record
 */
class Frobnicator {
  constructor() {
    /** @type {number} The number of attempts before giving up. */
    this.attempts;
  }

  /**
   * Performs the frobnication according to the given strategy.
   * @param {!FrobnicationStrategy} strategy
   */
  frobnicate(strategy) {}
}

</code></pre>

<h4 id="features-classes-abstract-classes">5.4.10 Abstract Classes</h4>

<p>Use abstract classes when appropriate. Abstract classes and methods must be
annotated with <code>@abstract</code>. Do not use <code>goog.abstractMethod</code>. See <a href="https://github.com/google/closure-compiler/wiki/@abstract-classes-and-methods">abstract
classes and methods</a>.</p>

<h3 id="features-functions">5.5 Functions</h3>

<h4 id="features-functions-top-level-functions">5.5.1 Top-level functions</h4>

<p>Top-level functions may be defined directly on the <code>exports</code> object, or else
declared locally and optionally exported. See <a href="#file-goog-module-exports">??</a>
for more on exports.</p>

<p>Examples:</p>

<pre><code class="language-js prettyprint">/** @param {string} str */
exports.processString = (str) =&gt; {
  // Process the string.
};
</code></pre>

<pre><code class="language-js prettyprint">/** @param {string} str */
const processString = (str) =&gt; {
  // Process the string.
};

exports = {processString};
</code></pre>

<h4 id="features-functions-nested-functions">5.5.2 Nested functions and closures</h4>

<p>Functions may contain nested function definitions.  If it is useful to give the
function a name, it should be assigned to a local <code>const</code>.</p>

<h4 id="features-functions-arrow-functions">5.5.3 Arrow functions</h4>

<p>Arrow functions provide a concise function syntax and simplify scoping <code>this</code>
for nested functions. Prefer arrow functions over the <code>function</code> keyword,
particularly for nested functions (but see
<a href="#features-objects-method-shorthand">??</a>).</p>

<p>Prefer arrow functions over other <code>this</code> scoping approaches such as
<code>f.bind(this)</code>, <code>goog.bind(f, this)</code>, and <code>const self = this</code>. Arrow functions
are particularly useful for calling into callbacks as they permit explicitly
specifying which parameters to pass to the callback whereas binding will blindly
pass along all parameters.</p>

<p>The left-hand side of the arrow contains zero or more parameters. Parentheses
around the parameters are optional if there is only a single non-destructured
parameter. When parentheses are used, inline parameter types may be specified
(see <a href="#jsdoc-method-and-function-comments">??</a>).</p>

<p>Tip: Always using parentheses even for single-parameter arrow functions can
avoid situations where adding parameters, but forgetting to add parentheses, may
result in parseable code which no longer works as intended.</p>

<p>The right-hand side of the arrow contains the body of the function. By default
the body is a block statement (zero or more statements surrounded by curly
braces). The body may also be an implicitly returned single expression if
either: the program logic requires returning a value, or the <code>void</code> operator
precedes a single function or method call (using <code>void</code> ensures <code>undefined</code> is
returned, prevents leaking values, and communicates intent). The single
expression form is preferred if it improves readability (e.g., for short or
simple expressions).</p>

<p>Examples:</p>

<pre><code class="language-js prettyprint">/**
 * Arrow functions can be documented just like normal functions.
 * @param {number} numParam A number to add.
 * @param {string} strParam Another number to add that happens to be a string.
 * @return {number} The sum of the two parameters.
 */
const moduleLocalFunc = (numParam, strParam) =&gt; numParam + Number(strParam);

// Uses the single expression syntax with `void` because the program logic does
// not require returning a value.
getValue((result) =&gt; void alert(`Got ${result}`));

class CallbackExample {
  constructor() {
    /** @private {number} */
    this.cachedValue_ = 0;

    // For inline callbacks, you can use inline typing for parameters.
    // Uses a block statement because the value of the single expression should
    // not be returned and the expression is not a single function call.
    getNullableValue((/** ?number */ result) =&gt; {
      this.cachedValue_ = result == null ? 0 : result;
    });
  }
}
</code></pre>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">/**
 * A function with no params and no returned value.
 * This single expression body usage is illegal because the program logic does
 * not require returning a value and we're missing the `void` operator.
 */
const moduleLocalFunc = () =&gt; anotherFunction();
</code></pre>

<h4 id="features-functions-generators">5.5.4 Generators</h4>

<p>Generators enable a number of useful abstractions and may be used as needed.</p>

<p>When defining generator functions, attach the <code>*</code> to the <code>function</code> keyword when
present, and separate it with a space from the name of the function.  When using
delegating yields, attach the <code>*</code> to the <code>yield</code> keyword.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">/** @return {!Iterator&lt;number&gt;} */
function* gen1() {
  yield 42;
}

/** @return {!Iterator&lt;number&gt;} */
const gen2 = function*() {
  yield* gen1();
}

class SomeClass {
  /** @return {!Iterator&lt;number&gt;} */
  * gen() {
    yield 42;
  }
}
</code></pre>

<h4 id="features-functions-parameter-return-types">5.5.5 Parameter and return types</h4>

<p>Function parameters and return types should usually be documented with JSDoc
annotations. See <a href="#jsdoc-method-and-function-comments">??</a> for more information.</p>

<h5 id="features-functions-default-parameters">5.5.5.1 Default parameters</h5>

<p>Optional parameters are permitted using the equals operator in the parameter
list. Optional parameters must include spaces on both sides of the equals
operator, be named exactly like required parameters (i.e., not prefixed with
<code>opt_</code>), use the <code>=</code> suffix in their JSDoc type, come after required parameters,
and not use initializers that produce observable side effects. All optional
parameters for concrete functions must have default values, even if that value
is <code>undefined</code>. In contrast to concrete functions, abstract and interface
methods must omit default parameter values.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">/**
 * @param {string} required This parameter is always needed.
 * @param {string=} optional This parameter can be omitted.
 * @param {!Node=} node Another optional parameter.
 */
function maybeDoSomething(required, optional = '', node = undefined) {}

/** @interface */
class MyInterface {
  /**
   * Interface and abstract methods must omit default parameter values.
   * @param {string=} optional
   */
  someMethod(optional) {}
}
</code></pre>

<p>Use default parameters sparingly. Prefer destructuring (as in
<a href="#features-objects-destructuring">??</a>) to create readable APIs when there
are more than a small handful of optional parameters that do not have a natural
order.</p>

<p>Note: Unlike Python's default parameters, it is okay to use initializers that
return new mutable objects (such as <code>{}</code> or <code>[]</code>) because the initializer is
evaluated each time the default value is used, so a single object won't be
shared across invocations.</p>

<p>Tip: While arbitrary expressions including function calls may be used as
initializers, these should be kept as simple as possible. Avoid initializers
that expose shared mutable state, as that can easily introduce unintended
coupling between function calls.</p>

<h5 id="features-functions-rest-parameters">5.5.5.2 Rest parameters</h5>

<p>Use a <em>rest</em> parameter instead of accessing <code>arguments</code>. Rest parameters are
typed with a <code>...</code> prefix in their JSDoc. The rest parameter must be the last
parameter in the list. There is no space between the <code>...</code> and the parameter
name.  Do not name the rest parameter <code>var_args</code>. Never name a local variable or
parameter <code>arguments</code>, which confusingly shadows the built-in name.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">/**
 * @param {!Array&lt;string&gt;} array This is an ordinary parameter.
 * @param {...number} numbers The remainder of arguments are all numbers.
 */
function variadic(array, ...numbers) {}
</code></pre>

<h4 id="features-functions-generics">5.5.6 Generics</h4>

<p>Declare generic functions and methods when necessary with <code>@template TYPE</code> in
the JSDoc above the function or method definition.</p>

<h4 id="features-functions-spread-operator">5.5.7 Spread operator</h4>

<p>Function calls may use the spread operator (<code>...</code>).  Prefer the spread operator
to <code>Function.prototype.apply</code> when an array or iterable is unpacked into
multiple parameters of a variadic function.  There is no space after the <code>...</code>.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">function myFunction(...elements) {}
myFunction(...array, ...iterable, ...generator());
</code></pre>

<h3 id="features-string-literals">5.6 String literals</h3>

<h4 id="features-strings-use-single-quotes">5.6.1 Use single quotes</h4>

<p>Ordinary string literals are delimited with single quotes (<code>'</code>), rather than
double quotes (<code>"</code>).</p>

<p>Tip: if a string contains a single quote character, consider using a template
string to avoid having to escape the quote.</p>

<p>Ordinary string literals may not span multiple lines.</p>

<h4 id="features-strings-template-strings">5.6.2 Template literals</h4>

<p>Use template literals (delimited with <code>`</code>) over complex string
concatenation, particularly if multiple string literals are involved. Template
literals may span multiple lines.</p>

<p>If a template literal spans multiple lines, it does not need to follow the
indentation of the enclosing block, though it may if the added whitespace does
not matter.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">function arithmetic(a, b) {
  return `Here is a table of arithmetic operations:
${a} + ${b} = ${a + b}
${a} - ${b} = ${a - b}
${a} * ${b} = ${a * b}
${a} / ${b} = ${a / b}`;
}
</code></pre>

<h4 id="features-strings-no-line-continuations">5.6.3 No line continuations</h4>

<p>Do not use <em>line continuations</em> (that is, ending a line inside a string literal
with a backslash) in either ordinary or template string literals. Even though
ES5 allows this, it can lead to tricky errors if any trailing whitespace comes
after the slash, and is less obvious to readers.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">const longString = 'This is a very long string that far exceeds the 80 \
    column limit. It unfortunately contains long stretches of spaces due \
    to how the continued lines are indented.';
</code></pre>

<p>Instead, write</p>

<pre><code class="language-js prettyprint">const longString = 'This is a very long string that far exceeds the 80 ' +
    'column limit. It does not contain long stretches of spaces since ' +
    'the concatenated strings are cleaner.';
</code></pre>

<h3 id="features-number-literals">5.7 Number literals</h3>

<p>Numbers may be specified in decimal, hex, octal, or binary.  Use exactly <code>0x</code>,
<code>0o</code>, and <code>0b</code> prefixes, with lowercase letters, for hex, octal, and binary,
respectively.  Never include a leading zero unless it is immediately followed by
<code>x</code>, <code>o</code>, or <code>b</code>.</p>

<h3 id="features-control-structures">5.8 Control structures</h3>

<h4 id="features-for-loops">5.8.1 For loops</h4>

<p>With ES6, the language now has three different kinds of <code>for</code> loops.  All may be
used, though <code>for</code>-<code>of</code> loops should be preferred when possible.</p>

<p><code>for</code>-<code>in</code> loops may only be used on dict-style objects (see
<a href="#features-objects-mixing-keys">??</a>), and should not be used to iterate over an
array.  <code>Object.prototype.hasOwnProperty</code> should be used in <code>for</code>-<code>in</code> loops to
exclude unwanted prototype properties.  Prefer <code>for</code>-<code>of</code> and <code>Object.keys</code> over
<code>for</code>-<code>in</code> when possible.</p>

<h4 id="features-exceptions">5.8.2 Exceptions</h4>

<p>Exceptions are an important part of the language and should be used whenever
exceptional cases occur.  Always throw <code>Error</code>s or subclasses of <code>Error</code>: never
throw string literals or other objects.  Always use <code>new</code> when constructing an
<code>Error</code>.</p>

<p>This treatment extends to <code>Promise</code> rejection values as <code>Promise.reject(obj)</code> is
equivalent to <code>throw obj;</code> in async functions.</p>

<p>Custom exceptions provide a great way to convey additional error information
from functions.  They should be defined and used wherever the native <code>Error</code>
type is insufficient.</p>

<p>Prefer throwing exceptions over ad-hoc error-handling approaches (such as
passing an error container reference type, or returning an object with an error
property).</p>

<h5 id="features-empty-catch-blocks">5.8.2.1 Empty catch blocks</h5>

<p>It is very rarely correct to do nothing in response to a caught exception. When
it truly is appropriate to take no action whatsoever in a catch block, the
reason this is justified is explained in a comment.</p>

<pre><code class="language-js prettyprint">try {
  return handleNumericResponse(response);
} catch (ok) {
  // it's not numeric; that's fine, just continue
}
return handleTextResponse(response);
</code></pre>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">  try {
    shouldFail();
    fail('expected an error');
  } catch (expected) {
  }
</code></pre>

<p>Tip: Unlike in some other languages, patterns like the above simply don&#8217;t work
since this will catch the error thrown by <code>fail</code>. Use <code>assertThrows()</code> instead.</p>

<h4 id="features-switch-statements">5.8.3 Switch statements</h4>

<p>Terminology Note: Inside the braces of a switch block are one or more statement groups. Each statement group consists of one or more switch labels (either <code>case FOO:</code> or <code>default:</code>), followed by one or more statements.</p>

<h5 id="features-switch-fall-through">5.8.3.1 Fall-through: commented</h5>

<p>Within a switch block, each statement group either terminates abruptly (with a
<code>break</code>, <code>return</code> or <code>throw</code>n exception), or is marked with a comment to
indicate that execution will or might continue into the next statement
group. Any comment that communicates the idea of fall-through is sufficient
(typically <code>// fall through</code>). This special comment is not required in the last
statement group of the switch block.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">switch (input) {
  case 1:
  case 2:
    prepareOneOrTwo();
  // fall through
  case 3:
    handleOneTwoOrThree();
    break;
  default:
    handleLargeNumber(input);
}
</code></pre>

<h5 id="features-switch-default-case">5.8.3.2 The <code>default</code> case is present</h5>

<p>Each switch statement includes a <code>default</code> statement group, even if it contains
no code. The <code>default</code> statement group must be last.</p>

<h3 id="features-this">5.9 this</h3>

<p>Only use <code>this</code> in class constructors and methods, in arrow functions defined
within class constructors and methods, or in functions that have an explicit
<code>@this</code> declared in the immediately-enclosing function&#8217;s JSDoc.</p>

<p>Never use <code>this</code> to refer to the global object, the context of an <code>eval</code>, the
target of an event, or unnecessarily <code>call()</code>ed or <code>apply()</code>ed functions.</p>

<h3 id="features-equality-checks">5.10 Equality Checks</h3>

<p>Use identity operators (<code>===</code>/<code>!==</code>) except in the cases documented below.</p>

<h4 id="features-equality-checks-exceptions">5.10.1 Exceptions Where Coercion is Desirable</h4>

<p>Catching both <code>null</code> and <code>undefined</code> values:</p>

<pre><code class="language-js prettyprint">if (someObjectOrPrimitive == null) {
  // Checking for null catches both null and undefined for objects and
  // primitives, but does not catch other falsy values like 0 or the empty
  // string.
}
</code></pre>

<h3 id="disallowed-features">5.11 Disallowed features</h3>

<h4 id="disallowed-features-with">5.11.1 with</h4>

<p>Do not use the <code>with</code> keyword.  It makes your code harder to understand and has
been banned in strict mode since ES5.</p>

<h4 id="disallowed-features-dynamic-code-evaluation">5.11.2 Dynamic code evaluation</h4>

<p>Do not use <code>eval</code> or the <code>Function(...string)</code> constructor (except for code
loaders).  These features are potentially dangerous and simply do not work in
CSP environments.</p>

<h4 id="disallowed-features-automatic-semicolon-insertion">5.11.3 Automatic semicolon insertion</h4>

<p>Always terminate statements with semicolons (except function and class
declarations, as noted above).</p>

<h4 id="disallowed-features-non-standard-features">5.11.4 Non-standard features</h4>

<p>Do not use non-standard features.  This includes old features that have been
removed (e.g., <code>WeakMap.clear</code>), new features that are not yet standardized
(e.g., the current TC39 working draft, proposals at any stage, or proposed but
not-yet-complete web standards), or proprietary features that are only
implemented in some browsers.  Use only features defined in the current ECMA-262
or WHATWG standards.  (Note that projects writing against specific APIs, such as
Chrome extensions or Node.js, can obviously use those APIs).  Non-standard
language &#8220;extensions&#8221; (such as those provided by some external transpilers) are
forbidden.</p>

<h4 id="disallowed-features-wrapper-objects">5.11.5 Wrapper objects for primitive types</h4>

<p>Never use <code>new</code> on the primitive object wrappers (<code>Boolean</code>, <code>Number</code>, <code>String</code>,
<code>Symbol</code>), nor include them in type annotations.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">const /** Boolean */ x = new Boolean(false);
if (x) alert(typeof x);  // alerts 'object' - WAT?
</code></pre>

<p>The wrappers may be called as functions for coercing (which is preferred over
using <code>+</code> or concatenating the empty string) or creating symbols.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">const /** boolean */ x = Boolean(0);
if (!x) alert(typeof x);  // alerts 'boolean', as expected
</code></pre>

<h4 id="disallowed-features-modifying-builtin-objects">5.11.6 Modifying builtin objects</h4>

<p>Never modify builtin types, either by adding methods to their constructors or to
their prototypes.  Avoid depending on libraries that do this.  Note that the
JSCompiler&#8217;s runtime library will provide standards-compliant polyfills where
possible; nothing else may modify builtin objects.</p>

<p>Do not add symbols to the global object unless absolutely necessary
(e.g. required by a third-party API).</p>

<h4 id="disallowed-features-omitting-parents-with-new">5.11.7 Omitting <code>()</code> when invoking a constructor</h4>

<p>Never invoke a constructor in a <code>new</code> statement without using parentheses <code>()</code>.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">new Foo;
</code></pre>

<p>Use instead:</p>

<pre><code class="language-js prettyprint">new Foo();
</code></pre>

<p>Omitting parentheses can lead to subtle mistakes. These two lines are not
equivalent:</p>

<pre><code class="language-js prettyprint">new Foo().Bar();
new Foo.Bar();
</code></pre>

<h2 id="naming">6 Naming</h2>

<h3 id="naming-rules-common-to-all-identifiers">6.1 Rules common to all identifiers</h3>

<p>Identifiers use only ASCII letters and digits, and, in a small number of cases
noted below, underscores and very rarely (when required by frameworks like
Angular) dollar signs.</p>

<p>Give as descriptive a name as possible, within reason. Do not worry about saving
horizontal space as it is far more important to make your code immediately
understandable by a new reader. Do not use abbreviations that are ambiguous or
unfamiliar to readers outside your project, and do not abbreviate by deleting
letters within a word.</p>

<pre><code class="language-js prettyprint">errorCount          // No abbreviation.
dnsConnectionIndex  // Most people know what "DNS" stands for.
referrerUrl         // Ditto for "URL".
customerId          // "Id" is both ubiquitous and unlikely to be misunderstood.
</code></pre>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">n                   // Meaningless.
nErr                // Ambiguous abbreviation.
nCompConns          // Ambiguous abbreviation.
wgcConnections      // Only your group knows what this stands for.
pcReader            // Lots of things can be abbreviated "pc".
cstmrId             // Deletes internal letters.
kSecondsPerDay      // Do not use Hungarian notation.
</code></pre>

<h3 id="naming-rules-by-identifier-type">6.2 Rules by identifier type</h3>

<h4 id="naming-package-names">6.2.1 Package names</h4>

<p>Package names are all <code>lowerCamelCase</code>. For example,
<code>my.exampleCode.deepSpace</code>, but not <code class="badcode">my.examplecode.deepspace</code> or <code class="badcode">my.example_code.deep_space</code>.</p>

<h4 id="naming-class-names">6.2.2 Class names</h4>

<p>Class, interface, record, and typedef names are written in <code>UpperCamelCase</code>.
Unexported classes are simply locals: they are not marked <code>@private</code> and
therefore are not named with a trailing underscore.</p>

<p>Type names are typically nouns or noun phrases. For example, <code>Request</code>,
<code>ImmutableList</code>, or <code>VisibilityMode</code>.  Additionally, interface names may
sometimes be adjectives or adjective phrases instead (for example, <code>Readable</code>).</p>

<h4 id="naming-method-names">6.2.3 Method names</h4>

<p>Method names are written in <code>lowerCamelCase</code>. Names for <code>@private</code> methods must
end with a trailing underscore.</p>

<p>Method names are typically verbs or verb phrases. For example, <code>sendMessage</code> or
<code>stop_</code>.  Getter and setter methods for properties are never required, but if
they are used they should be named <code>getFoo</code> (or optionally <code>isFoo</code> or <code>hasFoo</code>
for booleans), or <code>setFoo(value)</code> for setters.</p>

<p>Underscores may also appear in JsUnit test method names to separate logical
components of the name. One typical pattern is
<code>test&lt;MethodUnderTest&gt;_&lt;state&gt;_&lt;expectedOutcome&gt;</code>, for example
<code>testPop_emptyStack_throws</code>. There is no One Correct Way to name test methods.</p>

<h4 id="naming-enum-names">6.2.4 Enum names</h4>

<p>Enum names are written in <code>UpperCamelCase</code>, similar to classes, and should
generally be singular nouns.  Individual items within the enum are named in
<code>CONSTANT_CASE</code>.</p>

<h4 id="naming-constant-names">6.2.5 Constant names</h4>

<p>Constant names use <code>CONSTANT_CASE</code>: all uppercase letters, with words separated
by underscores. There is no reason for a constant to be named with a trailing
underscore, since private static properties can be replaced by (implicitly
private) module locals.</p>

<h5 id="naming-definition-of-constant">6.2.5.1 Definition of &#8220;constant&#8221;</h5>

<p>Every constant is a <code>@const</code> static property or a module-local <code>const</code>
declaration, but not all <code>@const</code> static properties and module-local <code>const</code>s
are constants. Before choosing constant case, consider whether the field really
feels like a <em>deeply immutable</em> constant. For example, if any of that instance's
observable state can change, it is almost certainly not a constant. Merely
intending to never mutate the object is generally not enough.</p>

<p>Examples:</p>

<pre><code class="language-js prettyprint">// Constants
const NUMBER = 5;
/** @const */ exports.NAMES = ImmutableList.of('Ed', 'Ann');
/** @enum */ exports.SomeEnum = { ENUM_CONSTANT: 'value' };

// Not constants
let letVariable = 'non-const';
class MyClass { constructor() { /** @const {string} */ this.nonStatic = 'non-static'; } };
/** @type {string} */ MyClass.staticButMutable = 'not @const, can be reassigned';
const /** Set&lt;string&gt; */ mutableCollection = new Set();
const /** ImmutableSet&lt;SomeMutableType&gt; */ mutableElements = ImmutableSet.of(mutable);
const Foo = goog.require('my.Foo');  // mirrors imported name
const logger = log.getLogger('loggers.are.not.immutable');
</code></pre>

<p>Constants&#8217; names are typically nouns or noun phrases.</p>

<h5 id="naming-local-aliases">6.2.5.2 Local aliases</h5>

<p>Local aliases should be used whenever they improve readability over
fully-qualified names.  Follow the same rules as <code>goog.require</code>s
(<a href="#file-goog-require">??</a>), maintaining the last part of the aliased name.
Aliases may also be used within functions.  Aliases must be <code>const</code>.</p>

<p>Examples:</p>

<pre><code class="language-js prettyprint">const staticHelper = importedNamespace.staticHelper;
const CONSTANT_NAME = ImportedClass.CONSTANT_NAME;
const {assert, assertInstanceof} = asserts;
</code></pre>

<h4 id="naming-non-constant-field-names">6.2.6 Non-constant field names</h4>

<p>Non-constant field names (static or otherwise) are written in <code>lowerCamelCase</code>,
with a trailing underscore for private fields.</p>

<p>These names are typically nouns or noun phrases. For example, <code>computedValues</code>
or <code>index_</code>.</p>

<h4 id="naming-parameter-names">6.2.7 Parameter names</h4>

<p>Parameter names are written in <code>lowerCamelCase</code>.  Note that this applies even if
the parameter expects a constructor.</p>

<p>One-character parameter names should not be used in public methods.</p>

<p><strong>Exception</strong>: When required by a third-party framework, parameter names may
begin with a <code>$</code>.  This exception does not apply to any other identifiers
(e.g. local variables or properties).</p>

<h4 id="naming-local-variable-names">6.2.8 Local variable names</h4>

<p>Local variable names are written in <code>lowerCamelCase</code>, except for module-local
(top-level) constants, as described above. Constants in function scopes are
still named in <code>lowerCamelCase</code>. Note that <code>lowerCamelCase</code> is used
even if the variable holds a constructor.</p>

<h4 id="naming-template-parameter-names">6.2.9 Template parameter names</h4>

<p>Template parameter names should be concise, single-word or single-letter
identifiers, and must be all-caps, such as <code>TYPE</code> or <code>THIS</code>.</p>

<h4 id="naming-module-local-names">6.2.10 Module-local names</h4>

<p>Module-local names that are not exported are implicitly private. They are not
marked <code>@private</code> and do not end in an underscore. This applies to classes,
functions, variables, constants, enums, and other module-local identifiers.</p>

<h3 id="naming-camel-case-defined">6.3 Camel case: defined</h3>

<p>Sometimes there is more than one reasonable way to convert an English phrase
into camel case, such as when acronyms or unusual constructs like <q>IPv6</q> or
<q>iOS</q> are present. To improve predictability, Google Style specifies the
following (nearly) deterministic scheme.</p>

<p>Beginning with the prose form of the name:</p>

<ol>
<li>Convert the phrase to plain ASCII and remove any apostrophes. For example,
<q>M&#252;ller's algorithm</q> might become <q>Muellers algorithm</q>.</li>
<li>Divide this result into words, splitting on spaces and any remaining
punctuation (typically hyphens).
<ol>
<li>Recommended: if any word already has a conventional camel case
appearance in common usage, split this into its constituent parts (e.g.,
<q>AdWords</q> becomes <q>ad words</q>). Note that a word such as <q>iOS</q> is not
really in camel case per se; it defies any convention, so this
recommendation does not apply.</li>
</ol></li>
<li>Now lowercase everything (including acronyms), then uppercase only the first
character of:
<ol>
<li>&#8230; each word, to yield upper camel case, or</li>
<li>&#8230; each word except the first, to yield lower camel case</li>
</ol></li>
<li>Finally, join all the words into a single identifier.</li>
</ol>

<p>Note that the casing of the original words is almost entirely disregarded.</p>

<p>Examples:</p>

<table>
<thead>
<tr>
<th style="text-align: center">Prose form</th>
<th style="text-align: center">Correct</th>
<th style="text-align: center">Incorrect</th>
</tr>
</thead>

<tbody>
<tr>
<td style="text-align: center"><q>XML HTTP request</q></td>
<td style="text-align: center">XmlHttpRequest</td>
<td style="text-align: center">XMLHTTPRequest</td>
</tr>
<tr>
<td style="text-align: center"><q>new customer ID</q></td>
<td style="text-align: center">newCustomerId</td>
<td style="text-align: center">newCustomerID</td>
</tr>
<tr>
<td style="text-align: center"><q>inner stopwatch</q></td>
<td style="text-align: center">innerStopwatch</td>
<td style="text-align: center">innerStopWatch</td>
</tr>
<tr>
<td style="text-align: center"><q>supports IPv6 on iOS?</q></td>
<td style="text-align: center">supportsIpv6OnIos</td>
<td style="text-align: center">supportsIPv6OnIOS</td>
</tr>
<tr>
<td style="text-align: center"><q>YouTube importer</q></td>
<td style="text-align: center">YouTubeImporter</td>
<td style="text-align: center">YoutubeImporter*</td>
</tr>
</tbody>
</table>

<p>*Acceptable, but not recommended.</p>

<p>Note: Some words are ambiguously hyphenated in the English language: for example <q>nonempty</q> and <q>non-empty</q> are both correct, so the method names checkNonempty and checkNonEmpty are likewise both correct.</p>

<h2 id="jsdoc">7 JSDoc</h2>

<p><a href="https://developers.google.com/closure/compiler/docs/js-for-compiler">JSDoc</a> is used on all classes, fields, and methods.</p>

<h3 id="jsdoc-general-form">7.1 General form</h3>

<p>The basic formatting of JSDoc blocks is as seen in this example:</p>

<pre><code class="language-js prettyprint">/**
 * Multiple lines of JSDoc text are written here,
 * wrapped normally.
 * @param {number} arg A number to do something to.
 */
function doSomething(arg) { &#8230; }
</code></pre>

<p>or in this single-line example:</p>

<pre><code class="language-js prettyprint">/** @const @private {!Foo} A short bit of JSDoc. */
this.foo_ = foo;
</code></pre>

<p>If a single-line comment overflows into multiple lines, it must use the
multi-line style with <code>/**</code> and <code>*/</code> on their own lines.</p>

<p>Many tools extract metadata from JSDoc comments to perform code validation and
optimization.  As such, these comments <strong>must</strong> be well-formed.</p>

<h3 id="jsdoc-markdown">7.2 Markdown</h3>

<p>JSDoc is written in Markdown, though it may include HTML when necessary.</p>

<p>Note that tools that automatically extract JSDoc (e.g. <a href="https://github.com/jleyba/js-dossier">JsDossier</a>) will often
ignore plain text formatting, so if you did this:</p>

<pre><code class="language-js prettyprint badcode">/**
 * Computes weight based on three factors:
 *   items sent
 *   items received
 *   last timestamp
 */
</code></pre>

<p>it would come out like this:</p>

<pre><code>Computes weight based on three factors: items sent items received last timestamp
</code></pre>

<p>Instead, write a Markdown list:</p>

<pre><code class="language-js prettyprint">/**
 * Computes weight based on three factors:
 *
 *  - items sent
 *  - items received
 *  - last timestamp
 */
</code></pre>

<h3 id="jsdoc-tags">7.3 JSDoc tags</h3>

<p>Google style allows a subset of JSDoc tags.  See
<a href="#appendices-jsdoc-tag-reference">??</a> for the complete list.  Most tags must
occupy their own line, with the tag at the beginning of the line.</p>

<p>Disallowed:</p>

<pre><code class="language-js prettyprint badcode">/**
 * The "param" tag must occupy its own line and may not be combined.
 * @param {number} left @param {number} right
 */
function add(left, right) { ... }
</code></pre>

<p>Simple tags that do not require any additional data (such as <code>@private</code>,
<code>@const</code>, <code>@final</code>, <code>@export</code>) may be combined onto the same line, along with an
optional type when appropriate.</p>

<pre><code class="language-js prettyprint">/**
 * Place more complex annotations (like "implements" and "template")
 * on their own lines.  Multiple simple tags (like "export" and "final")
 * may be combined in one line.
 * @export @final
 * @implements {Iterable&lt;TYPE&gt;}
 * @template TYPE
 */
class MyClass {
  /**
   * @param {!ObjType} obj Some object.
   * @param {number=} num An optional number.
   */
  constructor(obj, num = 42) {
    /** @private @const {!Array&lt;!ObjType|number&gt;} */
    this.data_ = [obj, num];
  }
}
</code></pre>

<p>There is no hard rule for when to combine tags, or in which order, but be
consistent.</p>

<p>For general information about annotating types in JavaScript see
<a href="https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler">Annotating JavaScript for the Closure Compiler</a> and <a href="https://github.com/google/closure-compiler/wiki/Types-in-the-Closure-Type-System">Types in the Closure Type
System</a>.</p>

<h3 id="jsdoc-line-wrapping">7.4 Line wrapping</h3>

<p>Line-wrapped block tags are indented four spaces.  Wrapped description text may
be lined up with the description on previous lines, but this horizontal
alignment is discouraged.</p>

<pre><code class="language-js prettyprint">/**
 * Illustrates line wrapping for long param/return descriptions.
 * @param {string} foo This is a param with a description too long to fit in
 *     one line.
 * @return {number} This returns something that has a description too long to
 *     fit in one line.
 */
exports.method = function(foo) {
  return 5;
};
</code></pre>

<p>Do not indent when wrapping a <code>@desc</code> or <code>@fileoverview</code> description.</p>

<h3 id="jsdoc-top-file-level-comments">7.5 Top/file-level comments</h3>

<p>A file may have a top-level file overview. A copyright notice , author information, and
default <a href="#jsdoc-visibility-annotations">visibility level</a> are optional.  File overviews are generally recommended whenever a
file consists of more than a single class definition. The top level comment is
designed to orient readers unfamiliar with the code to what is in this file. If
present, it may provide a description of the file's contents and any
dependencies or compatibility information. Wrapped lines are not indented.</p>

<p>Example:</p>

<pre><code class="language-js prettyprint">/**
 * @fileoverview Description of file, its uses and information
 * about its dependencies.
 * @package
 */
</code></pre>

<h3 id="jsdoc-class-comments">7.6 Class comments</h3>

<p>Classes, interfaces and records must be documented with a description and any
template parameters, implemented interfaces, visibility, or other appropriate
tags. The class description should provide the reader with enough information to
know how and when to use the class, as well as any additional considerations
necessary to correctly use the class. Textual descriptions may be omitted on the
constructor. <code>@constructor</code> and <code>@extends</code> annotations are not used with the
<code>class</code> keyword unless the class is being used to declare an <code>@interface</code> or
it extends a generic class.</p>

<pre><code class="language-js prettyprint">/**
 * A fancier event target that does cool things.
 * @implements {Iterable&lt;string&gt;}
 */
class MyFancyTarget extends EventTarget {
  /**
   * @param {string} arg1 An argument that makes this more interesting.
   * @param {!Array&lt;number&gt;} arg2 List of numbers to be processed.
   */
  constructor(arg1, arg2) {
    // ...
  }
};

/**
 * Records are also helpful.
 * @extends {Iterator&lt;TYPE&gt;}
 * @record
 * @template TYPE
 */
class Listable {
  /** @return {TYPE} The next item in line to be returned. */
  next() {}
}
</code></pre>

<h3 id="jsdoc-enum-and-typedef-comments">7.7 Enum and typedef comments</h3>

<p>All enums and typedefs must be documented with appropriate JSDoc tags
(<code>@typedef</code> or <code>@enum</code>) on the preceding line. Public enums and typedefs must
also have a description. Individual enum items may be documented with a JSDoc
comment on the preceding line.</p>

<pre><code class="language-js prettyprint">/**
 * A useful type union, which is reused often.
 * @typedef {!Bandersnatch|!BandersnatchType}
 */
let CoolUnionType;


/**
 * Types of bandersnatches.
 * @enum {string}
 */
const BandersnatchType = {
  /** This kind is really frumious. */
  FRUMIOUS: 'frumious',
  /** The less-frumious kind. */
  MANXOME: 'manxome',
};
</code></pre>

<p>Typedefs are useful for defining short record types, or aliases for unions,
complex functions, or generic types.
Typedefs should be avoided for record types with many fields, since they do not
allow documenting individual fields, nor using templates or recursive
references.
For large record types, prefer <code>@record</code>.</p>

<h3 id="jsdoc-method-and-function-comments">7.8 Method and function comments</h3>

<p>In methods and named functions, parameter and return types must be documented,
except in the case of same-signature <code>@override</code>s, where all types are omitted.
The <code>this</code> type should be documented when necessary. Return type may be omitted
if the function has no non-empty <code>return</code> statements.</p>

<p>Method, parameter, and return descriptions (but not types) may be omitted if
they are obvious from the rest of the method&#8217;s JSDoc or from its signature.</p>

<p>Method descriptions begin with a verb phrase that describes what the method
does. This phrase is not an imperative sentence, but instead is written in the
third person, as if there is an implied <q>This method ...</q> before it.</p>

<p>If a method overrides a superclass method, it must include an <code>@override</code>
annotation. Overridden methods inherit all JSDoc annotations from the super
class method (including visibility annotations) and they should be omitted in
the overridden method. However, if any type is refined in type annotations, all
<code>@param</code> and <code>@return</code> annotations must be specified explicitly.</p>

<pre><code class="language-js prettyprint">/** A class that does something. */
class SomeClass extends SomeBaseClass {
  /**
   * Operates on an instance of MyClass and returns something.
   * @param {!MyClass} obj An object that for some reason needs detailed
   *     explanation that spans multiple lines.
   * @param {!OtherClass} obviousOtherClass
   * @return {boolean} Whether something occurred.
   */
  someMethod(obj, obviousOtherClass) { ... }

  /** @override */
  overriddenMethod(param) { ... }
}

/**
 * Demonstrates how top-level functions follow the same rules.  This one
 * makes an array.
 * @param {TYPE} arg
 * @return {!Array&lt;TYPE&gt;}
 * @template TYPE
 */
function makeArray(arg) { ... }
</code></pre>

<p>If you only need to document the param and return types of a function, you may
optionally use inline JSDocs in the function's signature. These inline JSDocs
specify the return and param types without tags.</p>

<pre><code class="language-js prettyprint">function /** string */ foo(/** number */ arg) {...}
</code></pre>

<p>If you need descriptions or tags, use a single JSDoc comment above the method.
For example, methods which return values need a <code>@return</code> tag.</p>

<pre><code class="language-js prettyprint">class MyClass {
  /**
   * @param {number} arg
   * @return {string}
   */
  bar(arg) {...}
}
</code></pre>

<pre><code class="language-js prettyprint badcode">// Illegal inline JSDocs.

class MyClass {
  /** @return {string} */ foo() {...}
}

/** Function description. */ bar() {...}
</code></pre>



<p>In anonymous functions annotations are generally optional. If the automatic type
inference is insufficient or explicit annotation improves readability, then
annotate param and return types like this:</p>

<pre><code class="language-js prettyprint">promise.then(
    /** @return {string} */
    (/** !Array&lt;string&gt; */ items) =&gt; {
      doSomethingWith(items);
      return items[0];
    });
</code></pre>

<p>For function type expressions, see <a href="#jsdoc-function-types">??</a>.</p>

<h3 id="jsdoc-property-comments">7.9 Property comments</h3>

<p>Property types must be documented. The description may be omitted for private
properties, if name and type provide enough documentation for understanding the
code.</p>

<p>Publicly exported constants are commented the same way as properties.</p>

<pre><code class="language-js prettyprint">/** My class. */
class MyClass {
  /** @param {string=} someString */
  constructor(someString = 'default string') {
    /** @private @const {string} */
    this.someString_ = someString;

    /** @private @const {!OtherType} */
    this.someOtherThing_ = functionThatReturnsAThing();

    /**
     * Maximum number of things per pane.
     * @type {number}
     */
    this.someProperty = 4;
  }
}

/**
 * The number of times we'll try before giving up.
 * @const {number}
 */
MyClass.RETRY_COUNT = 33;
</code></pre>

<h3 id="jsdoc-type-annotations">7.10 Type annotations</h3>

<p>Type annotations are found on <code>@param</code>, <code>@return</code>, <code>@this</code>, and <code>@type</code> tags,
and optionally on <code>@const</code>, <code>@export</code>, and any visibility tags.  Type
annotations attached to JSDoc tags must always be enclosed in braces.</p>

<h4 id="jsdoc-nullability">7.10.1 Nullability</h4>

<p>The type system defines modifiers <code>!</code> and <code>?</code> for non-null and nullable,
respectively. These modifiers must precede the type.</p>

<p>Nullability modifiers have different requirements for different types, which
fall into two broad categories:</p>

<ol>
<li>Type annotations for primitives (<code>string</code>, <code>number</code>, <code>boolean</code>, <code>symbol</code>,
<code>undefined</code>, <code>null</code>) and literals (<code>{function(...): ...}</code> and <code>{{foo:
string...}}</code>) are always non-nullable by default. Use the <code>?</code> modifier to
make it nullable, but omit the redundant <code>!</code>.</li>
<li>Reference types (generally, anything in <code>UpperCamelCase</code>, including
<code>some.namespace.ReferenceType</code>) refer to a class, enum, record, or typedef
defined elsewhere. Since these types may or may not be nullable, it is
impossible to tell from the name alone whether it is nullable or not. Always
use explicit <code>?</code> and <code>!</code> modifiers for these types to prevent ambiguity at
use sites.</li>
</ol>

<p>Bad:</p>

<pre><code class="language-js prettyprint badcode">const /** MyObject */ myObject = null; // Non-primitive types must be annotated.
const /** !number */ someNum = 5; // Primitives are non-nullable by default.
const /** number? */ someNullableNum = null; // ? should precede the type.
const /** !{foo: string, bar: number} */ record = ...; // Already non-nullable.
const /** MyTypeDef */ def = ...; // Not sure if MyTypeDef is nullable.

// Not sure if object (nullable), enum (non-nullable, unless otherwise
// specified), or typedef (depends on definition).
const /** SomeCamelCaseName */ n = ...;
</code></pre>

<p>Good:</p>

<pre><code class="language-js prettyprint">const /** ?MyObject */ myObject = null;
const /** number */ someNum = 5;
const /** ?number */ someNullableNum = null;
const /** {foo: string, bar: number} */ record = ...;
const /** !MyTypeDef */ def = ...;
const /** ?SomeCamelCaseName */ n = ...;
</code></pre>

<h4 id="jsdoc-type-casts">7.10.2 Type Casts</h4>

<p>In cases where the compiler doesn't accurately infer the type of an expression,
and the assertion functions in
<a href="https://google.github.io/closure-library/api/goog.asserts.html">goog.asserts</a>
cannot remedy it , it is possible to
tighten the type by adding a type annotation comment and enclosing the
expression in parentheses. Note that the parentheses are required.</p>

<pre><code class="language-js prettyprint">/** @type {number} */ (x)
</code></pre>

<h4 id="jsdoc-template-parameter-types">7.10.3 Template Parameter Types</h4>

<p>Always specify template parameters. This way compiler can do a better job and it
makes it easier for readers to understand what code does.</p>

<p>Bad:</p>

<pre><code class="language-js prettyprint badcode">const /** !Object */ users = {};
const /** !Array */ books = [];
const /** !Promise */ response = ...;
</code></pre>

<p>Good:</p>

<pre><code class="language-js prettyprint">const /** !Object&lt;string, !User&gt; */ users = {};
const /** !Array&lt;string&gt; */ books = [];
const /** !Promise&lt;!Response&gt; */ response = ...;

const /** !Promise&lt;undefined&gt; */ thisPromiseReturnsNothingButParameterIsStillUseful = ...;
const /** !Object&lt;string, *&gt; */ mapOfEverything = {};
</code></pre>

<p>Cases when template parameters should not be used:</p>

<ul>
<li><code>Object</code> is used for type hierarchy and not as map-like structure.</li>
</ul>

<h4 id="jsdoc-function-types">7.10.4 Function type expressions</h4>

<p><strong>Terminology Note</strong>: <em>function type expression</em> refers to a type annotation for
function types with the keyword <code>function</code> in the annotation (see examples
below).</p>

<p>Where the function definition is given, do not use a function type expression.
Specify parameter and return types with <code>@param</code> and <code>@return</code>, or with inline
annotations (see <a href="#jsdoc-method-and-function-comments">??</a>). This includes
anonymous functions and functions defined and assigned to a const (where the
function jsdoc appears above the whole assignment expression).</p>

<p>Function type expressions are needed, for example, inside <code>@typedef</code>, <code>@param</code>
or <code>@return</code>. Use it also for variables or properties of function type, if they
are not immediately initialized with the function definition.</p>

<pre><code class="language-js prettyprint">  /** @private {function(string): string} */
  this.idGenerator_ = googFunctions.identity;
</code></pre>

<p>When using a function type expression, always specify the return type
explicitly. Otherwise the default return type is <q>unknown</q> (<code>?</code>), which leads to
strange and unexpected behavior, and is rarely what is actually desired.</p>

<p>Bad - type error, but no warning given:</p>

<pre><code class="language-js prettyprint badcode">/** @param {function()} generateNumber */
function foo(generateNumber) {
  const /** number */ x = generateNumber();  // No compile-time type error here.
}

foo(() =&gt; 'clearly not a number');
</code></pre>

<p>Good:</p>

<pre><code class="language-js prettyprint">/**
 * @param {function(): *} inputFunction1 Can return any type.
 * @param {function(): undefined} inputFunction2 Definitely doesn't return
 *      anything.
 * NOTE: the return type of `foo` itself is safely implied to be {undefined}.
 */
function foo(inputFunction1, inputFunction2) {...}
</code></pre>

<h4 id="jsdoc-whitespace">7.10.5 Whitespace</h4>

<p>Within a type annotation, a single space or line break is required after each
comma or colon. Additional line breaks may be inserted to improve readability or
avoid exceeding the column limit. These breaks should be chosen and indented
following the applicable guidelines (e.g. <a href="#formatting-line-wrapping">??</a> and
<a href="#formatting-block-indentation">??</a>). No other whitespace is allowed in type
annotations.</p>

<p>Good:</p>

<pre><code class="language-js prettyprint">/** @type {function(string): number} */

/** @type {{foo: number, bar: number}} */

/** @type {number|string} */

/** @type {!Object&lt;string, string&gt;} */

/** @type {function(this: Object&lt;string, string&gt;, number): string} */

/**
 * @type {function(
 *     !SuperDuperReallyReallyLongTypedefThatForcesTheLineBreak,
 *     !OtherVeryLongTypedef): string}
 */

/**
 * @type {!SuperDuperReallyReallyLongTypedefThatForcesTheLineBreak|
 *     !OtherVeryLongTypedef}
 */
</code></pre>

<p>Bad:</p>

<pre><code class="language-js prettyprint badcode">// Only put a space after the colon
/** @type {function(string) : number} */

// Put spaces after colons and commas
/** @type {{foo:number,bar:number}} */

// No space in union types
/** @type {number | string} */
</code></pre>

<h3 id="jsdoc-visibility-annotations">7.11 Visibility annotations</h3>

<p>Visibility annotations (<code>@private</code>, <code>@package</code>, <code>@protected</code>) may be specified
in a <code>@fileoverview</code> block, or on any exported symbol or property.  Do not
specify visibility for local variables, whether within a function or at the top
level of a module.  All <code>@private</code> names must end with an underscore.</p>

<h2 id="policies">8 Policies</h2>

<h3 id="policies-be-consistent">8.1 Issues unspecified by Google Style: Be Consistent!</h3>

<p>For any style question that isn't settled definitively by this specification,
prefer to do what the other code in the same file is already doing. If that
doesn't resolve the question, consider emulating the other files in the same
package.</p>

<h3 id="policies-compiler-warnings">8.2 Compiler warnings</h3>

<h4 id="policies-use-a-standard-warning-set">8.2.1 Use a standard warning set</h4>

<p>
As far as possible projects should use <code>--warning_level=VERBOSE</code>.
</p>

<h4 id="policies-how-to-handle-a-warning">8.2.2 How to handle a warning</h4>

<p>Before doing anything, make sure you understand exactly what the warning is
telling you. If you're not positive why a warning is appearing, ask for help
.</p>

<p>Once you understand the warning, attempt the following solutions in order:</p>

<ol>
<li><strong>First, fix it or work around it.</strong> Make a strong attempt to actually
address the warning, or find another way to accomplish the task that avoids
the situation entirely.</li>
<li><strong>Otherwise, determine if it's a false alarm.</strong> If you are convinced that
the warning is invalid and that the code is actually safe and correct, add a
comment to convince the reader of this fact and apply the <code>@suppress</code>
annotation.</li>
<li><strong>Otherwise, leave a TODO comment.</strong> This is a <strong>last resort</strong>.  If you do
this, <strong>do not suppress the warning.</strong> The warning should be visible until
it can be taken care of properly.</li>
</ol>

<h4 id="policies-suppress-a-warning-at-the-narrowest-reasonable-scope">8.2.3 Suppress a warning at the narrowest reasonable scope</h4>

<p>Warnings are suppressed at the narrowest reasonable scope, usually that of a single local variable or very small method. Often a variable or method is extracted for that reason alone.</p>

<p>Example</p>

<pre><code class="language-js prettyprint">/** @suppress {uselessCode} Unrecognized 'use asm' declaration */
function fn() {
  'use asm';
  return 0;
}
</code></pre>

<p>Even a large number of suppressions in a class is still better than blinding the
entire class to this type of warning.</p>

<h3 id="policies-deprecation">8.3 Deprecation</h3>

<p>Mark deprecated methods, classes or interfaces with <code>@deprecated</code> annotations. A
deprecation comment must include simple, clear directions for people to fix
their call sites.</p>

<h3 id="policies-code-not-in-google-style">8.4 Code not in Google Style</h3>

<p>You will occasionally encounter files in your codebase that are not in proper
Google Style. These may have come from an acquisition, or may have been written
before Google Style took a position on some issue, or may be in non-Google Style
for any other reason.</p>

<h4 id="policies-reformatting-existing-code">8.4.1 Reformatting existing code</h4>

<p>When updating the style of existing code, follow these guidelines.</p>

<ol>
<li>It is not required to change all existing code to meet current style
guidelines.  Reformatting existing code is a trade-off between code churn
and consistency. Style rules evolve over time and these kinds of tweaks to
maintain compliance would create unnecessary churn.  However, if significant
changes are being made to a file it is expected that the file will be in
Google Style.</li>
<li>Be careful not to allow opportunistic style fixes to muddle the focus of a
CL. If you find yourself making a lot of style changes that aren&#8217;t critical
to the central focus of a CL, promote those changes to a separate CL.</li>
</ol>

<h4 id="policies-newly-added-code-use-google-style">8.4.2 Newly added code: use Google Style</h4>

<p>Brand new files use Google Style, regardless of the style choices of other files
in the same package.</p>

<p>When adding new code to a file that is not in Google Style, reformatting the
existing code first is recommended, subject to the advice in
<a href="#policies-reformatting-existing-code">??</a>.</p>

<p>If this reformatting is not done, then new code should be as consistent as
possible with existing code in the same file, but must not violate the style
guide.</p>

<h3 id="policies-local-style-rules">8.5 Local style rules</h3>

<p>Teams and projects may adopt additional style rules beyond those in this
document, but must accept that cleanup changes may not abide by these additional
rules, and must not block such cleanup changes due to violating any additional
rules. Beware of excessive rules which serve no purpose. The style guide does
not seek to define style in every possible scenario and neither should you.</p>

<h3 id="policies-generated-code-mostly-exempt">8.6 Generated code: mostly exempt</h3>

<p>Source code generated by the build process is not required to be in Google
Style. However, any generated identifiers that will be referenced from
hand-written source code must follow the naming requirements. As a special
exception, such identifiers are allowed to contain underscores, which may help
to avoid conflicts with hand-written identifiers.</p>

<h2 id="appendices">9 Appendices</h2>

<h3 id="appendices-jsdoc-tag-reference">9.1 JSDoc tag reference</h3>

<p>JSDoc serves multiple purposes in JavaScript.  In addition to being used to
generate documentation it is also used to control tooling.  The best known are
the Closure Compiler type annotations.</p>

<h4 id="appendices-type-annotations">9.1.1 Type annotations and other Closure Compiler annotations</h4>

<p>Documentation for JSDoc used by the Closure Compiler is described in
<a href="https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler">Annotating JavaScript for the Closure Compiler</a> and <a href="https://github.com/google/closure-compiler/wiki/Types-in-the-Closure-Type-System">Types in the Closure Type
System</a>.</p>

<h4 id="appendices-documentation-annotations">9.1.2 Documentation annotations</h4>

<p>In addition to the JSDoc described in <a href="https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler">Annotating JavaScript for the Closure
Compiler</a> the following tags are common and well supported by various
documentation generation tools (such as <a href="https://github.com/jleyba/js-dossier">JsDossier</a>) for purely documentation
purposes.</p>

<p>You may also see other types of JSDoc annotations in third-party code. These
annotations appear in the <a href="http://code.google.com/p/jsdoc-toolkit/wiki/TagReference">JSDoc Toolkit Tag Reference</a> but are not considered
part of valid Google style.</p>

<section class="zippy">

<h5>9.1.2.1 <code>@author</code> or <code>@owner</code> - <em>Not recommended.</em></h5>

<p><strong>Not recommended.</strong></p>

<p>Syntax: <code>@author username@google.com (First Last)</code></p>

<pre><code class="language-js prettyprint">/**
 * @fileoverview Utilities for handling textareas.
 * @author kuth@google.com (Uthur Pendragon)
 */
</code></pre>

<p>Documents the author of a file or the owner of a test, generally only used in
the <code>@fileoverview</code> comment. The <code>@owner</code> tag is used by the unit test dashboard
to determine who owns the test results.</p>

</section>

<section class="zippy">

<h5>9.1.2.2 <code>@bug</code></h5>

<p>Syntax: <code>@bug bugnumber</code></p>

<pre><code class="language-js prettyprint">/** @bug 1234567 */
function testSomething() {
  // &#8230;
}

/**
 * @bug 1234568
 * @bug 1234569
 */
function testTwoBugs() {
  // &#8230;
}
</code></pre>

<p>Indicates what bugs the given test function regression tests.</p>

<p>Multiple bugs should each have their own <code>@bug</code> line, to make searching for
regression tests as easy as possible.</p>

</section>

<section class="zippy">

<h5>9.1.2.3 <code>@code</code> - <em>Deprecated. Do not use.</em></h5>

<p><strong>Deprecated. Do not use. Use Markdown backticks instead.</strong></p>

<p>Syntax: <code>{@code ...}</code></p>

<p>Historically, <code>`BatchItem`</code> was written as
<code class="badcode">{@code BatchItem}</code>.</p>

<pre><code class="language-js prettyprint">/** Processes pending `BatchItem` instances. */
function processBatchItems() {}
</code></pre>

<p>Indicates that a term in a JSDoc description is code so it may be correctly
formatted in generated documentation.</p>

</section>

<section class="zippy">

<h5>9.1.2.4 <code>@desc</code></h5>

<p>Syntax: <code>@desc Message description</code></p>

<pre><code class="language-js prettyprint">/** @desc Notifying a user that their account has been created. */
exports.MSG_ACCOUNT_CREATED = goog.getMsg(
    'Your account has been successfully created.');
</code></pre>

</section>

<section class="zippy">

<h5>9.1.2.5 <code>@link</code></h5>

<p>Syntax: <code>{@link ...}</code></p>

<p>This tag is used to generate cross-reference links within generated
documentation.</p>

<pre><code class="language-js prettyprint">/** Processes pending {@link BatchItem} instances. */
function processBatchItems() {}
</code></pre>

<p><strong>Historical note:</strong> @link tags have also been used to create external links in
generated documentation. For external links, always use Markdown's link syntax
instead:</p>

<pre><code class="language-js prettyprint">/**
 * This class implements a useful subset of the
 * [native Event interface](https://dom.spec.whatwg.org/#event).
 */
class ApplicationEvent {}
</code></pre>

</section>

<section class="zippy">

<h5>9.1.2.6 <code>@see</code></h5>

<p>Syntax: <code>@see Link</code></p>

<pre><code class="language-js prettyprint">/**
 * Adds a single item, recklessly.
 * @see #addSafely
 * @see goog.Collect
 * @see goog.RecklessAdder#add
 */
</code></pre>

<p>Reference a lookup to another class function or method.</p>

</section>

<section class="zippy">

<h5>9.1.2.7 <code>@supported</code></h5>

<p>Syntax: <code>@supported Description</code></p>

<pre><code class="language-js prettyprint">/**
 * @fileoverview Event Manager
 * Provides an abstracted interface to the browsers' event systems.
 * @supported IE10+, Chrome, Safari
 */
</code></pre>

<p>Used in a fileoverview to indicate what browsers are supported by the file.</p>

</section>

<h4 id="appendices-framework-specific-annotations">9.1.3 Framework specific annotations</h4>

<p>The following annotations are specific to a particular framework.</p>

<section class="zippy">

<h5>9.1.3.1 <code>@ngInject</code> for Angular 1</h5>

</section>

<section class="zippy">

<h5>9.1.3.2 <code>@polymerBehavior</code> for Polymer</h5>



<p><a href="https://github.com/google/closure-compiler/wiki/Polymer-Pass">https://github.com/google/closure-compiler/wiki/Polymer-Pass</a>
</p>

</section>

<section class="zippy">

</section>

<h4 id="appendices-notes-about-standard-closure-compiler-annotations">9.1.4 Notes about standard Closure Compiler annotations</h4>

<p>The following tags used to be standard but are now deprecated.</p>

<section class="zippy">

<h5>9.1.4.1 <code>@expose</code> - <em>Deprecated. Do not use.</em></h5>

<p><strong>Deprecated. Do not use. Use <code>@export</code> and/or <code>@nocollapse</code> instead.</strong></p>

</section>

<section class="zippy">

<h5>9.1.4.2 <code>@inheritDoc</code> - <em>Deprecated. Do not use.</em></h5>

<p><strong>Deprecated. Do not use. Use <code>@override</code> instead.</strong></p>

</section>

<section class="zippy">

</section>

<section class="zippy">

</section>

<section class="zippy">

</section>

<section class="zippy">

</section>

<section class="zippy">

</section>

<section class="zippy">

</section>

<h3 id="appendices-commonly-misunderstood-style-rules">9.2 Commonly misunderstood style rules</h3>

<p>Here is a collection of lesser-known or commonly misunderstood facts about
Google Style for JavaScript. (The following are true statements; this is not a
list of <q>myths.</q>)</p>

<ul>
<li>Neither a copyright statement nor <code>@author</code> credit is required in a source
file. (Neither is explicitly recommended, either.)</li>
<li>There is no <q>hard and fast</q> rule governing how to order the members of a
class (<a href="#features-classes">??</a>).</li>
<li>Empty blocks can usually be represented concisely as <code>{}</code>, as detailed in
(<a href="#formatting-empty-blocks">??</a>).</li>
<li>The prime directive of line-wrapping is: prefer to break at a higher
syntactic level (<a href="#formatting-where-to-break">??</a>).</li>
<li>Non-ASCII characters are allowed in string literals, comments and JSDoc,
and in fact are recommended when they make the code easier to read than the
equivalent Unicode escape would (<a href="#non-ascii-characters">??</a>).</li>
</ul>

<h3 id="appendices-style-related-tools">9.3 Style-related tools</h3>

<p>The following tools exist to support various aspects of Google Style.</p>

<h4 id="appendices-tools-closure-compiler">9.3.1 Closure Compiler</h4>

<p>This program performs type checking and other checks,
optimizations and other transformations (such as ECMAScript 6 to ECMAScript 5
code lowering).</p>

<h4 id="appendices-clang-format">9.3.2 <code>clang-format</code></h4>

<p>This program  reformats
JavaScript source code into Google Style, and also follows a number of
non-required but frequently readability-enhancing formatting practices.
The output produced by <code>clang-format</code> is compliant with the style guide.
</p>

<p><code>clang-format</code> is not required. Authors are allowed to change its output, and
reviewers are allowed to ask for such changes; disputes are worked out in the
usual way. However, subtrees may choose to opt in to such enforcement locally.</p>

<h4 id="appendices-closure-compiler-linter">9.3.3 Closure compiler linter</h4>

<p>This program  checks for a
variety of missteps and anti-patterns.
</p>

<h4 id="appendices-conformance-framework">9.3.4 Conformance framework</h4>

<p>The JS Conformance Framework is a tool that is part of the Closure Compiler that
provides developers a simple means to specify a set of additional checks to be
run against their code base above the standard checks.  Conformance checks can,
for example, forbid access to a certain property, or calls to a certain
function, or missing type information (unknowns).</p>

<p>These rules are commonly used to enforce critical restrictions (such as defining
globals, which could break the codebase) and security patterns (such as using
<code>eval</code> or assigning to <code>innerHTML</code>), or more loosely to improve code quality.</p>

<p>For additional information see the official documentation for the
<a href="https://github.com/google/closure-compiler/wiki/JS-Conformance-Framework">JS Conformance Framework</a>.</p>

<h3 id="appendices-legacy-exceptions">9.4 Exceptions for legacy platforms</h3>

<h4 id="appendices-legacy-exceptions-overview">9.4.1 Overview</h4>

<p>This section describes exceptions and additional rules to be followed when
modern ECMAScript 6 syntax is not available to the code authors. Exceptions to
the recommended style are required when ECMAScript 6 syntax is not possible and
are outlined here:</p>

<ul>
<li>Use of <code>var</code> declarations is allowed</li>
<li>Use of <code>arguments</code> is allowed</li>
<li>Optional parameters without default values are allowed</li>
</ul>

<h4 id="appendices-legacy-exceptions-var">9.4.2 Use <code>var</code></h4>

<h5 id="appendices-legacy-exceptions-var-scope">9.4.2.1 <code>var</code> declarations are NOT block-scoped</h5>

<p><code>var</code> declarations are scoped to the beginning of the nearest enclosing
function, script or module, which can cause unexpected behavior, especially with
function closures that reference <code>var</code> declarations inside of loops. The
following code gives an example:</p>

<pre><code class="language-js prettyprint badcode">for (var i = 0; i &lt; 3; ++i) {
  var iteration = i;
  setTimeout(function() { console.log(iteration); }, i*1000);
}

// logs 2, 2, 2 -- NOT 0, 1, 2
// because `iteration` is function-scoped, not local to the loop.

</code></pre>

<h5 id="appendices-legacy-exceptions-var-declare">9.4.2.2 Declare variables as close as possible to first use</h5>

<p>Even though <code>var</code> declarations are scoped to the beginning of the enclosing
function, <code>var</code> declarations should be as close as possible to their first use,
for readability purposes. However, do not put a <code>var</code> declaration inside a block
if that variable is referenced outside the block. For example:</p>

<pre><code class="language-js prettyprint">function sillyFunction() {
  var count = 0;
  for (var x in y) {
    // "count" could be declared here, but don't do that.
    count++;
  }
  console.log(count + ' items in y');
}
</code></pre>

<h5 id="appendices-legacy-exceptions-var-const">9.4.2.3 Use @const for constants variables</h5>

<p>For global declarations where the <code>const</code> keyword would be used, if it were
available, annotate the <code>var</code> declaration with @const instead (this is optional
for local variables).</p>

<h4 id="appendices-legacy-exceptions-function">9.4.3 Do not use block scoped functions declarations</h4>

<p>Do <strong>not</strong> do this:</p>

<pre><code class="language-js prettyprint badcode">if (x) {
  function foo() {}
}
</code></pre>

<p>While most JavaScript VMs implemented before ECMAScript 6 support function
declarations within blocks it was not standardized. Implementations were
inconsistent with each other and with the now-standard ECMAScript 6 behavior for
block scoped function declaration. ECMAScript 5 and prior only allow for
function declarations in the root statement list of a script or function and
explicitly ban them in block scopes in strict mode.</p>

<p>To get consistent behavior, instead use a <code>var</code> initialized with a function
expression to define a function within a block:</p>

<pre><code class="language-js prettyprint">if (x) {
  var foo = function() {};
}
</code></pre>

<h4 id="appendices-legacy-exceptions-goog-provide">9.4.4 Dependency management with <code>goog.provide</code>/<code>goog.require</code></h4>

<h5 id="appendices-legacy-exceptions-goog-provide-summary">9.4.4.1 Summary</h5>

<p><strong>WARNING: <code>goog.provide</code> dependency management is deprecated.</strong> All new files,
even in projects using <code>goog.provide</code> for older files, should use
<a href="#source-file-structure"><code>goog.module</code></a>. The following rules are for
pre-existing <code>goog.provide</code> files only.</p>

<ul>
<li>Place all <code>goog.provide</code>s first, <code>goog.require</code>s second. Separate provides
from requires with an empty line.</li>
<li>Sort the entries alphabetically (uppercase first).</li>
<li>Don't wrap <code>goog.provide</code> and <code>goog.require</code> statements. Exceed 80 columns
if necessary.</li>
<li>Only provide top-level symbols.</li>
</ul>

<p><code>goog.provide</code> statements should be grouped together and placed first. All
<code>goog.require</code> statements should follow. The two lists should be separated with
an empty line.</p>

<p>Similar to import statements in other languages, <code>goog.provide</code> and
<code>goog.require</code> statements should be written in a single line, even if they
exceed the 80 column line length limit.</p>

<p>The lines should be sorted alphabetically, with uppercase letters coming first:</p>

<pre><code class="language-js prettyprint">goog.provide('namespace.MyClass');
goog.provide('namespace.helperFoo');

goog.require('an.extremelyLongNamespace.thatSomeoneThought.wouldBeNice.andNowItIsLonger.Than80Columns');
goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('goog.dom.classes');
goog.require('goog.dominoes');

</code></pre>

<p>All members defined on a class should be in the same file. Only top-level
classes should be provided in a file that contains multiple members defined on
the same class (e.g. enums, inner classes, etc).</p>

<p>Do this:</p>

<pre><code class="language-js prettyprint">goog.provide('namespace.MyClass');
</code></pre>

<p>Not this:</p>

<pre><code class="language-js prettyprint badcode">goog.provide('namespace.MyClass');
goog.provide('namespace.MyClass.CONSTANT');
goog.provide('namespace.MyClass.Enum');
goog.provide('namespace.MyClass.InnerClass');
goog.provide('namespace.MyClass.TypeDef');
goog.provide('namespace.MyClass.staticMethod');
</code></pre>

<p>Members on namespaces may also be provided:</p>

<pre><code class="language-js prettyprint">goog.provide('foo.bar');
goog.provide('foo.bar.CONSTANT');
goog.provide('foo.bar.method');
</code></pre>

<h5 id="appendices-legacy-exceptions-goog-scope">9.4.4.2 Aliasing with <code>goog.scope</code></h5>

<p><strong>WARNING: <code>goog.scope</code> is deprecated.</strong> New files should not use <code>goog.scope</code>
even in projects with existing <code>goog.scope</code> usage.</p>

<p><code>goog.scope</code> may be used to shorten references to namespaced symbols in
code using <code>goog.provide</code>/<code>goog.require</code> dependency management.</p>

<p>Only one <code>goog.scope</code> invocation may be added per file. Always place it in
the global scope.</p>

<p>The opening <code>goog.scope(function() {</code> invocation must be preceded by exactly one
blank line and follow any <code>goog.provide</code> statements, <code>goog.require</code> statements,
or top-level comments. The invocation must be closed on the last line in the
file. Append <code>// goog.scope</code> to the closing statement of the scope. Separate the
comment from the semicolon by two spaces.</p>

<p>Similar to C++ namespaces, do not indent under <code>goog.scope</code> declarations.
Instead, continue from the 0 column.</p>

<p>Only make aliases for names that will not be re-assigned to another object
(e.g., most constructors, enums, and namespaces). Do not do this (see below for
how to alias a constructor):</p>

<pre><code class="language-js prettyprint badcode">goog.scope(function() {
var Button = goog.ui.Button;

Button = function() { ... };
...
</code></pre>

<p>Names must be the same as the last property of the global that they are aliasing.</p>

<pre><code class="language-js prettyprint">goog.provide('my.module.SomeType');

goog.require('goog.dom');
goog.require('goog.ui.Button');

goog.scope(function() {
var Button = goog.ui.Button;
var dom = goog.dom;

// Alias new types after the constructor declaration.
my.module.SomeType = function() { ... };
var SomeType = my.module.SomeType;

// Declare methods on the prototype as usual:
SomeType.prototype.findButton = function() {
  // Button as aliased above.
  this.button = new Button(dom.getElement('my-button'));
};
...
});  // goog.scope
</code></pre>

<h5 id="appendices-legacy-exceptions-forward-declare">9.4.4.3 <code>goog.forwardDeclare</code></h5>

<p>Prefer to use <code>goog.requireType</code> instead of <code>goog.forwardDeclare</code> to break
circular dependencies between files in the same library. Unlike <code>goog.require</code>,
a <code>goog.requireType</code> statement is allowed to import a namespace before it is
defined.</p>

<p><code>goog.forwardDeclare</code> may still be used in legacy code to break circular
references spanning across library boundaries, but newer code should be
structured to avoid it.</p>

<p><code>goog.forwardDeclare</code> statements must follow the same style rules as
<code>goog.require</code> and <code>goog.requireType</code>. The entire block of
<code>goog.forwardDeclare</code>, <code>goog.require</code> and <code>goog.requireType</code> statements is
sorted alphabetically.</p>

</div>
</body>
</html>
