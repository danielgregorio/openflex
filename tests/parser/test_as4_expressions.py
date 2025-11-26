"""
Tests for AS4 expression parsing
"""

import pytest
from compiler.parser.as4_parser import AS4Parser
from compiler.parser.ast import (
    BinaryExpression, UnaryExpression, CallExpression,
    MemberExpression, ArrayLiteral, ObjectLiteral,
    NumberLiteral, StringLiteral, Identifier
)


@pytest.fixture
def parser():
    """Create parser instance"""
    try:
        return AS4Parser()
    except RuntimeError:
        pytest.skip("Tree-sitter grammar not built")


def test_binary_expression(parser):
    """Test binary expressions"""
    source = "var x = 1 + 2 * 3;"
    ast = parser.parse(source)

    var_decl = ast.declarations[0]
    init = var_decl.initializer

    assert isinstance(init, BinaryExpression)
    # Should parse as: 1 + (2 * 3) due to precedence


def test_unary_expression(parser):
    """Test unary expressions"""
    source = "var x = -5;"
    ast = parser.parse(source)

    var_decl = ast.declarations[0]
    init = var_decl.initializer

    assert isinstance(init, UnaryExpression)
    assert init.operator == '-'
    assert isinstance(init.operand, NumberLiteral)


def test_call_expression(parser):
    """Test function calls"""
    source = """
    function test(): void {
        foo(1, 2, 3);
    }
    """
    ast = parser.parse(source)

    func = ast.declarations[0]
    stmt = func.body.body[0]  # First statement in function

    assert stmt.expression
    assert isinstance(stmt.expression, CallExpression)
    assert isinstance(stmt.expression.callee, Identifier)
    assert len(stmt.expression.arguments) == 3


def test_member_expression(parser):
    """Test member access"""
    source = """
    function test(): void {
        obj.prop;
    }
    """
    ast = parser.parse(source)

    func = ast.declarations[0]
    stmt = func.body.body[0]

    assert isinstance(stmt.expression, MemberExpression)
    assert not stmt.expression.is_computed  # dot notation


def test_array_literal(parser):
    """Test array literals"""
    source = "var arr = [1, 2, 3];"
    ast = parser.parse(source)

    var_decl = ast.declarations[0]
    init = var_decl.initializer

    assert isinstance(init, ArrayLiteral)
    assert len(init.elements) == 3


def test_object_literal(parser):
    """Test object literals"""
    source = 'var obj = { name: "Alice", age: 30 };'
    ast = parser.parse(source)

    var_decl = ast.declarations[0]
    init = var_decl.initializer

    assert isinstance(init, ObjectLiteral)
    assert len(init.properties) == 2


def test_complex_expression(parser):
    """Test complex nested expression"""
    source = """
    var result = (x + y) * foo(1, 2) + obj.prop[0];
    """
    ast = parser.parse(source)

    var_decl = ast.declarations[0]
    init = var_decl.initializer

    # Should be a binary expression at the top level
    assert isinstance(init, BinaryExpression)


def test_increment_decrement(parser):
    """Test ++ and -- operators"""
    source = """
    function test(): void {
        count++;
        ++count;
    }
    """
    ast = parser.parse(source)

    func = ast.declarations[0]
    assert len(func.body.body) == 2

    # Both should be unary expressions
    stmt1 = func.body.body[0]
    stmt2 = func.body.body[1]

    assert isinstance(stmt1.expression, UnaryExpression)
    assert isinstance(stmt2.expression, UnaryExpression)
