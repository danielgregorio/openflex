# openflex.toml Specification

## Overview

`openflex.toml` is the Maven-like project configuration file for OpenFlex Neo projects. It defines dependencies, build targets, compiler settings, and more.

**Why TOML?**
- ✅ Human-readable (easier than XML/JSON)
- ✅ Comments supported
- ✅ Type-safe
- ✅ Standard format (used by Rust/Cargo, Python/Poetry)

---

## Minimal Configuration

```toml
[package]
name = "my-app"
version = "0.1.0"

[build]
entry = "src/app/App.mxml"
output = "dist"
```

---

## Complete Reference

### [package] Section

Project metadata

```toml
[package]
name = "my-awesome-app"        # Required: Package name
version = "1.0.0"               # Required: Semantic version
authors = [                     # Optional: Authors
    "Your Name <you@example.com>"
]
license = "MIT"                 # Optional: License
description = "A great app"    # Optional: Description
homepage = "https://example.com"  # Optional: Homepage URL
repository = "https://github.com/user/repo"  # Optional: Source repo
keywords = ["app", "neo"]       # Optional: Keywords for discovery
```

---

### [build] Section

Build configuration

```toml
[build]
entry = "src/app/App.mxml"     # Required: Entry point
output = "dist"                 # Optional: Output directory (default: dist)
source = "src"                  # Optional: Source root (default: src)
assets = "assets"               # Optional: Assets directory
```

---

### [[build.target]] Sections

Multiple build targets (web, mobile, desktop)

```toml
# Web target
[[build.target]]
name = "web"                    # Target name
platform = "web"                # Platform: web, mobile, desktop
output = "dist/web"             # Target-specific output
defines = ["WEB", "PRODUCTION"] # Conditional compilation flags
renderer = "dom"                # Renderer: dom, canvas, webgl

# Mobile iOS target
[[build.target]]
name = "mobile-ios"
platform = "mobile"
os = "ios"                      # OS: ios, android
output = "dist/ios"
defines = ["MOBILE", "IOS", "PRODUCTION"]

# Desktop macOS target
[[build.target]]
name = "desktop-mac"
platform = "desktop"
os = "macos"                    # OS: macos, windows, linux
output = "dist/desktop"
defines = ["DESKTOP", "MACOS", "PRODUCTION"]
```

---

### [dependencies] Section

Package dependencies

```toml
[dependencies]
openflex-core = "^1.0.0"        # Semver range
openflex-charts = "2.1.0"       # Exact version
openflex-forms = "~3.0.0"       # Compatible version

# Git dependencies
custom-components = { git = "https://github.com/user/repo", branch = "main" }

# Path dependencies (local development)
shared-lib = { path = "../shared" }
```

#### Version Syntax

```toml
"1.2.3"      # Exact version
"^1.2.3"     # Compatible (>=1.2.3, <2.0.0)
"~1.2.3"     # Patch (>=1.2.3, <1.3.0)
">=1.2.3"    # Greater than or equal
"<2.0.0"     # Less than
"*"          # Any version (not recommended)
```

---

### [dev-dependencies] Section

Development-only dependencies (tests, tooling)

```toml
[dev-dependencies]
openflex-test = "^1.0.0"
openflex-mock = "^0.5.0"
```

---

### [compiler] Section

Compiler options

```toml
[compiler]
strict-null-checks = true       # Enable null safety (default: false)
strict-mode = false              # Strict type checking (default: false)
optimization-level = 2           # 0 = none, 1 = basic, 2 = aggressive
source-maps = true               # Generate source maps (default: true)
target = "es2022"                # JavaScript target (es2022, es2020, es2015)
module-system = "esm"            # esm, cjs, umd
tree-shaking = true              # Dead code elimination (default: true)
minify = false                   # Minify output (default: false in dev)
```

---

### [runtime] Section

Runtime configuration

```toml
[runtime]
renderer = "dom"                 # dom, canvas, webgl (default: dom)
reactive-mode = "fine-grained"   # fine-grained, coarse-grained
enable-hmr = true                # Hot module reload (default: true in dev)
```

---

### [dev] Section

Development server configuration

```toml
[dev]
port = 3000                      # Dev server port (default: 3000)
host = "localhost"               # Host (default: localhost)
open = true                      # Open browser (default: false)
hmr = true                       # Hot module reload (default: true)
https = false                    # Use HTTPS (default: false)
```

---

### [test] Section

Testing configuration

```toml
[test]
framework = "vitest"             # Test framework
coverage = true                  # Generate coverage (default: false)
watch = false                    # Watch mode (default: false)
```

---

### [style] Section

Styling configuration

```toml
[style]
preprocessor = "css"             # css, scss, less (default: css)
scope = "component"              # component, global (default: component)
postcss = true                   # Enable PostCSS (default: false)
```

---

## Complete Example

