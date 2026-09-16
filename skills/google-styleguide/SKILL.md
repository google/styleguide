---
name: google-styleguide
description: Validates and refactors code in the target codebase to adhere to the official Google Style Guides across multiple supported languages.
---

## Core Concept

The `google-styleguide` skill ensures that a codebase conforms to Google's official style conventions. Because modern codebases often mix multiple languages, this skill helps identify language-specific files and checks each one against its corresponding style guide.

## Supported Style Guides

| Language | File Extensions | Style Guide URL |
| :--- | :--- | :--- |
| **AngularJS** | `.js`, `.html` | [AngularJS Style Guide](guides/angularjs-google-style.html) |
| **Common Lisp** | `.lisp`, `.lsp`, `.cl` | [Common Lisp Style Guide](guides/lispguide.xml) |
| **C++** | `.cpp`, `.cc`, `.cxx`, `.hpp`, `.h`, `.hh` | [C++ Style Guide](guides/cppguide.html) |
| **C#** | `.cs` | [C# Style Guide](guides/csharp-style.md) |
| **Dart** | `.dart` | [Effective Dart](https://www.dartlang.org/guides/language/effective-dart) |
| **Go** | `.go` | [Go Style Guide](guides/go/index.md) |
| **HTML/CSS** | `.html`, `.css` | [HTML/CSS Style Guide](guides/htmlcssguide.html) |
| **JavaScript** | `.js`, `.mjs`, `.cjs` | [JavaScript Style Guide](guides/jsguide.html) |
| **Java** | `.java` | [Java Style Guide](guides/javaguide.html) |
| **JSON** | `.json`, `.jsonc` | [JSON Style Guide](guides/jsoncstyleguide.xml) |
| **Kotlin** | `.kt`, `.kts` | [Kotlin Style Guide](https://developer.android.com/kotlin/style-guide) |
| **Markdown** | `.md` | [Markdown Style Guide](guides/docguide/style.md) |
| **Objective-C** | `.m`, `.mm`, `.h` | [Objective-C Style Guide](guides/objcguide.md) |
| **Python** | `.py`, `.pyi` | [Python Style Guide](guides/pyguide.md) |
| **R** | `.r`, `.R` | [R Style Guide](guides/Rguide.md) |
| **Shell** | `.sh`, `.bash`, `.zsh` | [Shell Style Guide](guides/shellguide.md) |
| **Swift** | `.swift` | [Swift Style Guide](https://google.github.io/swift/) |
| **TypeScript** | `.ts`, `.tsx` | [TypeScript Style Guide](guides/tsguide.html) |
| **Vim script** | `.vim`, `.vimrc` | [Vim script Style Guide](guides/vimscriptguide.xml) |
| **XML** | `.xml` | [XML Document Format Style Guide](guides/xmlstyle.html) |

## Workflow Patterns

When invoked to check or refactor a codebase for style guide compliance:

### 1. Identify File Languages
Scan the current workspace to locate files matching the supported file extensions. Group files by language (e.g., Python files under `.py`, JavaScript files under `.js`).

### 2. Locate and Read the Style Guide
Determine which style guides are needed based on the file types present in the project. For each language under review, refer to the Supported Style Guides table above:
- **Local Guides (Symlinked)**: If the guide points to a local file or folder path (e.g. `guides/cppguide.html`, `guides/pyguide.md`, `guides/go/index.md`, etc.), you **MUST** read the contents of that local file directly from this skill's directory using your file-viewing tools to get the style guidelines.
- **External Guides**: If the guide points to a remote URL (Dart, Kotlin, Swift), access the remote documentation using web browsing/reading tools.

### 3. Core Compliance Auditing
For each file being checked:
1. **Naming Conventions**: Check variable names, class names, method/function names, constants, and file names (e.g., `camelCase` vs `snake_case` or `PascalCase`).
2. **Formatting**: Ensure indentation (e.g., 2 spaces vs 4 spaces vs tabs), maximum line length, and brace placement conform.
3. **Language Features**: Ensure restricted language features are not used (e.g., no global variables, no raw exceptions in C++ unless specified, etc.).
4. **Imports/Includes**: Review import structures, sorting order, and use of absolute vs relative paths.
5. **Comments & Docs**: Ensure docstrings and file comments adhere to formatting, positioning, and language requirements.

### 4. Non-Destructive Refactoring
Make changes to files to match style guide specifications. Use precise code-editing tools to preserve all logic and behavior of the code. Run any existing test suites to verify functionality is not altered by styling changes.
