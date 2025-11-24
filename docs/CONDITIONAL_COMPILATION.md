# Conditional Compilation Specification

## Philosophy

**Zero Bloat Multi-Platform**

When compiling for web, your bundle should contain **ZERO mobile code**. When compiling for mobile, **ZERO web-specific code**. Conditional compilation achieves this at compile-time.

**Design Goals**:
1. **Zero Runtime Overhead** - Code eliminated at compile-time
2. **Type-Safe** - Conditional blocks are type-checked
3. **Clear Intent** - Easy to see what's platform-specific
4. **IDE Support** - Grayed out inactive code
5. **Maintainable** - One codebase, multiple targets

---

## Basic Syntax

### #if / #endif

```actionscript
#if WEB
// This code only exists in web builds
import openflex.web.Canvas;

function useWebGL(): void {
    // Web-only implementation
}
#endif

#if MOBILE
// This code only exists in mobile builds
import openflex.mobile.Camera;

function useCamera(): void {
    // Mobile-only implementation
}
#endif
```

**Result**: Web build has NO mobile code, mobile build has NO web code.

### #if / #else / #endif

```actionscript
#if WEB
function getPlatformName(): String {
    return "Web Browser";
}
#else
function getPlatformName(): String {
    return "Other Platform";
}
#endif
```

### #if / #elif / #else / #endif

```actionscript
#if WEB
const STORAGE_KEY = "web_local_storage";
#elif MOBILE
const STORAGE_KEY = "mobile_async_storage";
#elif DESKTOP
const STORAGE_KEY = "desktop_file_storage";
#else
const STORAGE_KEY = "memory_storage";
#endif
```

---

## Built-in Flags

### Platform Flags (Mutually Exclusive)

```actionscript
#if WEB
// Web platform (browser)
#endif

#if MOBILE
// Mobile platform (iOS/Android)
#endif

#if DESKTOP
// Desktop platform (Windows/Mac/Linux)
#endif

#if TERMINAL
// Terminal/CLI platform
#endif
```

**Guaranteed**: Only ONE platform flag is true per build

### Build Mode Flags

```actionscript
#if DEBUG
// Debug mode - development
#endif

#if RELEASE
// Release mode - production
#endif

#if TEST
// Test mode - running tests
#endif
```

### OS Flags (Sub-platform)

```actionscript
#if IOS
// iOS devices
#endif

#if ANDROID
// Android devices
#endif

#if WINDOWS
// Windows desktop
#endif

#if MACOS
// macOS desktop
#endif

#if LINUX
// Linux desktop
#endif
```

### Renderer Flags

```actionscript
#if DOM_RENDERER
// Using DOM renderer
#endif

#if CANVAS_RENDERER
// Using Canvas 2D renderer
#endif

#if WEBGL_RENDERER
// Using WebGL renderer
#endif
```

---

## Compilation Flow

### Build Command

```bash
# Web build (sets WEB flag)
openflex build --target web

# Mobile build (sets MOBILE + IOS flags)
openflex build --target ios

# Desktop build (sets DESKTOP + MACOS flags)
openflex build --target desktop --os macos

# Debug vs Release
openflex build --target web --mode debug   # Sets DEBUG
openflex build --target web --mode release # Sets RELEASE
```

### Flag Configuration

```toml
# openflex.toml
[[build.target]]
name = "web"
platform = "web"
defines = ["WEB", "DOM_RENDERER", "PRODUCTION"]

[[build.target]]
name = "mobile-ios"
platform = "mobile"
defines = ["MOBILE", "IOS", "PRODUCTION"]

[[build.target]]
name = "desktop-mac"
platform = "desktop"
defines = ["DESKTOP", "MACOS", "PRODUCTION"]
```

---

## Advanced Usage

### Nested Conditions

```actionscript
#if MOBILE
    #if IOS
        import openflex.mobile.ios.Specific;
    #elif ANDROID
        import openflex.mobile.android.Specific;
    #endif

    function mobileFeature(): void {
        #if IOS
            // iOS-specific
        #else
            // Android-specific
        #endif
    }
#endif
```

### Boolean Logic

```actionscript
// AND
#if (WEB && DEBUG)
trace("Web debug build");
#endif

// OR
#if (IOS || ANDROID)
trace("Mobile platform");
#endif

// NOT
#if !PRODUCTION
trace("Not production");
#endif

// Complex
#if ((WEB || DESKTOP) && !DEBUG)
// Web or Desktop, in release mode
#endif
```

### Inline Expressions

```actionscript
// Conditional value
const API_URL = #if DEBUG
    "http://localhost:3000"
#else
    "https://api.production.com"
#endif;

// Conditional call
const result = fetchData(
    #if DEBUG
        { verbose: true, timeout: 0 }
    #else
        { verbose: false, timeout: 5000 }
    #endif
);

// Conditional parameter
function log(message: String, level: #if DEBUG "debug" #else "info" #endif): void {
    // ...
}
```

