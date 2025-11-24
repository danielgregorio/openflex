# OpenFlex Examples

Collection of example applications demonstrating OpenFlex features.

## 📁 Examples

### 1. Hello World
**Path**: `hello-world/`

Basic application showing:
- MXML structure
- Variable declarations
- Data binding `{variable}`
- Event handlers

**Run**:
```bash
openflex build examples/hello-world/App.mxml
```

### 2. Counter
**Path**: `counter/`

Reactive counter demonstrating:
- **Signals**: Reactive state management
- **Computed values**: Derived state
- **Effects**: Side effects
- Multiple controls

**Run**:
```bash
openflex build examples/counter/App.mxml
```

### 3. Todo App (Coming Soon)
**Path**: `todo-app/`

Full CRUD application with:
- List rendering
- Form handling
- Local storage
- Component composition

## 🚀 Running Examples

```bash
# Build an example
openflex build examples/<name>/App.mxml -o dist/<name>

# Watch mode
openflex build examples/<name>/App.mxml --watch

# Type check only
openflex check examples/<name>/App.mxml
```

## 📝 Learning Path

1. **hello-world**: Start here - basic syntax
2. **counter**: Learn reactive programming
3. **todo-app**: Full application patterns

Each example includes comments explaining key concepts.
