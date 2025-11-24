"""
Tests for MXML Neo parser
"""

import pytest
from compiler.parser.mxml_parser import MXMLParser, MXMLApplication, MXMLComponent
from compiler.parser.ast import Program


@pytest.fixture
def parser():
    """Create MXML parser instance"""
    return MXMLParser()


def test_simple_application(parser):
    """Test parsing simple MXML application"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo"
        title="Test App">
        <Label text="Hello" />
    </Application>
    """

    app = parser.parse(source)

    assert isinstance(app, MXMLApplication)
    assert app.root_component.tag == "Application"
    assert app.root_component.is_root
    assert len(app.root_component.children) == 1
    assert app.metadata.get('title') == "Test App"


def test_script_extraction(parser):
    """Test extracting AS4 script blocks"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Script>
            var count: Number = 0;

            function increment(): void {
                count++;
            }
        </fx:Script>

        <Label text="Counter" />
    </Application>
    """

    app = parser.parse(source)

    assert app.script_ast is not None
    assert isinstance(app.script_ast, Program)
    assert len(app.script_ast.declarations) == 2  # var + function


def test_style_extraction(parser):
    """Test extracting CSS style blocks"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Style>
            .button {
                background-color: #007bff;
            }
        </fx:Style>

        <Button />
    </Application>
    """

    app = parser.parse(source)

    assert app.styles
    assert "button" in app.styles
    assert "background-color" in app.styles


def test_data_binding(parser):
    """Test data binding detection"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Script>
            @reactive var message: String = "Hello";
        </fx:Script>

        <Label text="{message}" />
    </Application>
    """

    app = parser.parse(source)

    label = app.root_component.children[0]
    assert label.tag == "Label"
    assert 'text' in label.properties
    assert isinstance(label.properties['text'], dict)
    assert label.properties['text']['binding'] == 'message'


def test_nested_components(parser):
    """Test parsing nested component tree"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <VBox>
            <HBox>
                <Button label="A" />
                <Button label="B" />
            </HBox>
            <Label text="Bottom" />
        </VBox>
    </Application>
    """

    app = parser.parse(source)

    vbox = app.root_component.children[0]
    assert vbox.tag == "VBox"
    assert len(vbox.children) == 2

    hbox = vbox.children[0]
    assert hbox.tag == "HBox"
    assert len(hbox.children) == 2
    assert hbox.children[0].tag == "Button"
    assert hbox.children[1].tag == "Button"


def test_property_types(parser):
    """Test parsing different property types"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <Button
            label="Click"
            width="{100}"
            height="50"
            enabled="{true}"
            visible="false" />
    </Application>
    """

    app = parser.parse(source)

    button = app.root_component.children[0]
    props = button.properties

    # String
    assert props['label'] == "Click"

    # Binding (treated as binding due to braces)
    assert isinstance(props['width'], dict)
    assert props['width']['binding'] == '100'

    # Number (parsed as int)
    assert props['height'] == 50
    assert isinstance(props['height'], int)

    # Binding
    assert isinstance(props['enabled'], dict)
    assert props['enabled']['binding'] == 'true'

    # Boolean
    assert props['visible'] is False


def test_multiple_scripts(parser):
    """Test multiple script blocks"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Script>
            var x: Number = 1;
        </fx:Script>

        <fx:Script>
            var y: Number = 2;
        </fx:Script>

        <Label />
    </Application>
    """

    app = parser.parse(source)

    assert app.script_ast is not None
    # Both script blocks should be merged
    assert len(app.script_ast.declarations) == 2


def test_reactive_decorator_in_mxml(parser):
    """Test @reactive decorator in MXML script"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Script>
            @reactive var count: Number = 0;
        </fx:Script>

        <Label text="{count}" />
    </Application>
    """

    app = parser.parse(source)

    assert app.script_ast is not None
    var_decl = app.script_ast.declarations[0]
    assert var_decl.name == "count"
    assert len(var_decl.decorators) == 1
    assert var_decl.decorators[0].name == "reactive"


def test_parse_file(parser, tmp_path):
    """Test parsing MXML from file"""
    mxml_file = tmp_path / "test.mxml"
    mxml_file.write_text("""
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">
        <Label text="From File" />
    </Application>
    """)

    app = parser.parse_file(str(mxml_file))

    assert isinstance(app, MXMLApplication)
    assert len(app.root_component.children) == 1


def test_legacy_flex_namespace(parser):
    """Test compatibility with legacy Flex namespaces"""
    source = """
    <s:Application
        xmlns:fx="http://ns.adobe.com/mxml/2009"
        xmlns:s="library://ns.adobe.com/flex/spark">

        <s:Label text="Legacy" />
    </s:Application>
    """

    app = parser.parse(source)

    assert app.root_component.tag == "Application"
    assert len(app.root_component.children) == 1
    assert app.root_component.children[0].tag == "Label"


def test_hello_world_example(parser):
    """Test parsing actual hello-world example"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo"
        title="Hello OpenFlex Neo"
        width="800" height="600">

        <fx:Script>
            @reactive var message: String = "Hello, OpenFlex Neo!";

            function greet(): void {
                message = "Welcome to the future of ActionScript!";
            }
        </fx:Script>

        <fx:Style>
            .welcome {
                color: #2196F3;
                font-weight: bold;
            }
        </fx:Style>

        <VBox gap="{16}" padding="{32}">
            <Label text="{message}" fontSize="{32}" styleClass="welcome" />
            <Button label="Click Me" click="{greet}" />
        </VBox>
    </Application>
    """

    app = parser.parse(source)

    # Check metadata
    assert app.metadata['title'] == "Hello OpenFlex Neo"
    assert app.metadata['width'] == "800"

    # Check script
    assert app.script_ast is not None
    assert len(app.script_ast.declarations) == 2  # var + function

    # Check styles
    assert "welcome" in app.styles

    # Check component tree
    vbox = app.root_component.children[0]
    assert vbox.tag == "VBox"
    assert len(vbox.children) == 2


def test_counter_example(parser):
    """Test parsing actual counter example"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo"
        title="Counter Example">

        <fx:Script>
            @reactive var count: Number = 0;

            @computed var doubled: Number {
                return count * 2;
            }

            function increment(): void {
                count++;
            }

            function decrement(): void {
                count--;
            }
        </fx:Script>

        <VBox gap="{16}" padding="{32}">
            <Label text="{"Count: " + count}" fontSize="{24}" />
            <Label text="{"Doubled: " + doubled}" fontSize="{18}" />

            <HBox gap="{8}">
                <Button label="-" click="{decrement}" />
                <Button label="+" click="{increment}" />
            </HBox>
        </VBox>
    </Application>
    """

    app = parser.parse(source)

    # Check script has all declarations
    assert app.script_ast is not None
    assert len(app.script_ast.declarations) == 4  # 2 vars + 2 functions

    # Check reactive variable
    count_var = app.script_ast.declarations[0]
    assert count_var.name == "count"
    assert len(count_var.decorators) == 1
    assert count_var.decorators[0].name == "reactive"
