# AS4 Import System Specification

## Philosophy

ActionScript 4 uses a **clean, explicit import system** inspired by AS3 and Java. No JavaScript-style destructuring, no confusing syntax.

**Design Goals**:
1. **Explicit** - Clear what you're importing
2. **Simple** - No `{ }` destructuring or complex patterns
3. **Familiar** - AS3 developers feel at home
4. **Type-safe** - Compiler validates imports
5. **IDE-friendly** - Easy autocomplete

---

## Import Syntax

### Basic Import (Single Class)

```actionscript
import openflex.reactive.Signal;
import openflex.components.Button;
import openflex.http.Request;

// Usage - imported names are available directly
const count = new Signal(0);
const btn = new Button();
```

### Wildcard Import (Entire Package)

```actionscript
import openflex.reactive.*;
import openflex.components.*;

// Usage - all exports from package are available
const count = new Signal(0);
const computed = new Computed(() => count.value * 2);
const btn = new Button();
```

### Aliasing (Rename on Import)

```actionscript
import openflex.reactive.Signal as ReactiveSignal;
import openflex.charts.LineChart as Chart;

// Usage - with alias
const count = new ReactiveSignal(0);
const chart = new Chart();
```

### Multiple Imports (Same Package)

```actionscript
// Separate imports (verbose but clear)
import openflex.reactive.Signal;
import openflex.reactive.Computed;
import openflex.reactive.Effect;

// OR wildcard (recommended for 3+ imports)
import openflex.reactive.*;
```

### Full Qualification (No Import)

```actionscript
// No import needed - use full path
const count = new openflex.reactive.Signal(0);
const btn = new openflex.components.Button();

// Useful for one-off usage or avoiding conflicts
```

---

## Package Structure

### Standard Library Organization

```
openflex/
├── core/              # Core types
│   ├── Object
│   ├── Array
│   └── Map
├── reactive/          # Reactive primitives
│   ├── Signal
│   ├── Computed
│   └── Effect
├── components/        # UI components
│   ├── Button
│   ├── Label
│   └── VBox
├── http/              # HTTP client
│   ├── Request
│   ├── Response
│   └── Client
├── async/             # Async utilities
│   ├── Promise
│   └── AsyncIterator
└── collections/       # Data structures
    ├── List
    ├── Set
    └── HashMap
```

### Import Examples

```actionscript
// Reactive
import openflex.reactive.Signal;
import openflex.reactive.*;

// Components
import openflex.components.Button;
import openflex.components.*;

// HTTP
import openflex.http.Request;
import openflex.http.*;

// Collections
import openflex.collections.List;
import openflex.collections.*;
```

---

## Package Namespaces

### Explicit Namespace Imports

```actionscript
// Import entire namespace
import openflex.reactive;
import openflex.components;

// Usage with namespace prefix
const count = new reactive.Signal(0);
const btn = new components.Button();
```

### Namespace Aliasing

```actionscript
// Alias namespace
import openflex.reactive as rx;
import openflex.components as ui;

// Usage
const count = new rx.Signal(0);
const btn = new ui.Button();
```

---

## Import Resolution

### Resolution Order

1. **Built-in packages** (`openflex.*`)
2. **Installed packages** (from `openflex.toml`)
3. **Project files** (relative to source root)
4. **Error** if not found

### Project Files

```actionscript
// Project structure:
// src/
//   app/App.mxml
//   components/CustomButton.mxml
//   lib/utils.as4

// Import from project
import components.CustomButton;
import lib.utils.formatDate;

// Relative imports NOT supported - always from source root
```

### Third-Party Packages

```toml
# openflex.toml
[dependencies]
openflex-charts = "^1.0.0"
```

```actionscript
// Package defines namespace: "charts"
import charts.LineChart;
import charts.BarChart;
import charts.*;
```

---

## Import Rules

### 1. Case Sensitivity

```actionscript
import openflex.reactive.Signal;  // ✓ Correct
import openflex.Reactive.Signal;  // ✗ Error - case mismatch
import Openflex.reactive.Signal;  // ✗ Error - case mismatch
```

### 2. No Circular Imports

```actionscript
// File A.as4
import B;  // ✗ Error if B imports A

class A { }

// File B.as4
import A;  // Circular dependency!

class B { }
```

**Solution**: Extract shared code to third file

### 3. Import Before Usage

```actionscript
const s = new Signal(0);  // ✗ Error - Signal not imported

import openflex.reactive.Signal;  // ✗ Error - import must be at top

// ✓ Correct order:
import openflex.reactive.Signal;

const s = new Signal(0);
```

### 4. No Duplicate Imports

```actionscript
import openflex.reactive.Signal;
import openflex.reactive.Signal;  // ⚠️ Warning - duplicate

// Compiler removes duplicates
```

### 5. Wildcard Conflicts

```actionscript
import openflex.components.*;  // Contains Button
import thirdparty.controls.*;  // Also contains Button

const btn = new Button();  // ✗ Error - ambiguous!

// Solution 1: Specific import
import openflex.components.Button;
import thirdparty.controls.*;

// Solution 2: Aliasing
import openflex.components.Button;
import thirdparty.controls.Button as ThirdPartyButton;
```

---

## Type Imports

### Import Types Only

```actionscript
// Import for type annotation (interface, type alias)
import openflex.types.User;

// Usage as type
function greet(user: User): void {
    trace("Hello " + user.name);
}

// No runtime import - just for type checking
```

