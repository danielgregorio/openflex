# OpenFlex Architecture

## Overview

OpenFlex is a multi-phase compiler that transforms ActionScript 4 + MXML into modern JavaScript with a reactive runtime.

```
Source Code (MXML/AS4)
         ↓
    [Parser]
         ↓
       AST
         ↓
  [Type Checker]
         ↓
   Typed AST
         ↓
   [Optimizer]
         ↓
  Optimized AST
         ↓
  [Code Generator]
         ↓
  JavaScript + Runtime
```

## Compiler Phases

### 1. Parser Phase

**Input**: `.mxml` and `.as4` source files
**Output**: Abstract Syntax Tree (AST)

**Components**:
- **MXML Parser** (`compiler/parser/mxml_parser.py`)
  - Parses XML structure using `lxml`
  - Extracts `<fx:Script>` blocks
  - Extracts `<fx:Style>` CSS
  - Builds component tree

- **AS4 Parser** (`compiler/parser/as4_parser.py`)
  - Uses tree-sitter for proper parsing
  - Handles modern AS4 syntax:
    - Nullable types `T?`
    - Union types `T | U`
    - Pattern matching
    - Async/await
    - Signals

**AST Structure** (`compiler/parser/ast.py`):
```python
Program
├── imports: List[ImportDeclaration]
├── declarations: List[Statement]
│   ├── VariableDeclaration
│   ├── FunctionDeclaration
│   ├── ClassDeclaration
│   └── InterfaceDeclaration
└── component: Component (for MXML)
```

### 2. Type Checker Phase

**Input**: AST
**Output**: Typed AST with semantic information

**Components**:
- **Symbol Table** (`compiler/analyzer/scope.py`)
  - Tracks variables, functions, classes
  - Handles scope nesting
  - Resolves identifiers

- **Type Checker** (`compiler/analyzer/type_checker.py`)
  - Type inference
  - Type compatibility checking
  - Null safety validation
  - Generic constraint checking

**Type System Features**:
```actionscript
// Null safety
var nullable: String? = null;     // OK
var notNull: String = null;       // ERROR

// Type inference
var count = 0;                    // Inferred as Number
const name = "Alice";             // Inferred as String

// Union types
var result: Success | Error;

// Generics
function map<T, U>(arr: Array<T>, fn: (T) => U): Array<U>
```

### 3. Optimizer Phase

**Input**: Typed AST
**Output**: Optimized AST

**Optimizations**:
- Dead code elimination
- Constant folding
- Inline small functions
- Remove unused imports
- Tree shaking

Example:
```actionscript
// Before
const DEBUG = false;
if (DEBUG) {
    console.log("debug");  // Dead code
}

// After
// (removed completely)
```

### 4. Code Generator Phase

**Input**: Optimized AST
**Output**: JavaScript + Runtime calls

**Components**:
- **JS Emitter** (`compiler/codegen/js_emitter.py`)
  - Converts AST to JavaScript
  - Generates ES2022 modules
  - Preserves semantics

- **Source Map Generator** (`compiler/codegen/sourcemap.py`)
  - Maps generated JS back to source
  - For debugging

**Code Generation Examples**:

```actionscript
// AS4
const count = signal(0);

function increment(): void {
    count.set(count() + 1);
}
```

↓

```javascript
// Generated JS
import { signal } from '@openflex/runtime';

const count = signal(0);

function increment() {
    count.set(count() + 1);
}
```

## Runtime Architecture

### Reactive Core

**Signals** (`runtime/reactive.js`):
```javascript
class Signal {
    constructor(value) {
        this._value = value;
        this._subscribers = new Set();
    }

    get() {
        // Track dependency
        if (currentEffect) {
            this._subscribers.add(currentEffect);
        }
        return this._value;
    }

    set(value) {
        this._value = value;
        // Notify subscribers
        this._subscribers.forEach(effect => effect.run());
    }
}
```

