# Google's Haskell Style Guide

Revision 1.01

<a id="Background"></a>
## Background 

Haskell is a mature, general purpose, purely functional language. It is noted
for its strong static type system (with type inference), lazy (technically,
'non-strict') execution semantics, higher-order functions, parametric
polymorphism, type classes, and monadic effects.

Haskell's syntax is fairly concise, and most of the choices you might make about
style are generally closely tied to the semantics of the code you wish to
convey. As such, this guide tends to be somewhat less prescriptive than most, as
there are just fewer arbitrary choices to make when coding Haskell.

Open-source projects developed by Google should conform to the requirements in this guide.

<a id="Structure"></a>
## Structure 

<a id="Haddock"></a>
### Haddock 

The module and all exported top-level elements should have Haddock.

Haddock should directly precede the element it documents. It need not repeat
argument names or types, as they are readily apparent from the declaration.

Write proper sentences; start with a capital letter and use proper punctuation.

**Exception:** Extremely simple type synonyms or other very obvious declarations
need not have any Haddock.

```haskell
type Forest p a = [Tree p a]    -- simple enough to not need Haddock

-- | Returns values in the Forest from entries that cover the given prefix.
-- The value list is ordered from most general to most specific entries.
forestLookup :: (Prefix p) => p -> Forest p a -> [a]
```

Use in-line links economically in Haddock. Links are encouraged, but it is not
necessary to add links for all API names. Add a link if:

*   The user might actually want to click on it for more information (in your
    judgment), and
*   Only for the first occurrence of each API name in the comment (don't bother
    repeating a link).

<a id="Exports"></a>
### Exports 

*   All modules should have an explicit export list.
*   Format like all lists, starting on new line after `module`.
*   Can have multiple exports on a single line if logically related.
*   Order should tell a story - it is the order shown in Haddock.

In addition to the rules above, don't re-export modules as a "convenience".
However, it is acceptable to re-export modules in these two circumstances:

*   It is okay to re-export things from `Internal` modules that otherwise
    wouldn't be exported.
*   It is okay to have a "package" module that does nothing but export the
    common modules from the same package.

**Exception:** It is acceptable to not have an explicit exports list when the
bulk of the exported definitions are generated with Template Haskell, since
explicitly naming them in the export list would be counter-productive.

<a id="Imports"></a>
### Imports 

*   Imports may be split up into groups separated by a single newline.
*   Recommended: Split imports into two groups: external and
    internal modules.
*   Within each group, imports must be alphabetized by full module name.
*   Imports can either be qualified or for specific elements. It is okay to have
    both.
*   Imports from the same package can be imported wholesale, but this is
    discouraged.

In general, use the last component of the module name as the qualified name.

It is acceptable to use the same prefix for related modules.

**Exception:** Some modules are designed to be reasonably imported without an
import list, such as `Data.Bits`, and this is acceptable.

Very short names for qualified imports are acceptable for the following modules,
as they are in very wide use in Haskell source:

```haskell
import qualified Data.ByteString as BS
import qualified Data.ByteString.Lazy as BL
import qualified Data.HashMap.Strict as HM    -- or Data.HashMap.Lazy as needed
import qualified Data.HashSet as HS
import qualified Data.Map as M
import qualified Data.Set as S
import qualified Data.Text as T
import qualified Data.Text.Lazy as TL
```

Putting these all together:

```haskell
import Data.Bits                             -- okay for some modules
import Data.Maybe (mapMaybe, maybeToList)    -- better to list what you use...
import qualified Data.Ratio as Ratio         -- ...or import qualified
import qualified Data.Text as T              -- short name allowed for this
import qualified Data.Text.Encoding as T     -- reuse name for related modules
import qualified Data.Text.IO as T
import qualified Text.Parsec as Parsec
import qualified Text.Parsec.Expr as Parsec

import AnInternalProject.Data.WhoopTree      -- okay to import all, but discouraged
```

<a id="Pragmas"></a>
### Pragmas 

