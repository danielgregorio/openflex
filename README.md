# 🚀 OpenFlex

**ActionScript 4 + MXML → Modern Web Platform**

OpenFlex is a modern compiler and runtime that brings ActionScript/Flex concepts into 2025 with contemporary features like signals, pattern matching, null safety, and WebAssembly support.

## 🎯 Vision

ActionScript 3 was ahead of its time with strong typing, MXML declarative UI, and data binding. Flash died, but the ideas were brilliant. OpenFlex evolves these concepts with modern features:

- **ActionScript 4**: Modern language features (null safety, pattern matching, async/await, signals)
- **MXML 2.0**: Declarative UI with reactive data binding
- **Multiple Targets**: JavaScript, TypeScript, WebAssembly
- **Modern Runtime**: Reactive signals (à la Solid.js), Virtual DOM
- **Type Safety**: Full type inference and checking
- **Developer Experience**: Fast builds, hot reload, excellent errors

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           OpenFlex Compiler             │
├─────────────────────────────────────────┤
│  1. Parser (tree-sitter)                │
│     • MXML → AST                        │
│     • AS4 → AST                         │
│                                         │
│  2. Type Checker                        │
│     • Type inference                    │
│     • Null safety                       │
│     • Generic constraints               │
│                                         │
│  3. Optimizer                           │
│     • Dead code elimination             │
│     • Constant folding                  │
│                                         │
│  4. Code Generator                      │
│     • JavaScript (ES2022)               │
│     • TypeScript                        │
│     • WebAssembly (future)              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│          OpenFlex Runtime               │
├─────────────────────────────────────────┤
│  • Reactive Signals                     │
│  • Virtual DOM                          │
│  • Component System                     │
│  • Event Handling                       │
│  • Data Binding                         │
└─────────────────────────────────────────┘
```

## ✨ Language Features (ActionScript 4)

### Modern Type System

```actionscript
// Null Safety
var name: String? = null;  // Explicitly nullable
var count: Number = 0;     // Never null

// Pattern Matching
match result {
    Success(value) => trace("Got: " + value),
    Error(msg) => trace("Error: " + msg)
}

// Union Types
type Result<T, E> = Success<T> | Error<E>;

// Async/Await
async function fetchUser(id: String): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    return await response.json();
}
```

### Reactive Programming

```actionscript
import { signal, computed, effect } from "openflex/reactive";

// Signals (reactive state)
const count = signal(0);
const doubled = computed(() => count() * 2);

// Effects (side effects)
effect(() => {
    trace("Count changed: " + count());
});

count.set(5);  // Automatically triggers effect
```

### MXML 2.0 - Declarative UI

```xml
<s:Application xmlns:fx="http://ns.adobe.com/mxml/2009"
               xmlns:s="library://ns.adobe.com/flex/spark">

    <fx:Script>
        import { signal } from "openflex/reactive";

        const count = signal(0);

        function increment(): void {
            count.set(count() + 1);
        }
    </fx:Script>

    <s:VBox gap={16}>
        <s:Label text="Count: {count()}" fontSize={24} />
        <s:Button label="Increment" click={increment} />
    </s:VBox>

</s:Application>
```

## 🚀 Getting Started

### Installation

```bash
# Using pip
pip install openflex

# From source
git clone https://github.com/danielgregorio/openflex.git
cd openflex
pip install -e .
```

### Quick Start

```bash
# Create new project
openflex init my-app
cd my-app

# Build
openflex build src/App.mxml

# Development with watch
openflex build src/App.mxml --watch

# Type check
openflex check src/App.mxml
```

### Example Project Structure

```
my-app/
├── src/
│   ├── App.mxml           # Main application
│   ├── components/        # UI components
│   │   ├── Button.mxml
│   │   └── Card.mxml
│   └── lib/               # AS4 libraries
│       └── utils.as4
├── public/
│   └── index.html
├── openflex.config.json
└── package.json
```

## 📚 Documentation

### Compiler Pipeline

1. **Parser**: Converts MXML/AS4 source to Abstract Syntax Tree (AST)
2. **Type Checker**: Validates types, infers missing annotations
3. **Optimizer**: Eliminates dead code, constant folding
4. **Code Generator**: Outputs JavaScript/TypeScript/WASM

### Type System

- **Primitives**: `Number`, `String`, `Boolean`, `int`, `uint`
- **Collections**: `Array<T>`, `Map<K,V>`, `Set<T>`
- **Nullable**: `T?` (explicit null types)
- **Union**: `T | U` (sum types)
- **Generics**: `Box<T>`, `Result<T, E>`

### Component Library

OpenFlex includes Flex Spark components modernized for 2025:

- **Layout**: `VBox`, `HBox`, `Grid`, `Spacer`
- **Controls**: `Button`, `TextInput`, `CheckBox`, `RadioButton`
- **Display**: `Label`, `Image`, `Panel`
- **Data**: `DataGrid`, `List`, `Tree`

## 🛠️ Development Status

**Current Phase**: Foundation (0.1.0-alpha)

- [x] Project structure
- [x] AST definitions
- [x] Type system foundation
- [x] CLI interface
- [ ] Tree-sitter grammar for AS4
- [ ] MXML parser
- [ ] Type checker
- [ ] JavaScript code generator
- [ ] Reactive runtime
- [ ] Component library
- [ ] Hot reload
- [ ] Source maps

See [ROADMAP.md](docs/ROADMAP.md) for detailed plans.

## 🤝 Contributing

OpenFlex is in early development. Contributions welcome!

```bash
# Clone and setup
git clone https://github.com/danielgregorio/openflex.git
cd openflex
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black compiler/
ruff check compiler/
```

## 📖 History & Inspiration

OpenFlex is inspired by:
- **Adobe Flex/Apache Royale**: MXML declarative UI
- **TypeScript**: Gradual typing, excellent DX
- **Rust**: Null safety, pattern matching, trait system
- **Solid.js**: Reactive signals without Virtual DOM overhead
- **Svelte**: Compile-time optimization

### Why "OpenFlex"?

Flex was closed when Adobe killed Flash. OpenFlex is:
- **Open**: MIT licensed, community-driven
- **Flex**ible: Multiple targets (JS/TS/WASM), modern features
- **Evolutionary**: Not just preserving the past, evolving it

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

## 🌟 Status

**Pre-alpha** - Core architecture in development

Follow development: [@openflex_dev](https://twitter.com/openflex_dev)

---

*"What if ActionScript had evolved instead of dying?"* 💭