**Effects**:
```javascript
class Effect {
    constructor(fn) {
        this.fn = fn;
        this.run();
    }

    run() {
        currentEffect = this;
        this.fn();
        currentEffect = null;
    }
}
```

### Component System

**Virtual DOM** (`runtime/vdom.js`):
- Lightweight virtual DOM
- Efficient diffing algorithm
- Minimal re-renders

**Components** (`runtime/components/`):
- VBox, HBox, Button, Label, etc.
- Reactive properties
- Event handling

## Data Flow

```
User Action (click)
       ↓
Event Handler (AS4 function)
       ↓
Signal Update (count.set())
       ↓
Effect Triggers
       ↓
Component Re-render
       ↓
DOM Update
```

## Module System

### Import Resolution

```actionscript
// Standard library
import { signal } from "openflex/reactive";

// Relative imports
import { Button } from "./components/Button.mxml";

// npm packages (future)
import axios from "axios";
```

### Module Output

Each MXML/AS4 file becomes an ES module:
```javascript
// App.mxml → App.js
import { VBox, Label } from '@openflex/runtime';

export default function App() {
    // Component logic
    return VBox({ /* ... */ });
}
```

## Build Pipeline

```
1. Parse Entry File
2. Resolve Imports
3. Parse Dependencies
4. Type Check All
5. Optimize All
6. Generate Code
7. Bundle (optional)
8. Output to dist/
```

## Performance Considerations

### Compile-Time
- Tree-sitter: Fast parsing (~100k lines/sec)
- Incremental compilation: Cache AST
- Parallel type checking: Multi-threaded

### Runtime
- Signals: O(1) updates
- Virtual DOM: Minimal diffing
- Code splitting: Lazy load components

## Error Handling

### Compile Errors

Rich error messages with context:
```
Error: Type mismatch
  ┌─ App.mxml:10:15
  │
10│     var x: String = 123;
  │                     ^^^ Expected String, got Number
  │
```

### Runtime Errors

Source maps enable debugging in original AS4:
```javascript
// Generated JS
function foo() { /* line 100 */ }

// Stack trace points to:
// App.mxml:15 (original source)
```

## Testing Strategy

### Unit Tests
- Parser: Test AST generation
- Type Checker: Test type inference
- Codegen: Test output correctness

### Integration Tests
- Full compilation pipeline
- Example apps compile
- Runtime behavior

### E2E Tests
- Browser tests with Playwright
- Component rendering
- User interactions

## Future Architecture

### WebAssembly Target

```
AS4 → LLVM IR → WASM
     ↓
  Rust Runtime (WASM)
     ↓
  Canvas/WebGL Rendering
```

### Multi-Platform

- Web (JavaScript/WASM)
- Desktop (Tauri/Electron)
- Mobile (React Native bridge)
- Terminal (TUI with blessed)

## Directory Structure

```
compiler/
├── parser/
│   ├── ast.py          # AST node definitions
│   ├── types.py        # Type system
│   ├── mxml_parser.py  # MXML → AST
│   └── as4_parser.py   # AS4 → AST
├── analyzer/
│   ├── type_checker.py # Type inference & checking
│   ├── scope.py        # Symbol table
│   └── errors.py       # Error reporting
├── codegen/
│   ├── js_emitter.py   # AST → JavaScript
│   └── sourcemap.py    # Source map generation
└── cli.py              # Command-line interface

runtime/
├── reactive.js         # Signals & effects
├── vdom.js             # Virtual DOM
├── components/         # UI components
│   ├── Application.js
│   ├── VBox.js
│   ├── Button.js
│   └── ...
└── index.js            # Runtime exports
```

## Design Principles

1. **Correctness First**: Types prevent bugs
2. **Fast Feedback**: Quick compile times, good errors
3. **Zero Cost Abstractions**: Pay only for what you use
4. **Interop Friendly**: Works with existing JS ecosystem
5. **Progressive Enhancement**: Start simple, add features gradually

---

For implementation details, see individual module documentation.
