# OpenFlex Neo for Visual Studio Code

Language support for ActionScript 4 and MXML in Visual Studio Code.

## Features

### Syntax Highlighting
- Full AS4 syntax highlighting
- MXML tag and attribute highlighting
- Reactive binding syntax (`{expression}`)
- Decorator syntax (`@reactive`, `@computed`, `@effect`)

### IntelliSense
- Code snippets for common patterns
- Auto-completion for AS4 and MXML

### Commands
- **OpenFlex: Compile File** (`Ctrl+Shift+B` / `Cmd+Shift+B`)
- **OpenFlex: Start Watch Mode**
- **OpenFlex: Stop Watch Mode**

## Snippets

### ActionScript 4

- `reactive` - Create reactive variable
- `computed` - Create computed variable
- `effect` - Create effect function
- `function` - Function declaration
- `class` - Class declaration
- `interface` - Interface declaration

### MXML

- `mxml:app` - MXML Application template
- `mxml:component` - MXML Component template
- `vbox` - VBox container
- `hbox` - HBox container
- `label` - Label component
- `button` - Button component

## Requirements

- Python 3.9 or higher
- OpenFlex Neo compiler (`npm install -g openflex-neo`)

## Extension Settings

- `openflex.compilerPath`: Path to OpenFlex compiler
- `openflex.watchMode`: Enable watch mode for auto-compilation
- `openflex.sourceMapEnabled`: Generate source maps for debugging

## Quick Start

1. Install the extension
2. Install OpenFlex compiler: `npm install -g openflex-neo`
3. Create a new `.as4` or `.mxml` file
4. Start typing and use snippets!

## Examples

### AS4 with Reactivity

```actionscript
@reactive var count: Number = 0;
@computed var doubled: Number = count * 2;

@effect
function logCount(): void {
    trace("Count: " + count);
}

function increment(): void {
    count = count + 1;
}
```

### MXML Application

```xml
<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var count: Number = 0;

        function increment(): void {
            count = count + 1;
        }
    </fx:Script>

    <VBox>
        <Label text="Count: {count}" />
        <Button label="Increment" click={increment} />
    </VBox>
</Application>
```

## License

MIT
