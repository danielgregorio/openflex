# 🆕 OpenFlex Neo

**ActionScript 4 + MXML → Modern Multi-Platform**

OpenFlex Neo is a modern compiler and runtime that brings ActionScript/Flex concepts into 2025. Write once in AS4/MXML, deploy everywhere: Web, Mobile, Desktop.

**"Neo. Reborn for 2025."**

## 🎉 **Milestone: Working Compiler Achieved!**

**50/53 tests passing (94.3%)** | Type Checker: 100% | Regression: 100% | Codegen: 75%

OpenFlex Neo now has a **complete working compiler pipeline**:
- ✅ AS4 Parser with Tree-sitter
- ✅ Full Type Checker with null safety
- ✅ JavaScript Code Generator
- ✅ Command-line interface (`openflex` command)

```bash
$ ./openflex build examples/hello-world.as4
📄 Compiling examples/hello-world.as4...
✅ Parsed successfully
✅ Generated JavaScript
💾 Saved to examples/hello-world.js
✨ Compilation complete!
```

## 🎯 Vision

ActionScript 3 was ahead of its time with strong typing, MXML declarative UI, and data binding. Flash died, but the ideas were brilliant. OpenFlex Neo evolves these concepts with 2025 features:

- **ActionScript 4**: Null safety, pattern matching, traits, conditional compilation, built-in reactivity
- **MXML Neo**: Declarative UI with reactive data binding, conditional rendering, list iteration
- **Multi-Platform**: One codebase → Web, Mobile, Desktop (conditional compilation prevents bloat)
- **Neo Components**: Platform-agnostic component library
- **Zero Bloat**: Conditional compilation eliminates unused platform code
- **Clean Imports**: AS3-style imports (`import package.Class`), no JS destructuring
- **Type Safety**: Gradual typing with strict mode available
- **Developer Experience**: Fast builds, hot reload, excellent error messages

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

// Union Types (Tagged Unions)
type Result<T, E> = Success<T> | Error<E>;

// Async/Await
async function fetchUser(id: String): Result<User, String> {
    const response = await http.get(`/api/users/${id}`);
    if (response.ok) {
        return Success(response.data);
    }
    return Error("Failed to fetch user");
}
```

### Clean Imports (AS3-style, no destructuring!)

```actionscript
// AS4 Neo - Clean, explicit imports
import openflex.reactive.Signal;
import openflex.reactive.Computed;
import openflex.components.Button;

// Or import entire package
import openflex.reactive.*;

// Usage
const count = new Signal(0);
const doubled = new Computed(() => count.value * 2);
```

### Built-in Reactivity

```actionscript
// Built into the language!
@reactive var count: Number = 0;
@reactive var message: String = "Hello";

// Automatically reactive - updates UI
count++;  // Triggers re-render

// Computed values
@computed var doubled: Number {
    return count * 2;
}

// Effects (side effects)
@effect
function logCount() {
    trace("Count: " + count);
}
```

### Conditional Compilation (Zero Bloat!)

```actionscript
// Platform-specific code is compiled out
#if WEB
import openflex.web.Canvas;

function useWebGL(): void {
    // This code doesn't exist in mobile builds!
}
#endif

#if MOBILE
import openflex.mobile.Camera;

function useCamera(): void {
    // This code doesn't exist in web builds!
}
#endif

// Build flags
const API_URL = #if DEBUG
    "http://localhost:3000"
#else
    "https://api.production.com"
#endif;
```

### MXML Neo - Declarative UI

```xml
<?xml version="1.0" encoding="utf-8"?>
<Application
    xmlns:fx="http://openflex.dev/core"
    xmlns="http://openflex.dev/neo">

    <fx:Script>
        import openflex.reactive.Signal;

        // Built-in reactivity
        @reactive var count: Number = 0;

        function increment(): void {
            count++;  // Automatically updates UI!
        }
    </fx:Script>

    <!-- Neo components (no prefix needed!) -->
    <VBox gap={16}>
        <Label text="Count: {count}" fontSize={24} />
        <Button label="Increment" click={increment} />
    </VBox>

