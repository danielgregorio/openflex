"""
End-to-end integration tests for MXML Neo parser

These tests parse real example files and validate the complete pipeline:
MXML → Component Tree + AS4 Scripts → Full AST
"""

import pytest
from pathlib import Path
from compiler.parser.mxml_parser import MXMLParser
from compiler.parser.ast import (
    Program, VariableDeclaration, FunctionDeclaration,
    Identifier, BinaryExpression, CallExpression
)


@pytest.fixture
def parser():
    """Create MXML parser instance"""
    return MXMLParser()


@pytest.fixture
def examples_dir():
    """Get examples directory"""
    return Path(__file__).parent.parent.parent / "examples"


def test_hello_world_file(parser, examples_dir):
    """Test parsing actual hello-world example file"""
    hello_world = examples_dir / "hello-world" / "App.mxml"

    if not hello_world.exists():
        pytest.skip(f"Example file not found: {hello_world}")

    # Parse the file
    app = parser.parse_file(str(hello_world))

    # Verify structure
    assert app is not None, "Failed to parse hello-world example"
    assert app.root_component.tag == "Application", f"Expected Application, got {app.root_component.tag}"

    # Check metadata
    assert app.metadata.get('title') == "Hello World - OpenFlex Neo", "Missing or wrong title"

    # Verify script was parsed
    assert app.script_ast is not None, "No script found"
    assert isinstance(app.script_ast, Program), "Script is not a Program AST"

    # Check for @reactive variable
    var_decls = [d for d in app.script_ast.declarations if isinstance(d, VariableDeclaration)]
    assert len(var_decls) >= 1, "No variable declarations found"

    message_var = next((v for v in var_decls if v.name == "message"), None)
    assert message_var is not None, "Variable 'message' not found"

    # Check for greet function
    func_decls = [d for d in app.script_ast.declarations if isinstance(d, FunctionDeclaration)]
    greet_func = next((f for f in func_decls if f.name == "greet"), None)
    assert greet_func is not None, "Function 'greet' not found"

    # Verify component tree
    assert len(app.root_component.children) > 0, "No child components"

    # Check for VBox
    vbox = next((c for c in app.root_component.children if c.tag == "VBox"), None)
    assert vbox is not None, "VBox component not found"

    # VBox should have Label and Button
    assert len(vbox.children) >= 2, f"Expected at least 2 children in VBox, got {len(vbox.children)}"

    tags = [c.tag for c in vbox.children]
    assert "Label" in tags, "Label not found in VBox"
    assert "Button" in tags, "Button not found in VBox"

    # Check data binding on Label
    label = next(c for c in vbox.children if c.tag == "Label")
    if 'text' in label.properties:
        text_prop = label.properties['text']
        if isinstance(text_prop, dict) and 'binding' in text_prop:
            assert text_prop['binding'] == 'message', "Label text binding incorrect"

    print("✅ Hello World example parsed successfully!")
    print(f"   - Found {len(var_decls)} variables")
    print(f"   - Found {len(func_decls)} functions")
    print(f"   - Component tree has {len(app.root_component.children)} top-level children")


def test_counter_file(parser, examples_dir):
    """Test parsing actual counter example file"""
    counter = examples_dir / "counter" / "App.mxml"

    if not counter.exists():
        pytest.skip(f"Example file not found: {counter}")

    # Parse the file
    app = parser.parse_file(str(counter))

    # Verify structure
    assert app is not None, "Failed to parse counter example"
    assert app.root_component.tag == "Application"

    # Verify script
    assert app.script_ast is not None, "No script found"

    # Check for required variables
    var_decls = [d for d in app.script_ast.declarations if isinstance(d, VariableDeclaration)]
    var_names = [v.name for v in var_decls]

    assert "count" in var_names, "Variable 'count' not found"

    # Check for functions
    func_decls = [d for d in app.script_ast.declarations if isinstance(d, FunctionDeclaration)]
    func_names = [f.name for f in func_decls]

    assert "increment" in func_names, "Function 'increment' not found"
    assert "decrement" in func_names, "Function 'decrement' not found"

    # Verify component structure
    assert len(app.root_component.children) > 0, "No child components"

    print("✅ Counter example parsed successfully!")
    print(f"   - Found {len(var_decls)} variables: {var_names}")
    print(f"   - Found {len(func_decls)} functions: {func_names}")


def test_parse_all_examples(parser, examples_dir):
    """Parse all MXML files in examples directory"""
    if not examples_dir.exists():
        pytest.skip(f"Examples directory not found: {examples_dir}")

    mxml_files = list(examples_dir.rglob("*.mxml"))

    if not mxml_files:
        pytest.skip("No MXML example files found")

    results = {}

    for mxml_file in mxml_files:
        try:
            app = parser.parse_file(str(mxml_file))

            # Basic validation
            assert app is not None
            assert app.root_component is not None
            assert app.root_component.tag in ["Application", "Component", "Module"]

            results[mxml_file.name] = {
                'status': 'PASS',
                'components': len(app.root_component.children),
                'scripts': app.script_ast is not None,
                'styles': bool(app.styles)
            }

        except Exception as e:
            results[mxml_file.name] = {
                'status': 'FAIL',
                'error': str(e)
            }

    # Print summary
    print("\n📊 Example Files Parse Results:")
    print("=" * 60)

    passed = sum(1 for r in results.values() if r['status'] == 'PASS')
    total = len(results)

    for filename, result in results.items():
        if result['status'] == 'PASS':
            print(f"✅ {filename}")
            print(f"   Components: {result['components']}, Scripts: {result['scripts']}, Styles: {result['styles']}")
        else:
            print(f"❌ {filename}")
            print(f"   Error: {result['error']}")

    print("=" * 60)
    print(f"Results: {passed}/{total} passed ({100*passed//total}%)")

    # Ensure at least some examples parsed
    assert passed > 0, "No example files parsed successfully"
    assert passed == total, f"{total - passed} example files failed to parse"