### Import Both Type and Value

```actionscript
// Import class (both type and constructor)
import openflex.components.Button;

// Usage as type
var btn: Button;

// Usage as value (constructor)
btn = new Button();
```

---

## Conditional Imports

### Platform-Specific Imports

```actionscript
#if WEB
import openflex.web.Canvas;
import openflex.web.WebGL;
#endif

#if MOBILE
import openflex.mobile.Camera;
import openflex.mobile.GPS;
#endif

#if DESKTOP
import openflex.desktop.FileDialog;
import openflex.desktop.MenuBar;
#endif
```

**Result**: Only imports for target platform are included in build

---

## Package Manager Integration

### Installing Packages

```bash
# Install from registry
opm install openflex-charts

# Install specific version
opm install openflex-charts@1.2.0

# Install from git
opm install github:user/package
```

### Package Configuration

```toml
# package.openflex.toml
[package]
name = "openflex-charts"
version = "1.0.0"
namespace = "charts"  # Import as: import charts.LineChart

[dependencies]
openflex-core = "^1.0.0"

[exports]
# Explicitly list what's importable
LineChart = "src/LineChart.mxml"
BarChart = "src/BarChart.mxml"
PieChart = "src/PieChart.mxml"
```

### Using Installed Packages

```actionscript
// Package namespace from package.openflex.toml
import charts.LineChart;
import charts.*;

const chart = new LineChart();
```

---

## IDE Support

### Autocomplete

Type `import ` → IDE suggests:
- openflex.*
- Installed packages
- Project files

Type `import openflex.` → IDE suggests:
- reactive
- components
- http
- etc.

### Organize Imports

```actionscript
// Before (messy)
import openflex.components.Button;
import lib.utils.formatDate;
import openflex.reactive.Signal;
import charts.LineChart;

// After (organized by IDE)
// Standard library
import openflex.components.Button;
import openflex.reactive.Signal;

// Third-party
import charts.LineChart;

// Project
import lib.utils.formatDate;
```

### Auto-Import

```actionscript
const count = new Signal(0);  // Signal underlined

// IDE quick-fix: "Import openflex.reactive.Signal"
// Result:
import openflex.reactive.Signal;

const count = new Signal(0);
```

---

## Migration from AS3

### AS3 → AS4 Import Changes

```actionscript
// AS3
import mx.controls.Button;
import mx.containers.*;
import flash.events.Event;

// AS4 (Neo)
import openflex.components.Button;
import openflex.components.*;
import openflex.events.Event;
```

**Changes**:
- `mx.*` → `openflex.components.*`
- `flash.*` → `openflex.*`
- `spark.*` → `openflex.components.*` (Neo namespace)

---

## Best Practices

### 1. Prefer Specific Imports

```actionscript
// ✓ Good - explicit
import openflex.reactive.Signal;
import openflex.reactive.Computed;

// ⚠️ Less ideal - less clear what you're using
import openflex.reactive.*;
```

**Exception**: When using 4+ exports from same package, wildcard is cleaner

### 2. Group Imports

```actionscript
// ✓ Good - grouped by source
// Standard library
import openflex.reactive.Signal;
import openflex.components.Button;

// Third-party
import charts.LineChart;
import forms.TextField;

// Project
import lib.utils;
import components.CustomButton;
```

### 3. Avoid Deep Nesting

```actionscript
// ✗ Bad - too deep
import openflex.ui.controls.buttons.primary.LargeButton;

// ✓ Better - flatter structure
import openflex.components.Button;
// Use props: <Button variant="primary" size="large" />
```

### 4. Use Aliases for Conflicts

```actionscript
// When two packages export same name
import openflex.components.Button;
import material.Button as MaterialButton;

const btn1 = new Button();
const btn2 = new MaterialButton();
```

### 5. Import Order

```actionscript
// Recommended order:
// 1. Standard library
import openflex.reactive.*;
import openflex.components.*;

// 2. Third-party packages
import charts.*;
import forms.*;

// 3. Project files
import lib.utils;
import components.CustomButton;
```

---

## Comparison with Other Languages

### AS4 vs JavaScript

```javascript
// JavaScript (messy!)
import { signal, computed, effect } from "openflex/reactive";
import Button from "openflex/components/Button";
import * as React from "react";

// AS4 (clean!)
import openflex.reactive.Signal;
import openflex.reactive.Computed;
import openflex.reactive.Effect;
import openflex.components.Button;
```

### AS4 vs TypeScript

```typescript
// TypeScript
import { Signal } from "openflex/reactive";
import type { User } from "types";

// AS4
import openflex.reactive.Signal;
import openflex.types.User;
// (Types and values use same import - simpler!)
```

### AS4 vs Java

```java
// Java (AS4 is inspired by this)
import java.util.List;
import java.util.*;

// AS4 (very similar!)
import openflex.collections.List;
import openflex.collections.*;
```

---

## Summary

**AS4 Import Philosophy**:
- ✅ Explicit over implicit
- ✅ Simple over complex
- ✅ Familiar to AS3/Java developers
- ✅ No JavaScript baggage
- ✅ Type-safe
- ✅ IDE-friendly

**Key Syntax**:
```actionscript
import package.Class;           // Single class
import package.*;               // Wildcard
import package.Class as Alias;  // Aliasing
import package;                 // Namespace import
```

**Result**: Clean, readable, maintainable code! 🆕
