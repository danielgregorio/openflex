# OpenFlex Project Structure

## 📁 Complete Directory Tree

```
openflex/
│
├── 📄 README.md                    # Project overview and vision
├── 📄 LICENSE                      # MIT License
├── 📄 pyproject.toml              # Python project configuration
├── 📄 requirements.txt            # Python dependencies
├── 📄 setup.sh                    # Quick setup script
├── 📄 .gitignore                  # Git ignore rules
│
├── 📁 compiler/                   # Compiler implementation
│   ├── __init__.py
│   ├── cli.py                     # Command-line interface
│   │
│   ├── 📁 parser/                 # Parsing phase
│   │   ├── __init__.py
│   │   ├── ast.py                 # ⭐ AST node definitions (60+ types)
│   │   ├── types.py               # ⭐ Type system (primitives, utilities)
│   │   ├── mxml_parser.py         # TODO: MXML → AST
│   │   └── as4_parser.py          # TODO: AS4 → AST (tree-sitter)
│   │
│   ├── 📁 analyzer/               # Analysis phase
│   │   ├── __init__.py
│   │   ├── type_checker.py        # TODO: Type inference & checking
│   │   ├── scope.py               # TODO: Symbol table management
│   │   └── errors.py              # TODO: Error reporting
│   │
│   └── 📁 codegen/                # Code generation phase
│       ├── __init__.py
│       ├── js_emitter.py          # TODO: AST → JavaScript
│       └── sourcemap.py           # TODO: Source map generation
│
├── 📁 runtime/                    # Runtime library (JavaScript)
│   ├── reactive.js                # TODO: Signals & effects
│   ├── vdom.js                    # TODO: Virtual DOM
│   ├── index.js                   # TODO: Runtime exports
│   └── 📁 components/             # TODO: UI component library
│       ├── Application.js
│       ├── VBox.js
│       ├── HBox.js
│       ├── Button.js
│       ├── Label.js
│       └── ...
│
├── 📁 examples/                   # Example applications
│   ├── README.md                  # Examples documentation
│   │
│   ├── 📁 hello-world/            # Basic example
│   │   └── App.mxml               # Simple hello world
│   │
│   ├── 📁 counter/                # Reactive example
│   │   └── App.mxml               # Counter with signals
│   │
│   └── 📁 todo-app/               # TODO: Full CRUD example
│
├── 📁 tests/                      # Test suite
│   ├── 📁 parser/                 # Parser tests
│   ├── 📁 analyzer/               # Type checker tests
│   └── 📁 codegen/                # Code generation tests
│
├── 📁 docs/                       # Documentation
│   ├── ARCHITECTURE.md            # ⭐ Detailed architecture
│   ├── PROJECT_STRUCTURE.md       # This file
│   ├── ROADMAP.md                 # TODO: Development roadmap
│   └── AS4_SPEC.md                # TODO: Language specification
│
└── 📁 reference-quantum/          # Reference implementation
    └── (quantum-as4 code)         # For reference only
```

## 🎯 Implementation Status

### ✅ Completed (Foundation)

- [x] Project structure
- [x] AST type definitions (60+ node types)
- [x] Type system foundations
- [x] CLI interface skeleton
- [x] Documentation structure
- [x] Examples (2 MXML apps)
- [x] Python package config

### 🚧 In Progress (Next Steps)

- [ ] Tree-sitter grammar for AS4
- [ ] MXML parser implementation
- [ ] AS4 parser implementation
- [ ] Type checker
- [ ] Code generator

### 📋 Planned

- [ ] Reactive runtime (signals)
- [ ] Virtual DOM
- [ ] Component library
- [ ] Hot reload
- [ ] Source maps
- [ ] WebAssembly target

## 📊 Code Statistics

### Python (Compiler)

| File | Lines | Purpose |
|------|-------|---------|
| `compiler/parser/ast.py` | ~450 | AST definitions |
| `compiler/parser/types.py` | ~130 | Type system |
| `compiler/cli.py` | ~200 | CLI interface |
| **Total** | **~780** | Foundation complete |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `docs/ARCHITECTURE.md` | Technical architecture |
| `docs/PROJECT_STRUCTURE.md` | This file |
| `examples/README.md` | Example documentation |

### Examples