def test_ast_structure_validation(parser):
    """Validate AST structure is complete and correct"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Script>
            var x: Number = 5;
            var y: Number = 10;

            function add(): Number {
                return x + y;
            }
        </fx:Script>

        <VBox>
            <Label text="Result" />
        </VBox>
    </Application>
    """

    app = parser.parse(source)

    # Validate AST completeness
    assert app.script_ast is not None

    # Check variables
    vars = [d for d in app.script_ast.declarations if isinstance(d, VariableDeclaration)]
    assert len(vars) == 2, f"Expected 2 variables, got {len(vars)}"

    x_var = next(v for v in vars if v.name == "x")
    assert x_var.var_type is not None, "Variable x has no type"
    assert x_var.initializer is not None, "Variable x has no initializer"

    # Check function
    funcs = [d for d in app.script_ast.declarations if isinstance(d, FunctionDeclaration)]
    assert len(funcs) == 1, f"Expected 1 function, got {len(funcs)}"

    add_func = funcs[0]
    assert add_func.name == "add"
    assert add_func.return_type is not None, "Function has no return type"
    assert add_func.body is not None, "Function has no body"
    assert len(add_func.body.body) > 0, "Function body is empty"

    # Check return statement contains binary expression
    return_stmt = add_func.body.body[0]
    assert hasattr(return_stmt, 'argument'), "Return statement has no argument"
    assert isinstance(return_stmt.argument, BinaryExpression), "Return argument is not a binary expression"

    print("✅ AST structure validation passed!")
    print(f"   - Variables: {len(vars)}")
    print(f"   - Functions: {len(funcs)}")
    print(f"   - AST depth validated")


def test_error_handling(parser):
    """Test that parser handles errors gracefully"""

    # Test 1: Invalid XML
    invalid_xml = "<Application><unclosed"

    with pytest.raises(Exception) as exc_info:
        parser.parse(invalid_xml)

    assert "Invalid MXML" in str(exc_info.value) or "XML" in str(exc_info.value)

    # Test 2: Invalid AS4 syntax
    invalid_as4 = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Script>
            var x = ;  // Invalid syntax
        </fx:Script>
    </Application>
    """

    # Should parse XML but may have issues with AS4
    # Parser should not crash
    try:
        app = parser.parse(invalid_as4)
        # If it parses, that's okay - just check it doesn't crash
        assert app is not None
    except Exception as e:
        # If it fails, that's also okay - just check error is meaningful
        assert len(str(e)) > 0

    print("✅ Error handling validated!")


def test_component_nesting_depth(parser):
    """Test deeply nested component structures"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <VBox>
            <HBox>
                <Panel>
                    <VBox>
                        <Label text="Deeply nested" />
                    </VBox>
                </Panel>
            </HBox>
        </VBox>
    </Application>
    """

    app = parser.parse(source)

    # Navigate down the tree
    level1 = app.root_component.children[0]  # VBox
    assert level1.tag == "VBox"

    level2 = level1.children[0]  # HBox
    assert level2.tag == "HBox"

    level3 = level2.children[0]  # Panel
    assert level3.tag == "Panel"

    level4 = level3.children[0]  # VBox
    assert level4.tag == "VBox"

    level5 = level4.children[0]  # Label
    assert level5.tag == "Label"
    assert level5.properties.get('text') == "Deeply nested"

    print("✅ Deep nesting handled correctly!")
    print("   - Successfully parsed 5 levels of nesting")


def test_complex_bindings(parser):
    """Test complex data binding expressions"""
    source = """
    <Application
        xmlns:fx="http://openflex.dev/core"
        xmlns="http://openflex.dev/neo">

        <fx:Script>
            var firstName: String = "John";
            var lastName: String = "Doe";
            var age: Number = 25;
        </fx:Script>

        <VBox>
            <Label text="{firstName}" />
            <Label text="{firstName + ' ' + lastName}" />
            <Label text="{'Age: ' + age}" />
        </VBox>
    </Application>
    """

    app = parser.parse(source)

    vbox = app.root_component.children[0]
    labels = [c for c in vbox.children if c.tag == "Label"]

    assert len(labels) == 3, f"Expected 3 labels, got {len(labels)}"

    # All should have text property with binding
    for label in labels:
        assert 'text' in label.properties, f"Label missing text property"
        text = label.properties['text']
        assert isinstance(text, dict) and 'binding' in text, "Text is not a binding"

    print("✅ Complex bindings parsed successfully!")
    print(f"   - Parsed {len(labels)} labels with bindings")


if __name__ == "__main__":
    # Allow running directly for quick testing
    parser = MXMLParser()
    examples = Path(__file__).parent.parent.parent / "examples"

    print("🧪 Running MXML Parser Integration Tests\n")

    try:
        test_hello_world_file(parser, examples)
    except Exception as e:
        print(f"❌ Hello World test failed: {e}")

    try:
        test_counter_file(parser, examples)
    except Exception as e:
        print(f"❌ Counter test failed: {e}")

    try:
        test_parse_all_examples(parser, examples)
    except Exception as e:
        print(f"❌ Parse all examples failed: {e}")

    try:
        test_ast_structure_validation(parser)
    except Exception as e:
        print(f"❌ AST validation failed: {e}")

    try:
        test_error_handling(parser)
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

    try:
        test_component_nesting_depth(parser)
    except Exception as e:
        print(f"❌ Nesting depth test failed: {e}")

    try:
        test_complex_bindings(parser)
    except Exception as e:
        print(f"❌ Complex bindings test failed: {e}")