---

## In MXML

### Conditional Components

```xml
<Application
    xmlns:fx="http://openflex.dev/core"
    xmlns="http://openflex.dev/neo">

    <fx:Script>
        #if WEB
        function useWebFeature(): void {
            // Web-only code
        }
        #endif

        #if MOBILE
        function useMobileFeature(): void {
            // Mobile-only code
        }
        #endif
    </fx:Script>

    <VBox>
        <!-- Web-only components -->
        #if WEB
        <WebCanvas />
        <WebGLView />
        #endif

        <!-- Mobile-only components -->
        #if MOBILE
        <CameraView />
        <GPSView />
        #endif

        <!-- Universal components -->
        <Button label="Click" />
    </VBox>

</Application>
```

### Conditional Imports in MXML

```xml
<Application>
    <fx:Script>
        #if WEB
        import openflex.web.*;
        #endif

        #if MOBILE
        import openflex.mobile.*;
        #endif

        // This code adapts to platform
        function takePicture(): void {
            #if MOBILE
            return Camera.capture();
            #else
            return null;  // Not supported
            #endif
        }
    </fx:Script>
</Application>
```

---

## Custom Flags

### Defining Custom Flags

```bash
# Command line
openflex build --define FEATURE_BETA --define ANALYTICS_ENABLED

# openflex.toml
[[build.target]]
name = "web-beta"
platform = "web"
defines = ["WEB", "FEATURE_BETA", "ANALYTICS_ENABLED"]
```

### Using Custom Flags

```actionscript
#if FEATURE_BETA
function betaOnlyFeature(): void {
    // Only in beta builds
}
#endif

#if ANALYTICS_ENABLED
import analytics.Tracker;

const tracker = new Tracker();
#endif

#if PREMIUM_VERSION
const MAX_UPLOADS = 1000;
#else
const MAX_UPLOADS = 10;
#endif
```

---

## Type Safety

### Type-Checked Conditional Blocks

```actionscript
#if WEB
import openflex.web.Canvas;

function draw(canvas: Canvas): void {
    // Canvas type is valid here
}
#endif

// Usage
#if WEB
const canvas = new Canvas();
draw(canvas);  // ✓ Type-safe
#endif
```

### Avoiding Type Errors

```actionscript
// ✗ Bad - causes error in mobile build
function render(): void {
    const canvas = new Canvas();  // Error: Canvas not defined in MOBILE
}

// ✓ Good - conditional entire function
#if WEB
function render(): void {
    const canvas = new Canvas();  // OK - only in WEB build
}
#endif

// ✓ Also good - conditional inside function
function render(): void {
    #if WEB
    const canvas = new Canvas();
    canvas.draw();
    #endif
}
```

---

## Dead Code Elimination

### How It Works

```actionscript
// Source code
#if WEB
function webOnly(): void {
    trace("Web");
}
#endif

#if MOBILE
function mobileOnly(): void {
    trace("Mobile");
}
#endif

function universal(): void {
    trace("Universal");
}
```

**Web build output**:
```javascript
function webOnly() {
    console.log("Web");
}

function universal() {
    console.log("Universal");
}
// mobileOnly() doesn't exist!
```

**Mobile build output**:
```javascript
function mobileOnly() {
    console.log("Mobile");
}

function universal() {
    console.log("Universal");
}
// webOnly() doesn't exist!
```

### Bundle Size Impact

```actionscript
// Large platform-specific libraries
#if WEB
import openflex.web.*;      // 100KB
#endif

#if MOBILE
import openflex.mobile.*;   // 80KB
#endif

#if DESKTOP
import openflex.desktop.*;  // 90KB
#endif
```

**Result**:
- Web build: Only 100KB (no mobile/desktop)
- Mobile build: Only 80KB (no web/desktop)
- Desktop build: Only 90KB (no web/mobile)

**Without conditional compilation**: All builds = 270KB (bloat!)

---

## IDE Support

### Grayed Out Code

```actionscript
// When editing with "WEB" configuration active:
#if WEB
function activeCode(): void {
    // Normal syntax highlighting
}
#endif

#if MOBILE
function inactiveCode(): void {
    // Grayed out / dimmed
}
#endif
```

### Configuration Switching

```bash
# IDE settings
Current Configuration: WEB
Available:
  - WEB (active)
  - MOBILE
  - DESKTOP

# Switch to MOBILE → mobile code becomes active, web code grays out
```

### Warnings

```actionscript
#if WEB
const canvas = new Canvas();
#endif

#if MOBILE
canvas.draw();  // ⚠️ Warning: canvas undefined in MOBILE
#endif
```

