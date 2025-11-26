"""
Basic tests for AS4 parser
"""

import pytest
from compiler.parser.as4_parser import AS4Parser
from compiler.parser.ast import (
    Program, ImportDeclaration, VariableDeclaration,
    FunctionDeclaration, Decorator
)


def test_parser_initialization():
    """Test that parser initializes"""
    try:
        parser = AS4Parser()
        assert parser is not None
    except RuntimeError as e:
        # Grammar not built yet - skip
        pytest.skip(f"Tree-sitter grammar not built: {e}")


def test_simple_variable():
    """Test parsing simple variable declaration"""
    try:
        parser = AS4Parser()
    except RuntimeError:
        pytest.skip("Tree-sitter grammar not built")

    source = "var count: Number = 0;"
    ast = parser.parse(source)

    assert isinstance(ast, Program)
    assert len(ast.declarations) == 1

    var_decl = ast.declarations[0]
    assert isinstance(var_decl, VariableDeclaration)
    assert var_decl.name == "count"
    assert not var_decl.is_const


def test_reactive_variable():
    """Test parsing @reactive variable"""
    try:
        parser = AS4Parser()
    except RuntimeError:
        pytest.skip("Tree-sitter grammar not built")

    source = "@reactive var count: Number = 0;"
    ast = parser.parse(source)

    assert isinstance(ast, Program)
    assert len(ast.declarations) == 1

    var_decl = ast.declarations[0]
    assert isinstance(var_decl, VariableDeclaration)
    assert var_decl.name == "count"
    assert len(var_decl.decorators) == 1
    assert var_decl.decorators[0].name == "reactive"


def test_function_declaration():
    """Test parsing function"""
    try:
        parser = AS4Parser()
    except RuntimeError:
        pytest.skip("Tree-sitter grammar not built")

    source = """
    function greet(name: String): void {
        return;
    }
    """
    ast = parser.parse(source)

    assert isinstance(ast, Program)
    assert len(ast.declarations) == 1

    func_decl = ast.declarations[0]
    assert isinstance(func_decl, FunctionDeclaration)
    assert func_decl.name == "greet"
    assert len(func_decl.params) == 1
    assert func_decl.params[0].name == "name"


def test_import_statement():
    """Test parsing import"""
    try:
        parser = AS4Parser()
    except RuntimeError:
        pytest.skip("Tree-sitter grammar not built")

    source = "import openflex.reactive.Signal;"
    ast = parser.parse(source)

    assert isinstance(ast, Program)
    assert len(ast.imports) == 1

    import_decl = ast.imports[0]
    assert isinstance(import_decl, ImportDeclaration)
    assert import_decl.source == "openflex.reactive.Signal"


def test_complete_example():
    """Test parsing complete example"""
    try:
        parser = AS4Parser()
    except RuntimeError:
        pytest.skip("Tree-sitter grammar not built")

    source = """
    import openflex.reactive.Signal;

    @reactive var count: Number = 0;

    function increment(): void {
        count++;
    }
    """

    ast = parser.parse(source)

    assert isinstance(ast, Program)
    assert len(ast.imports) == 1
    assert len(ast.declarations) == 2  # var + function

    # Check variable
    var_decl = ast.declarations[0]
    assert isinstance(var_decl, VariableDeclaration)
    assert var_decl.name == "count"
    assert len(var_decl.decorators) == 1

    # Check function
    func_decl = ast.declarations[1]
    assert isinstance(func_decl, FunctionDeclaration)
    assert func_decl.name == "increment"