GHC options and `LANGUAGE` pragmas go at the very top of the file.

*   One `{-# OPTIONS_GHC ... #-}` directive at the top, if needed
*   One `{-# LANGUAGE ... #-}` directive for each language extension after that,
    in sorted order, if needed

The `OPTIONS_GHC` directive should only be used for specific options that relate
to the source file, such as `-fno-warn-orphans` for test code. General
compilation options, like `-O2`, belong in
the `.cabal` file.

Features enabled by the `LANGUAGE` pragma should always be listed in each source
file that needs them, and never turned on globally via flags in the
the `.cabal` file. This is so future
developers know what language extensions are in effect when reading the code.

`INLINE`, `INLINEABLE`, and similar pragmas should only be used when you've
tested that they actually improve speed in cases that you care about. When used,
they should follow directly the declaration they apply to.

The following GHC language extensions are non-controversial and can be used as
needed. That said, consider if use of the extension improves the code in
proportion to the extra burden it gives to future readers:

*   `DeriveDataTypeable`, `DeriveGeneric`, `DeriveFunctor`, `DeriveFoldable`,
    and `DeriveTraversable`
*   `BangPatterns`
*   `CPP`
*   `FlexibleContexts`
*   `ForeignFunctionInterface`
*   `GADTs`
*   `GeneralizedNewtypeDeriving`
*   `MagicHash`
*   `MultiParamTypeClasses`
*   `NamedFieldPuns`
*   `OverloadedStrings`
*   `PatternGuards`
*   `Rank2Types`, `RankNTypes`
*   `RecordWildCards` and `DisambiguateRecordFields`
*   `ScopedTypeVariables`
*   `TemplateHaskell`
*   `TupleSections`
*   `TypeFamilies`
*   `ViewPatterns`

Other GHC extensions should be avoided, as they may or may not be stable,
increase the burden on readers to know them, and may force clients to use them.

<a id="Warnings"></a>
### Warnings 

Code should compile cleanly with no warnings from GHC.

GHC emits very useful warnings when given the `-Wall` argument. Code should
compile with both `-Wall` and `-Werror`, ensuring warnings are not ignored.

(You get the same effect in GHCi by adding `:set -Wall ...` to your
`~/.ghc/ghci.conf` file.)

In the rare cases when it's necessary to declare an instance in a module which
contains neither the corresponding class declaration nor the corresponding type
declaration, warnings about orphans can be suppressed by adding `{-# OPTIONS_GHC
-fno-warn-orphans #-}` line at the top of the relevant file.

<a id="Style"></a>
## Style 

<a id="Layout"></a>
### Layout 

Use layout, rather than braces and semicolons.

Except for one-liners, use layout rather than braces and semicolons. It makes
for clearer code.

<a id="Type_Declarations"></a>
### Type Declarations 

All top level functions should have type declarations.

Even though Haskell supports type inference, all top-level functions should
include type declarations. If nothing else, type declarations provide good
documentation.

Where reasonable, use the most polymorphic possible type.

<a id="Comments"></a>
### Comments 

Use `--` for all comments except pragmas, or where the comment must be in the
middle of a line.

If there is text on the line before the dashes, there should be at least two
spaces immediately before the dashes. If there is text after the dashes, there
should be a space immediately after the dashes.

As per the section on Haddock, all top level elements should have a preceding
comment for the purpose of Haddock. The aim is to explain the purpose of the
function, not the implementation.

The implementation should be clear from the code, but comments in the code
should be used to explain any non-obvious reasoning for why something was done a
particular way, or is particularly tricky.

<a id="if_then_else"></a>
### if…then…else 

Consider using guards and pattern matches over `if`…`then`…`else`.

Generally, pattern matches and guards are clearer at the outer level of a
function than nested `if` and `case` constructs. However, elsewhere `if` might
be more clear. Use your judgement.