```toml
# OpenFlex Neo Project Configuration

[package]
name = "my-awesome-app"
version = "1.0.0"
authors = ["Alice Developer <alice@example.com>"]
license = "MIT"
description = "A cross-platform app built with OpenFlex Neo"
homepage = "https://myawesomeapp.com"
repository = "https://github.com/alice/my-awesome-app"
keywords = ["app", "neo", "cross-platform"]

[build]
entry = "src/app/App.mxml"
output = "dist"
source = "src"
assets = "assets"

# Web target
[[build.target]]
name = "web"
platform = "web"
output = "dist/web"
defines = ["WEB", "PRODUCTION"]
renderer = "dom"

# Mobile iOS target
[[build.target]]
name = "mobile-ios"
platform = "mobile"
os = "ios"
output = "dist/ios"
defines = ["MOBILE", "IOS", "PRODUCTION"]

# Mobile Android target
[[build.target]]
name = "mobile-android"
platform = "mobile"
os = "android"
output = "dist/android"
defines = ["MOBILE", "ANDROID", "PRODUCTION"]

# Desktop macOS target
[[build.target]]
name = "desktop-mac"
platform = "desktop"
os = "macos"
output = "dist/desktop-mac"
defines = ["DESKTOP", "MACOS", "PRODUCTION"]

# Desktop Windows target
[[build.target]]
name = "desktop-windows"
platform = "desktop"
os = "windows"
output = "dist/desktop-windows"
defines = ["DESKTOP", "WINDOWS", "PRODUCTION"]

[dependencies]
openflex-core = "^1.0.0"
openflex-charts = "^2.1.0"
openflex-forms = "^1.5.0"

[dev-dependencies]
openflex-test = "^1.0.0"

[compiler]
strict-null-checks = true
optimization-level = 2
source-maps = true
target = "es2022"
module-system = "esm"
tree-shaking = true

[runtime]
renderer = "dom"
reactive-mode = "fine-grained"
enable-hmr = true

[dev]
port = 3000
host = "localhost"
open = true
hmr = true

[test]
framework = "vitest"
coverage = true

[style]
preprocessor = "css"
scope = "component"
```

---

## CLI Integration

### Building Targets

```bash
# Build specific target
openflex build --target web
openflex build --target mobile-ios
openflex build --target desktop-mac

# Build all targets
openflex build --all

# Build with custom config
openflex build --config openflex.production.toml
```

### Development

```bash
# Start dev server (uses [dev] config)
openflex dev

# Custom port
openflex dev --port 8080

# Specific target
openflex dev --target web
```

### Testing

```bash
# Run tests (uses [test] config)
openflex test

# With coverage
openflex test --coverage

# Watch mode
openflex test --watch
```

---

## Environment-Specific Configs

### Multiple Config Files

```
my-app/
├── openflex.toml              # Default (dev)
├── openflex.production.toml   # Production
├── openflex.staging.toml      # Staging
└── openflex.test.toml         # Testing
```

### Using Different Configs

```bash
# Development (default)
openflex build

# Production
openflex build --config openflex.production.toml

# Staging
openflex build --config openflex.staging.toml
```

### Production Example

```toml
# openflex.production.toml
[package]
name = "my-app"
version = "1.0.0"

[build]
entry = "src/app/App.mxml"
output = "dist-prod"

[[build.target]]
name = "web"
platform = "web"
defines = ["WEB", "PRODUCTION", "ANALYTICS_ENABLED"]

[compiler]
optimization-level = 2
source-maps = false              # No source maps in prod
minify = true                    # Minify in prod
tree-shaking = true

[runtime]
enable-hmr = false               # No HMR in prod
```

---

## Validation

### Schema Validation

```bash
# Validate config file
openflex validate

# Validate specific file
openflex validate openflex.production.toml
```

### Common Errors

```toml
# ✗ Error: Missing required fields
[package]
# Missing 'name' and 'version'

# ✗ Error: Invalid version format
[package]
version = "1.0"  # Must be semver (1.0.0)

# ✗ Error: Unknown platform
[[build.target]]
platform = "ios"  # Should be "mobile" with os = "ios"

# ✗ Error: Invalid optimization level
[compiler]
optimization-level = 5  # Must be 0, 1, or 2
```

---

## Migration from package.json

### Before (NPM style)

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "build": "webpack build",
    "dev": "webpack serve"
  },
  "dependencies": {
    "react": "^18.0.0"
  }
}
```

### After (OpenFlex Neo)

```toml
[package]
name = "my-app"
version = "1.0.0"

[build]
entry = "src/app/App.mxml"

[dependencies]
openflex-core = "^1.0.0"

[dev]
port = 3000
```

**Benefits**:
- ✅ No build scripts needed
- ✅ Convention over configuration
- ✅ Type-safe config
- ✅ Multi-target support built-in

---

## Best Practices

### 1. Version Dependencies Properly

```toml
# ✓ Good - use caret for compatible versions
openflex-charts = "^2.1.0"

# ⚠️ Careful - exact version harder to update
openflex-charts = "2.1.0"

# ✗ Bad - wildcard unpredictable
openflex-charts = "*"
```

### 2. Separate Dev from Prod

```toml
# Development
[compiler]
optimization-level = 0
source-maps = true
minify = false

# Production (separate file)
[compiler]
optimization-level = 2
source-maps = false
minify = true
```

### 3. Use Defines for Features

```toml
[[build.target]]
name = "web-beta"
defines = ["WEB", "FEATURE_BETA", "ANALYTICS_ENABLED"]

[[build.target]]
name = "web-stable"
defines = ["WEB", "PRODUCTION"]
# No FEATURE_BETA
```

### 4. Document Custom Targets

```toml
# Production web build with analytics
[[build.target]]
name = "web-prod"
platform = "web"
defines = ["WEB", "PRODUCTION", "ANALYTICS"]

# Development web build with debug tools
[[build.target]]
name = "web-dev"
platform = "web"
defines = ["WEB", "DEBUG", "VERBOSE_LOGGING"]
```

---

## Summary

**openflex.toml provides**:
- ✅ Centralized configuration
- ✅ Multi-target builds
- ✅ Dependency management
- ✅ Compiler options
- ✅ Development server config
- ✅ Maven-like familiarity

**Key Sections**:
- `[package]` - Project metadata
- `[build]` - Build configuration
- `[[build.target]]` - Platform targets
- `[dependencies]` - Package dependencies
- `[compiler]` - Compiler options
- `[runtime]` - Runtime configuration
- `[dev]` - Dev server config

**Result**: Clean, type-safe, multi-platform configuration! 🆕