| Example | Lines | Features |
|---------|-------|----------|
| `hello-world` | ~20 | Basic MXML, data binding |
| `counter` | ~45 | Signals, computed values |
| `todo-app` | TBD | Full CRUD (planned) |

## 🗂️ Key Files Explained

### Core Compiler Files

#### `compiler/parser/ast.py`
**Purpose**: Define all AST node types for AS4

**Contains**:
- Base types: `ASTNode`, `SourceLocation`
- Type nodes: `Type`, `PrimitiveType`, `ArrayType`, `UnionType`, etc.
- Expression nodes: `Identifier`, `Literal`, `BinaryExpression`, etc.
- Statement nodes: `VariableDeclaration`, `FunctionDeclaration`, etc.
- Declaration nodes: `ClassDeclaration`, `InterfaceDeclaration`, etc.
- Program root: `Program`

**Example**:
```python
@dataclass
class VariableDeclaration(Statement):
    name: str
    var_type: Optional[Type]
    initializer: Optional[Expression]
    is_const: bool = False
    is_bindable: bool = False
```

#### `compiler/parser/types.py`
**Purpose**: Built-in types and type utilities

**Contains**:
- `BuiltinTypes`: All primitive types (Number, String, Boolean, etc.)
- `TYPE_MAP`: Name → Type mapping
- Type utilities: `is_numeric()`, `is_assignable()`, `make_nullable()`, etc.

#### `compiler/cli.py`
**Purpose**: Command-line interface

**Commands**:
- `openflex build` - Compile files
- `openflex dev` - Dev server
- `openflex check` - Type check
- `openflex init` - New project

### Configuration Files

#### `pyproject.toml`
**Purpose**: Python project metadata and dependencies

**Key sections**:
- `[project]`: Package info, dependencies
- `[project.scripts]`: CLI entry point
- `[tool.black]`: Code formatter config
- `[tool.pytest]`: Test configuration

#### `requirements.txt`
**Purpose**: Python dependencies list

**Dependencies**:
- `tree-sitter`: Parser generator
- `lxml`: XML parsing
- `click`: CLI framework
- `rich`: Terminal formatting
- `pydantic`: Data validation

## 🎨 AST Design Highlights

### Type System

```python
# Primitive
Number, String, Boolean, void, any

# Complex
Array<T>              # Generic array
Map<K, V>            # Generic map
T | U                # Union type
T?                   # Nullable type
(T) => U             # Function type
```

### Expression Nodes

```python
Literal              # 42, "hello", true
Identifier           # variable name
BinaryExpression     # a + b
CallExpression       # foo(1, 2)
MemberExpression     # obj.prop
ArrowFunction        # (x) => x * 2
AwaitExpression      # await promise
```

### Statement Nodes

```python
VariableDeclaration  # var x: Number = 5
FunctionDeclaration  # function foo(): void {}
ClassDeclaration     # class User { }
IfStatement          # if (x) { }
ForStatement         # for (;;) { }
MatchStatement       # match x { }
```

## 🔄 Compilation Flow

```
1. Input: App.mxml
   ↓
2. MXML Parser
   → Extract <fx:Script>
   → Parse component tree
   ↓
3. AS4 Parser (tree-sitter)
   → Parse ActionScript
   → Build AST
   ↓
4. Type Checker
   → Infer types
   → Validate
   ↓
5. Optimizer
   → Dead code elimination
   → Constant folding
   ↓
6. Code Generator
   → Emit JavaScript
   → Generate source maps
   ↓
7. Output: App.js + runtime
```

## 🚀 Getting Started

### Setup

```bash
# Clone and setup
git clone <repo>
cd openflex
./setup.sh

# Or manually
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Try CLI

```bash
# Check version
openflex version

# Create new project
openflex init my-app

# Build example
openflex build examples/hello-world/App.mxml
```

## 📚 Next Steps

See [ROADMAP.md](ROADMAP.md) for detailed implementation plan.

### Phase 1: Parser (Current)
1. Write tree-sitter grammar for AS4
2. Implement MXML parser
3. Test with examples

### Phase 2: Type Checker
1. Symbol table
2. Type inference
3. Error reporting

### Phase 3: Code Generator
1. AST → JavaScript
2. Source maps
3. Runtime integration

---

**Status**: Foundation Complete ✅
**Next**: Implement parsers 🚧