</Application>
```

### MXML Neo Advanced Features

```xml
<Application
    xmlns:fx="http://openflex.dev/core"
    xmlns="http://openflex.dev/neo">

    <fx:Script>
        @reactive var users: Array<User> = [];
        @reactive var loading: Boolean = false;
    </fx:Script>

    <VBox>
        <!-- Conditional rendering -->
        <if test={loading}>
            <Spinner />
        </if>
        <else>
            <!-- List rendering with key -->
            <for each={users} as="user" key="id">
                <UserCard user={user} />
            </for>
        </else>
    </VBox>

</Application>
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
│   ├── app/
│   │   └── App.mxml       # Main application
│   ├── components/        # Reusable components
│   │   ├── Button.mxml
│   │   └── Card.mxml
│   ├── lib/               # AS4 libraries
│   │   └── utils.as4
│   ├── styles/            # CSS styles
│   │   └── theme.css
│   └── assets/            # Images, fonts, etc
│       └── logo.png
├── public/
│   └── index.html
└── openflex.toml          # Project configuration (Maven-like)
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

### Neo Component Library

OpenFlex Neo includes platform-agnostic components (works on Web, Mobile, Desktop):

- **Layout**: `VBox`, `HBox`, `Grid`, `Spacer`, `Stack`
- **Controls**: `Button`, `TextInput`, `CheckBox`, `RadioButton`, `Slider`
- **Display**: `Label`, `Image`, `Panel`, `Card`
- **Data**: `DataGrid`, `List`, `Tree`, `VirtualList`
- **Navigation**: `TabBar`, `TabNavigator`, `Accordion`
- **Feedback**: `Spinner`, `ProgressBar`, `Toast`, `Modal`

All components are:
- ✅ Platform-agnostic (same code, all platforms)
- ✅ Reactive (built-in signal support)
- ✅ Styled with CSS
- ✅ Accessible (ARIA support)

## 🛠️ Development Status

**Current Phase**: Design & Foundation (0.1.0-alpha)

**Completed**:
- [x] Architecture design (multi-platform ready)
- [x] Language features defined (AS4 with modern features)
- [x] Neo namespace and branding
- [x] Project structure
- [x] AST definitions (60+ node types)
- [x] Type system foundation
- [x] CLI interface skeleton
- [x] Import system design (AS3-style)
- [x] Conditional compilation design
- [x] Built-in reactivity design

**In Progress**:
- [ ] Tree-sitter grammar for AS4
- [ ] MXML Neo parser
- [ ] Type checker with null safety
- [ ] JavaScript code generator
- [ ] Conditional compilation implementation
- [ ] Reactive runtime (@reactive, @computed, @effect)
- [ ] Neo component library
- [ ] Platform abstraction layer

**Planned**:
- [ ] Hot reload / HMR
- [ ] Source maps
- [ ] Mobile target (React Native)
- [ ] Desktop target (Tauri)
- [ ] Package manager (OPM)
- [ ] WebAssembly backend

See [docs/](docs/) for detailed specifications.

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

### Why "OpenFlex Neo"?

Flex was closed when Adobe killed Flash. OpenFlex Neo is the evolution:
- **Open**: MIT licensed, community-driven
- **Flex**ible: Multiple targets (Web/Mobile/Desktop), modern features
- **Neo**: Reborn for 2025 with modern language features
- **Zero Bloat**: Conditional compilation means you only ship code for your target platform
- **Clean**: AS3-style imports, no JS ecosystem baggage

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

## 🌟 Status

**Pre-alpha** - Core architecture in development

Follow development: [@openflex_dev](https://twitter.com/openflex_dev)

---

*"What if ActionScript had evolved instead of dying?"* 💭
