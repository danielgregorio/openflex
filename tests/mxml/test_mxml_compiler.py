"""
Tests for MXML Compiler
"""

import pytest
from compiler.enhanced_mxml_compiler import EnhancedMXMLCompiler


class TestMXMLCompiler:
    """Tests for MXML compilation"""

    @pytest.fixture
    def compiler(self):
        """Create MXML compiler instance"""
        return EnhancedMXMLCompiler()

    def test_basic_mxml_compilation(self, compiler):
        """Test basic MXML compilation"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        var message: String = "Hello";
    </fx:Script>
    <VBox>
        <Label text="Test" />
    </VBox>
</Application>"""

        js = compiler.compile(mxml, "test.mxml")

        assert "class AppComponent extends HTMLElement" in js
        assert "customElements.define('app-root', AppComponent)" in js

    def test_reactive_mxml_compilation(self, compiler):
        """Test MXML with reactive variables"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
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
</Application>"""

        js = compiler.compile(mxml, "test.mxml")

        # Check reactive imports
        assert "Signal, Computed, createEffect" in js

        # Check reactive variable
        assert "const count = new Signal(0)" in js

        # Check function
        assert "function increment()" in js
        assert "count.value = count.value + 1" in js

        # Check Web Component structure
        assert "class AppComponent extends HTMLElement" in js
        assert "attachShadow" in js

        # Check reactive binding setup
        assert "setupReactivity()" in js
        assert "createEffect" in js

        # Check event handler
        assert "onclick = () => increment()" in js

    def test_bindings_extracted(self, compiler):
        """Test that reactive bindings are extracted"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var name: String = "World";
    </fx:Script>
    <VBox>
        <Label text="Hello {name}" />
    </VBox>
</Application>"""

        js = compiler.compile(mxml, "test.mxml")

        # Check binding element created
        assert "binding_" in js

        # Check effect created
        assert "createEffect(() => {" in js
        assert "getElementById('binding_" in js
        assert "textContent = 'Hello ' + name.value" in js

    def test_event_handlers_extracted(self, compiler):
        """Test that event handlers are extracted"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        function handleClick(): void {
            trace("clicked");
        }
    </fx:Script>
    <VBox>
        <Button label="Click Me" click={handleClick} />
    </VBox>
</Application>"""

        js = compiler.compile(mxml, "test.mxml")

        # Check button created
        assert "btn_" in js

        # Check event handler attached
        assert "onclick = () => handleClick()" in js

    def test_multiple_bindings(self, compiler):
        """Test multiple reactive bindings"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var count: Number = 0;
        @reactive var total: Number = 0;
    </fx:Script>
    <VBox>
        <Label text="Count: {count}" />
        <Label text="Total: {total}" />
    </VBox>
</Application>"""

        js = compiler.compile(mxml, "test.mxml")

        # Check both bindings created
        assert "binding_0" in js
        assert "binding_1" in js

        # Check both effects created
        assert js.count("createEffect") >= 2

    def test_id_consistency(self, compiler):
        """Test that IDs are consistent between HTML and handlers"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var count: Number = 0;
        function increment(): void { count = count + 1; }
    </fx:Script>
    <VBox>
        <Label text="Count: {count}" />
        <Button label="+" click={increment} />
    </VBox>
</Application>"""

        js = compiler.compile(mxml, "test.mxml")

        # Extract button ID from HTML
        import re
        html_match = re.search(r"<button id='(btn_\d+)'>", js)
        assert html_match, "Button not found in HTML"
        button_id = html_match.group(1)

        # Check same ID used in event handler
        assert f"getElementById('{button_id}').onclick" in js

        # Extract binding ID from HTML
        binding_match = re.search(r"<span id='(binding_\d+)'>", js)
        assert binding_match, "Binding span not found in HTML"
        binding_id = binding_match.group(1)

        # Check same ID used in effect
        assert f"getElementById('{binding_id}')" in js
