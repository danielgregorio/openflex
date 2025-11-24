# Tree-sitter Grammar for ActionScript 4

Tree-sitter grammar for ActionScript 4 (OpenFlex Neo) including all modern language features.

## Features

This grammar supports:

### Core AS4 Syntax
- Variables and constants (`var`, `const`)
- Functions (`function`, `async function`)
- Classes and interfaces
- Traits (AS4 extension)
- Type annotations
- Generics

### Modern Type System
- Nullable types (`String?`)
- Union types (`Success | Error`)
- Array types (`Array<T>`)
- Function types (`(T) => U`)
- Type aliases (`type Result<T, E> = ...`)

### Reactive Decorators
- `@reactive` - Reactive variables
- `@computed` - Computed values
- `@effect` - Side effects
- Custom decorators

### Conditional Compilation
- `#if FLAG` - Conditional blocks
- `#elif FLAG` - Else-if conditions
- `#else` - Else blocks
- `#endif` - End conditional
- Boolean logic (`&&`, `||`, `!`)

### Pattern Matching
- `match` expressions and statements
- Pattern destructuring
- Guards
- Exhaustiveness checking (via type system)

### Import System
- AS3-style imports (`import package.Class`)
- Wildcard imports (`import package.*`)
- Aliasing (`import package.Class as Alias`)

### Modern Features
- Async/await
- Arrow functions
- Template strings
- Optional chaining (`?.`)
- Spread operator (`...`)
- Destructuring

## Installation

```bash
cd compiler/parser/tree-sitter-as4
npm install
npm run build
```

## Usage

### Node.js

```javascript
const Parser = require('tree-sitter');
const AS4 = require('tree-sitter-actionscript4');

const parser = new Parser();
parser.setLanguage(AS4);

const sourceCode = `
@reactive var count: Number = 0;

function increment(): void {
    count++;
}
`;

const tree = parser.parse(sourceCode);
console.log(tree.rootNode.toString());
```

### Python (via py-tree-sitter)

```python
from tree_sitter import Language, Parser

# Build the language
Language.build_library(
    'build/as4.so',
    ['compiler/parser/tree-sitter-as4']
)

# Load and use
AS4_LANGUAGE = Language('build/as4.so', 'actionscript4')
parser = Parser()
parser.set_language(AS4_LANGUAGE)

source = b"""
@reactive var count: Number = 0;
"""

tree = parser.parse(source)
print(tree.root_node.sexp())
```

## Grammar Structure

### Entry Point
```
source_file -> statement*
```

### Statements
- `import_statement` - Import declarations
- `variable_declaration` - Variable/constant declarations
- `function_declaration` - Function definitions
- `class_declaration` - Class definitions
- `interface_declaration` - Interface definitions
- `trait_declaration` - Trait definitions
- `type_alias` - Type alias declarations
- `conditional_compilation_block` - #if blocks
- Control flow: `if`, `for`, `while`, `match`
- `return`, `break`, `continue`, `throw`, `try`

### Expressions
- Literals: `number`, `string`, `boolean`, `null`
- Binary operations: `+`, `-`, `*`, `/`, `==`, `&&`, etc.
- Unary operations: `-`, `!`, `++`, `--`
- `call_expression` - Function calls
- `member_expression` - Property access
- `new_expression` - Object creation
- `array_literal` - Array literals
- `object_literal` - Object literals
- `arrow_function` - Arrow functions
- `await_expression` - Await expressions
- `match_expression` - Pattern matching
- `ternary_expression` - Conditional expressions

### Types
- `identifier` - Simple types
- `nullable_type` - `T?`
- `union_type` - `T | U`
- `array_type` - `Array<T>`
- `generic_type` - `Map<K, V>`
- `function_type` - `(T) => U`

## Testing

```bash
npm test
```

Test files are in `test/corpus/`.

## Syntax Highlighting

Syntax highlighting queries are in `queries/highlights.scm` for editor integration.

## License

MIT