```haskell
nth :: Int -> [a] -> Maybe a
nth i xs = if null xs || i < 0
    then Nothing
    else if i == 0
        then Just (head xs)
        else nth (i-1) (tail xs)
```

```haskell
nth :: Int -> [a] -> Maybe a
nth i _     | i < 0 = Nothing
nth _ []            = Nothing
nth 0 (x:xs)        = Just x
nth i (_:xs)        = nth (i-1) xs
```

<a id="Idioms"></a>
## Idioms 

Functional programming has given rise to a large number of new programming
idioms. The following idioms are encouraged:

<a id="Partial_Functions"></a>
### Partial Functions 

[Partial functions](https://www.haskell.org/haskellwiki/Partial_functions) are
those that are not defined for all possible arguments.

Strenuously avoid partial functions from the `Prelude` and base libraries.
Commonly used examples are: `head`, `(!!)`, `minimum`, `fromJust`, and `read`.

**Exception:** In cases where pattern matching, guards, or other logic
immediately nearby makes it certain that these functions are applied safely, it
is acceptable to call them.

```haskell
defaultChoice :: [String] -> String
defaultChoice [] = "beige"
defaultChoice opts = minimum opts
  -- okay because pattern match ensures non-empty

digitsReversed :: Integer -> Integer
digitsReversed i = (* signum i) . read . reverse . show $ abs i
  -- okay because show of a non-negative value only produces digits
```

Do not write partial functions.

**Exception:** If a function internal to a module should never reach some case
due to invariants maintained by the module, then it is acceptable to call
`error` for those cases, and preferred to returning inaccurate results, or
heuristically restoring the invariant:

```haskell
data PTrie = PT { ptSubs :: [(String, PTrie)] }
  -- Invariant this module maintains: There is no non-empty prefix that is
  -- shared by any two sub-PTries of a given node.

insert :: String -> PTrie -> PTrie
insert s pt = case filter (not . null . greatestCommonPrefix s) $ ptSubs pt of
  [] -> ...   -- no node matches
  [a] -> ...  -- one node matches, need to recurse or split
  _ -> error "PTrie.insert PTrie has subs with a common prefix"
```

<a id="Point_Free"></a>
### Point-Free 

[Point-free style](http://www.haskell.org/haskellwiki/Haskell/Pointfree) is fine
and often leads to concise code that focuses on what the code does, rather than
on what it does it to.

However, avoid over-using it. For example, do not use contorted point free just
to handle multiple arguments:

```haskell
f = (g .) . h       -- makes most of us puzzle it out
```

```haskell
f x = g . h x       -- most readers will get this immediately
f x y = g $ h x y   -- depending on the functions, this may or may not be better
```

<a id="Combinators"></a>
### Combinators 

Libraries designed to be combinators produce very powerful tools for other
developers. Examples to learn from are Parsec and PrettyPrint.

<a id="QuickCheck"></a>
### QuickCheck 

Tests should be written with QuickCheck whenever possible. This form of testing
is surprisingly effective. Use HUnit for special cases that need explicit
testing. Tie them all together with Test Framework.

It will often be required to write instances of `Arbitrary`. These should go in
the corresponding `_Test` module. (With the corresponding option to turn off the
warning about orphan instances.) Such instances should be sure to weight cases
equally, or if they don't, explain why.

<a id="Naming"></a>
## Naming 

<a id="General_Rules"></a>
### General Rules 

Use mixed-case identifiers, without underscores.

Haskell's naming rules are fairly strict, and are not reproduced here, as the
language enforces adherence.

Underscores are to be avoided, as mixed-case is the predominant style in the
Haskell community. The following uses of underscores are acceptable:

*   An un-used argument or pattern element: `_`
*   An un-used argument or pattern match element that needs a more descriptive
    name: `_sizeHint`.
*   To identify a QuickCheck property, a test, a test group, or test module:
    `prop_UnionIsAssociative`, `test_SetOperations`, or `Data.MultiWaySet_Test`
*   When naming something where the logical name is also a reserved word in
    Haskell, append an underscore: `type_`.

Use the common idiom of appending tick marks (`'`) to names to represent altered
values like: `fib` and `fib'`.

Use the common idiom of plural for the lists: For example, a pattern match
against a list might be `(a:as)`. (See also Short Variables, below.)

```haskell
simpleMetricComputer :: Double -> Set Things -> Double
simpleMetricComputer _ things = ...
    -- it isn't clear what the first argument is

map :: (a -> b) -> [a] -> [b]
map _f [] = []
map f (a:as) = f a : map f as
    -- no need to name _f in first clause, as it is clear from the second clause
```

```haskell
simpleMetricComputer :: Double -> Set Things -> Double
simpleMetricComputer _sizeHint things = ...
    -- clear what the first argument is for, and that it isn't used

map :: (a -> b) -> [a] -> [b]
map _ [] = []
map f (a:as) = f a : map f as
    -- first argument in first clause is clear from context and second clause
```

<a id="Short_Variables"></a>
### Short Variables 

Short and single letter variable names are fine.

Where the scope of a variable name is over just a few lines, short or single
letter variable names are acceptable and even encouraged. Generally, they help
expose the structure of the code.

```haskell
nextAfter :: Eq element => element -> [element] -> Maybe element
nextAfter match (current:next:remainder) =
    if current == match then Just next
                        else nextAfter match (next:remainder)
nextAfter _ _ = Nothing
```

```haskell
nextAfter :: Eq a => a -> [a] -> Maybe a
nextAfter m (x:y:ys) =
    if x == m then Just y
              else nextAfter m (y:ys)
nextAfter _ _ = Nothing
```

<a id="Module_Names"></a>
### Modules 

Use singular when naming modules.

Use `Data.Map` and `Data.ByteString.Internal` instead of `Data.Maps` and
`Data.ByteString.Internals`.

<a id="Abbreviations"></a>
### Abbreviations 

Abbreviations in names should be mixed-case.

```haskell
HTTPResponse
IPBlock
```

```haskell
HttpResponse
IpBlock
```

**Exception:** There are a few cases where there is considerable precedent for a
particular case usage of a term. In this case, it is acceptable to retain a
specific choice. Note that this does not apply to things like `HTTP` which are
all caps in common usage simply because they are an abbreviation.

```haskell
GREoIPsec  -- acceptable because specific precedent for this form exists
```

<a id="Formatting"></a>
## Formatting 

<a id="Vertical_Spacing"></a>
### Vertical Spacing 

Vertical white space is to be used sparingly, ensuring that more context can be
seen in a screenful.

In general, one blank line is enough to separate declarations. Two blank lines
should be used between the module imports and the first top level declaration,
and between major sections of the file, if needed. No blank lines are required
between declarations in a where clause, but are sometimes used if there are many
or longer declarations.

```haskell
{-# OPTIONS_GHC -fno-warn-orphans #-}
{-# LANGUAGE TupleSections #-}

-- | Run-length encoding types and functions.
--
-- Run-length encoded sequences are a quick and efficient compression scheme
-- that is so on and so forth....

module RunLength
    ( RunList
    , rleEncode
    , relDecode
    ) where

import Data.List (replicate)


type RunList a = [(Int, a)]

-- | Run-length encode a sequence of elements.
rleEncode :: (Eq a) => [a] -> RunList a
rleEncode [] = []
rleEncode (a:as) = go 1 a as
  where
    go n a [] = [(n,a)]
    go n a (b:bs) | a == b    =         go (n+1) b bs
                  | otherwise = (n,a) : go 1     b bs
-- | Run-length decode a RunList.
rleDecode :: RunList a -> [a]
rleDecode = concatMap (uncurry replicate)
```

<a id="Horizontal_Spacing"></a>
### Horizontal Spacing 

*   80 columns wide
*   No trailing spaces

The aim is to have horizontal spacing help show the structure of the
expressions. It is acceptable, and even encouraged, to use horizontal spacing to
make the structural relationship between clauses clear.

```haskell
-- | Run-length encode a sequence of elements.
rleEncode :: (Eq a) => [a] -> RunList a
rleEncode [] = []
rleEncode (a:as) = go 1 a as
  where                        -- see rules for "where" below
    go n a [] = [(n,a)]
    go n a (b:bs) | a == b    =         go (n+1) b bs
                  | otherwise = (n,a) : go 1     b bs
```

Data declarations should also follow these rules:

```haskell
data Tree a = Branch a (Tree a) (Tree a)
            | Leaf

data HttpException
    = InvalidStatusCode Int
    | MissingContentHeader
```

<a id="Indentation"></a>
### Indentation 

*   Indents on 4 space intervals
*   No tabs

As indents serve an important semantic function in Haskell, the indents are on 4
space intervals.

Parts of an expression that are continued on another line, are indented one
indent from the indent of the preceding line, not from the construct that they
are continuting. (Though see the preceding section about using alignment to make
structure clear, and use your judgement.)

```haskell
arbitrary = arbitrary >>= \b -> if b
    then do
        cidr <- choose (0, 32)
        ip <- pick 32 cidr
        return $ makeBlock (IPv4 ip) cidr
    else do
        cidr <- choose (0, 64)
        hi <- pick 64 cidr
        lo <- pick 64 (cidr - 64)
        return $ makeBlock (IPv6 hi lo) cidr
```

<a id="Comment_Formatting"></a>
### Comments 

*   Use `--` comments
*   Use 2 or more spaces between code and comments

Separate end-of-line comments from the code using 2 spaces. Align comments for
data type definitions:

```haskell
data CommandSummary = CommandSummary
    { ciName :: T.Text        -- ^ name and short summary on one line
    , ciSynopsis :: T.Text    -- ^ invocation template, like "foo [-f] file..."
    , ciOptions :: [([T.Text], T.Text)]
                              -- ^ a list of pairs of options synonyms and their
                              -- summary description
    }
```

<a id="Where"></a>
### where 

To separate the local declarations from the main expression, use a *hanging
indent* for `where`. For all other uses (module, class, and instance
declarations), use trailing `where`.

```haskell
module Main.TestRouters
    ( TestPrefix, TestMetric(..)
    , prop_routeSameAsNaive
    ) where

class PrefixLength a where
    prefixLength :: a -> Int

instance Arbitrary TestMetric where
    arbitrary = arbitraryBoundedEnum
    shrink = shrinkNothing

updateFlowTable :: (Ord m, Eq p) =>
    FlowMod m p t -> FlowTable m p t -> FlowTable m p t
updateFlowTable u tbl = case u of
    AddFlow m p t -> let (cs,ds) = break ((<= m) . fst) (clean p)
                     in cs ++ (m, (p, t)) : ds
    DeleteFlow p  -> clean p
  where
    clean p = filter ((/= p) . fst . snd) tbl
```

<a id="Deriving"></a>
### deriving 

The `deriving` clause can trail the declaration, or go on a line of its own.

```haskell
data Light = Stop | Slow | Go
    deriving (Eq, Ord, Enum, Bounded, Show)

newtype Max a = Max a deriving (Eq, Ord, Show)

data HttpStats
    = StatusOk
    | StatusRedirectMoved
    | StatusRedirectTemporary
    | StatusNotFound
    deriving (Eq, Show)

data Employee = Employee
    { empName :: String
    , empId :: Integer
    , empDepartment :: Integer
    } deriving (Eq, Ord, Show)
```

<a id="case_of"></a>
### case…of 

The `of` token appears on the same line as the `case` token. Indent the cases.

Align the `->` arrows when it helps readability.

```haskell
foobar = case something of
    Just j  -> foo
    Nothing -> bar
```

<a id="let_in"></a>
### let…in 

The `in` token appears on the line after the line with the `let` token, lined up
with it.

```haskell
access add = let (s,a) = add `divMod` segmentSize
                 (p,b) = a `divMod` pageSize
             in getPageByte b . getSegmentPage p <$> getSegment s
```

If short, the whole `let` expression can be all on one line:

```haskell
formatItem x = let (a,b) = x `divMod` 1000 in show a ++ '/' : show b
```

<a id="if_then_else_2"></a>
### if…then…else 

Indent the `then` and `else`.

The `then` and `else` are indented from the indent level of the line containing
the `if`, not from the `if` itself.

```haskell
foo = if ....
    then ...
    else ...

foo = do
    someCode
    if condition
        then someMoreCode
        else someAlternativeCode

foo = bar $ \qux -> if predicate qux
    then doSomethingSilly
    else someOtherCode
```

The same rule applies to do blocks nested within:

```haskell
foo = do
    instruction <- decodeInstruction
    skip <- load Memory.skip
    if skip == 0x0000
        then do
            execute instruction
            addCycles $ instructionCycles instruction
        else do
            store Memory.skip 0x0000
            addCycles 1
```

**Exception:** If the expressions are short, it is acceptable to have the whole
expression on one line:

```haskell
adjective n = if odd n then "odd" else "even"
```

<a id="List_Formatting"></a>
### List Formatting 

Use "leading comma" list format for multiple line spanning lists.

Lists and other constructs that are surrounded by parenthesis or braces, and are
extended over several lines, should be formatted such that a comma starts the
subsequent lines, and the closing punctuation is on a line by itself. This
applies to export lists, import lists, list values, record field declarations,
and record values.

It is acceptable to have several values on a single line, "comma space"
separated if they are grouped logically together.

```haskell
exceptions =
    [ InvalidStatusCode
    , MissingContentHeader
    , InternalServerError
    ]
```

```haskell
data Person = Person
    { firstName :: !String  -- ^ First name
    , lastName  :: !String  -- ^ Last name
    , age       :: !Int     -- ^ Age
    } deriving (Eq, Show)
```

```haskell
module CPU
    ( CpuState(..), powerOnState

    , zeroPage
    , bitN, bitV, bitD, bitI, bitZ, bitC

    , assignBit
    , assignZN

    , setZN, setAZN, setXZN, setYZN
    , setZVNbit, setACZVN, setCZN

    , fetch, store
    , clearBus
    , fetchIndirectAddr
    , nextPC, fetchPC

    , push, pull, pushAddr, pullAddr, pushP, pullP
    ) where
```

<a id="Operators_Punctuation"></a>
### Operators & Punctuation 

Use one space around all operators. Use one space after commas and semicolons.
Use no space after a backslash token.

```haskell
sumSqDelta = dSumSqDelta + delta' * (val' - mean)

(rib', fib') = process updates rib

\s -> s ++ reverse s      -- note: \ is not an operator, no trailing space

quarterlyIncome `mod` 10  -- treat identifiers used as an operator the same

foldr (*) 1 list          -- treat operator in parenthesis as an identifier
```

For operator sections, don't add a space on the "unapplied" side:

```haskell
map (++ " likes noodles") people
```

**Exception:** For tuples and common operations consisting of single character
values, it is acceptable to elide the space after the comma or operator when it
improves readability:

```haskell
swap (a,b) = (b,a)

foldl' (\v d -> 10*v + digitToInt d) 0

go n m (a:as) | m == a = go (n+1) m as
```

<a id="Parting_Words"></a>
## Parting Words 

Use common sense and *BE CONSISTENT*.

If you are editing code, take a few minutes to look at the code around you and
determine its style, and mirror it.

The point of having style guidelines is to have a common vocabulary of coding so
people can concentrate on what you are saying, rather than on how you are saying
it. We present global style rules here so people know the vocabulary. But local
style is also important. If code you add to a file looks drastically different
from the existing code around it, the discontinuity throws readers out of their
rhythm when they go to read it. Try to avoid this.

OK, enough writing about writing code; the code itself is much more interesting.
Have fun!
