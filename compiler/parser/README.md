# OpenFlex AS4 Parser

Python parser for ActionScript 4 using tree-sitter.

## Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install tree-sitter

# Install tree-sitter CLI (for building grammar)
npm install -g tree-sitter-cli
```

### 2. Build Grammar

```bash
# Build the tree-sitter grammar
cd compiler/parser
./build_grammar.sh
```

This will:
1. Generate parser from `tree-sitter-as4/grammar.js`
2. Compile to shared library `tree-sitter-as4/build/as4.so`

## Usage

### Basic Example

```python
from compiler.parser.as4_parser import AS4Parser

parser = AS4Parser()

# Parse AS4 source
source = """
@reactive var count: Number = 0;

function increment(): void {
    count++;
}
"""

ast = parser.parse(source)

# Inspect AST
print(f"Imports: {len(ast.imports)}")
print(f"Declarations: {len(ast.declarations)}")

for decl in ast.declarations:
    print(f"  - {decl.__class__.__name__}: {decl.name if hasattr(decl, 'name') else '?'}")
```

### Parse File

```python
ast = parser.parse_file("examples/counter/App.mxml")
```

## Supported Features

### Core Syntax
- ✅ Variables (`var`, `const`) with type annotations
- ✅ Functions with parameters and return types
- ✅ Imports (AS3-style: `import package.Class`)
- ⏳ Classes (stub)
- ⏳ Interfaces (stub)
- ⏳ Traits (stub)

### Modern Features
- ✅ Decorators (`@reactive`, `@computed`, `@effect`)
- ✅ Type system (nullable `T?`, union `T|U`, arrays `Array<T>`)
- ⏳ Conditional compilation (`#if`, `#elif`, `#else`)
- ⏳ Pattern matching
- ⏳ Async/await

### Expressions
- ✅ Literals (number, string, boolean, null)
- ✅ Identifiers
- ⏳ Binary expressions (`+`, `-`, `*`, `/`, etc.)
- ⏳ Call expressions (`foo()`)
- ⏳ Member expressions (`obj.prop`)

### Statements
- ✅ Variable declarations
- ✅ Function declarations
- ✅ If statements (partial)
- ✅ Return statements
- ⏳ For loops
- ⏳ While loops
- ⏳ Try-catch

Legend:
- ✅ Implemented
- ⏳ Stubbed/Partial
- ❌ Not yet implemented

## Architecture

```
AS4 Source Code
       ↓
tree-sitter Parse
       ↓
tree-sitter Tree
       ↓
ASTVisitor
       ↓
OpenFlex AST (ast.py)
```

### Key Files

- `grammar.js` - Tree-sitter grammar definition
- `as4_parser.py` - Python wrapper
- `ast.py` - AST node definitions
- `types.py` - Type system

## Testing

```bash
# Run parser tests
pytest tests/parser/test_as4_basic.py

# Specific test
pytest tests/parser/test_as4_basic.py::test_reactive_variable
```

## Examples

### Reactive Variable

```python
source = "@reactive var count: Number = 0;"
ast = parser.parse(source)

var_decl = ast.declarations[0]
print(var_decl.name)  # "count"
print(var_decl.decorators[0].name)  # "reactive"
```

### Function with Parameters

```python
source = """
function greet(name: String, age: Number): String {
    return "Hello";
}
"""
ast = parser.parse(source)

func = ast.declarations[0]
print(func.name)  # "greet"
print(len(func.params))  # 2
print(func.params[0].name)  # "name"
```

### Imports

```python
source = """
import openflex.reactive.Signal;
import openflex.components.*;
"""
ast = parser.parse(source)

print(len(ast.imports))  # 2
print(ast.imports[0].source)  # "openflex.reactive.Signal"
```

## Development

### Adding New Features

1. Update `grammar.js` with new syntax
2. Run `./build_grammar.sh` to rebuild
3. Update `as4_parser.py` visitor methods
4. Add AST nodes to `ast.py` if needed
5. Write tests in `tests/parser/`

### Debugging

```python
# Enable tree-sitter debug output
import tree_sitter

parser = AS4Parser()
tree = parser.parser.parse(b"var x = 5;")

# Print S-expression
print(tree.root_node.sexp())
```

## Roadmap

### Phase 1: Core Parsing (Current)
- [x] Variable declarations
- [x] Function declarations
- [x] Import statements
- [x] Decorators
- [x] Basic types

### Phase 2: Complete Statements
- [ ] If/else statements
- [ ] For/while loops
- [ ] Try-catch blocks
- [ ] Match statements

### Phase 3: Complete Expressions
- [ ] Binary/unary operations
- [ ] Call expressions
- [ ] Member access
- [ ] Array/object literals

### Phase 4: Advanced Features
- [ ] Classes with generics
- [ ] Interfaces
- [ ] Traits
- [ ] Conditional compilation
- [ ] Pattern matching

### Phase 5: Optimizations
- [ ] Error recovery
- [ ] Better error messages
- [ ] Performance tuning
- [ ] Incremental parsing

## Troubleshooting

### "Failed to load tree-sitter grammar"

Run the build script:
```bash
./build_grammar.sh
```

### "tree-sitter CLI not found"

Install tree-sitter CLI:
```bash
npm install -g tree-sitter-cli
```

### Grammar changes not taking effect

Rebuild:
```bash
cd compiler/parser/tree-sitter-as4
tree-sitter generate
tree-sitter build
```

## Resources

- [Tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter)
- [AS4 Language Spec](../../docs/AS4_LANGUAGE_SPEC.md)