---

## Best Practices

### 1. Minimize Platform-Specific Code

```actionscript
// ✗ Bad - too much duplication
#if WEB
function fetchData(): Result<Data, Error> {
    const response = await http.get("/data");
    if (response.ok) {
        return Success(response.data);
    }
    return Error("Failed");
}
#endif

#if MOBILE
function fetchData(): Result<Data, Error> {
    const response = await http.get("/data");
    if (response.ok) {
        return Success(response.data);
    }
    return Error("Failed");
}
#endif

// ✓ Good - shared logic, platform-specific only when needed
function fetchData(): Result<Data, Error> {
    #if WEB
    const response = await webHttp.get("/data");
    #elif MOBILE
    const response = await mobileHttp.get("/data");
    #endif

    if (response.ok) {
        return Success(response.data);
    }
    return Error("Failed");
}
```

### 2. Use Abstraction for Platform Differences

```actionscript
// Platform abstraction layer
#if WEB
class StorageImpl {
    save(key: String, value: String): void {
        localStorage.setItem(key, value);
    }
}
#endif

#if MOBILE
class StorageImpl {
    async save(key: String, value: String): Promise<void> {
        await AsyncStorage.setItem(key, value);
    }
}
#endif

// Universal code - uses abstraction
const storage = new StorageImpl();
```

### 3. Document Platform Requirements

```actionscript
/**
 * Takes a photo using device camera
 *
 * @platform MOBILE - Requires camera access
 * @returns Photo data or null
 */
function takePhoto(): Photo? {
    #if MOBILE
    return Camera.capture();
    #else
    return null;
    #endif
}
```

### 4. Test All Platforms

```bash
# CI/CD pipeline
openflex build --target web && openflex test --target web
openflex build --target mobile && openflex test --target mobile
openflex build --target desktop && openflex test --target desktop

# Ensure all builds succeed
```

### 5. Avoid Deep Nesting

```actionscript
// ✗ Bad - hard to follow
#if WEB
    #if DEBUG
        #if FEATURE_BETA
            // Triple nested
        #endif
    #endif
#endif

// ✓ Better - combined conditions
#if (WEB && DEBUG && FEATURE_BETA)
    // Much clearer
#endif
```

---

## Comparison with Runtime Checks

### Runtime Check (BAD!)

```actionscript
// ✗ Anti-pattern - all code in bundle!
if (platform === "web") {
    useWebFeature();  // Mobile build still contains this!
}

if (platform === "mobile") {
    useMobileFeature();  // Web build still contains this!
}

// Result: Bloated bundle with ALL platform code
```

### Conditional Compilation (GOOD!)

```actionscript
// ✓ Compile-time elimination
#if WEB
useWebFeature();  // Only in web build
#endif

#if MOBILE
useMobileFeature();  // Only in mobile build
#endif

// Result: Each build only contains relevant code!
```

---

## Common Patterns

### Feature Flags

```actionscript
#if ANALYTICS_ENABLED
import analytics.Tracker;

const tracker = new Tracker();

@effect
function trackPageView() {
    tracker.pageView(currentRoute);
}
#endif

// Zero overhead when ANALYTICS_ENABLED not defined!
```

### Debug Logging

```actionscript
#if DEBUG
function debugLog(message: String): void {
    trace("[DEBUG] " + message);
}
#else
// No-op in production - eliminated by compiler
function debugLog(message: String): void { }
#endif
```

### A/B Testing

```actionscript
#if VARIANT_A
const buttonColor = "#FF0000";
#elif VARIANT_B
const buttonColor = "#00FF00";
#else
const buttonColor = "#0000FF";
#endif
```

---

## Migration from Runtime Checks

### Before (Runtime)

```javascript
// Old code - runtime checks
if (process.env.NODE_ENV === 'development') {
    console.log("Debug info");
}

if (platform.name === 'web') {
    useWebAPI();
}
```

### After (Compile-time)

```actionscript
// AS4 - compile-time elimination
#if DEBUG
trace("Debug info");
#endif

#if WEB
useWebAPI();
#endif
```

---

## Summary

**Conditional Compilation Benefits**:
- ✅ Zero runtime overhead
- ✅ Smaller bundle sizes
- ✅ Type-safe
- ✅ One codebase, multiple platforms
- ✅ Clear platform-specific code
- ✅ Maintainable

**Key Syntax**:
```actionscript
#if FLAG          // If defined
#if !FLAG         // If not defined
#if (A && B)      // Boolean AND
#if (A || B)      // Boolean OR
#elif FLAG        // Else if
#else             // Else
#endif            // End block
```

**Result**: Truly cross-platform with zero bloat! 🆕
