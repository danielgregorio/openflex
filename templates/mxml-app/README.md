# OpenFlex Neo - MXML App Template

A complete MXML application with Web Components and reactivity.

## Features

- ✅ MXML declarative UI
- ✅ Reactive data bindings
- ✅ Web Components output
- ✅ Event handling
- ✅ Hot reload ready

## Quick Start

```bash
# Install dependencies
npm install

# Compile MXML to Web Components
npm run build

# Or use watch mode for development
npm run dev

# Open in browser
open index.html
```

## Project Structure

```
mxml-app/
├── src/
│   ├── App.mxml          # Main application
│   └── components/       # Reusable components
├── public/
│   └── index.html        # HTML entry point
├── package.json          # Project configuration
└── README.md            # This file
```

## Customization

Edit `src/App.mxml` to build your application:

```xml
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var myData: String = "Hello";
    </fx:Script>

    <VBox>
        <Label text="{myData}" />
    </VBox>
</Application>
```

## Learn More

- [MXML Guide](https://openflex.dev/docs/mxml)
- [Reactive Bindings](https://openflex.dev/docs/bindings)
- [Web Components](https://openflex.dev/docs/web-components)
