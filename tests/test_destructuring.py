"""
Tests for destructuring syntax compilation
"""

import pytest
from compiler.codegen.js_codegen import JSCodeGenerator
from compiler.parser.ast import *


class TestDestructuring:
    """Tests for array and object destructuring"""

    @pytest.fixture
    def codegen(self):
        """Create code generator"""
        return JSCodeGenerator()

    # ========================================================================
    # Array Destructuring Tests
    # ========================================================================

    def test_simple_array_destructuring(self, codegen):
        """Test simple array destructuring: const [a, b] = arr"""
        # For now, we'll create a DestructuringDeclaration that holds a pattern
        # This is a wrapper around VariableDeclaration with pattern support
        decl = DestructuringDeclaration(
            pattern=ArrayPattern(elements=[
                IdentifierPattern(name="a"),
                IdentifierPattern(name="b")
            ]),
            initializer=Identifier(name="arr"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert js == "const [a, b] = arr;"

    def test_array_destructuring_with_skip(self, codegen):
        """Test array destructuring with skipped elements: const [a, , c] = arr"""
        decl = DestructuringDeclaration(
            pattern=ArrayPattern(elements=[
                IdentifierPattern(name="a"),
                WildcardPattern(),  # Skip element
                IdentifierPattern(name="c")
            ]),
            initializer=Identifier(name="arr"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert js == "const [a, , c] = arr;"

    def test_array_destructuring_with_rest(self, codegen):
        """Test array destructuring with rest: const [first, ...rest] = arr"""
        decl = DestructuringDeclaration(
            pattern=ArrayPattern(
                elements=[IdentifierPattern(name="first")],
                rest="rest"
            ),
            initializer=Identifier(name="arr"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert js == "const [first, ...rest] = arr;"

    def test_array_destructuring_let(self, codegen):
        """Test array destructuring with let"""
        decl = DestructuringDeclaration(
            pattern=ArrayPattern(elements=[
                IdentifierPattern(name="x"),
                IdentifierPattern(name="y")
            ]),
            initializer=Identifier(name="point"),
            is_const=False
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert js == "let [x, y] = point;"

    def test_nested_array_destructuring(self, codegen):
        """Test nested array destructuring: const [[a, b], c] = arr"""
        decl = DestructuringDeclaration(
            pattern=ArrayPattern(elements=[
                ArrayPattern(elements=[
                    IdentifierPattern(name="a"),
                    IdentifierPattern(name="b")
                ]),
                IdentifierPattern(name="c")
            ]),
            initializer=Identifier(name="arr"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert js == "const [[a, b], c] = arr;"

    # ========================================================================
    # Object Destructuring Tests
    # ========================================================================

    def test_simple_object_destructuring(self, codegen):
        """Test simple object destructuring: const {x, y} = point"""
        decl = DestructuringDeclaration(
            pattern=ObjectPattern(properties={
                "x": IdentifierPattern(name="x"),
                "y": IdentifierPattern(name="y")
            }),
            initializer=Identifier(name="point"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert js == "const {x, y} = point;"

    def test_object_destructuring_with_rename(self, codegen):
        """Test object destructuring with rename: const {name: n, age: a} = person"""
        decl = DestructuringDeclaration(
            pattern=ObjectPattern(properties={
                "name": IdentifierPattern(name="n"),
                "age": IdentifierPattern(name="a")
            }),
            initializer=Identifier(name="person"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        # Should generate: const {name: n, age: a} = person;
        assert "const {" in js
        assert "name: n" in js
        assert "age: a" in js
        assert "} = person;" in js

    def test_object_destructuring_with_rest(self, codegen):
        """Test object destructuring with rest: const {x, ...rest} = obj"""
        decl = DestructuringDeclaration(
            pattern=ObjectPattern(
                properties={"x": IdentifierPattern(name="x")},
                rest="rest"
            ),
            initializer=Identifier(name="obj"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert js == "const {x, ...rest} = obj;"

    def test_nested_object_destructuring(self, codegen):
        """Test nested object destructuring: const {pos: {x, y}} = data"""
        decl = DestructuringDeclaration(
            pattern=ObjectPattern(properties={
                "pos": ObjectPattern(properties={
                    "x": IdentifierPattern(name="x"),
                    "y": IdentifierPattern(name="y")
                })
            }),
            initializer=Identifier(name="data"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert "const {pos: {x, y}} = data;" in js

    # ========================================================================
    # Mixed Destructuring Tests
    # ========================================================================

    def test_mixed_destructuring(self, codegen):
        """Test mixed array and object destructuring"""
        decl = DestructuringDeclaration(
            pattern=ArrayPattern(elements=[
                ObjectPattern(properties={
                    "x": IdentifierPattern(name="x"),
                    "y": IdentifierPattern(name="y")
                }),
                IdentifierPattern(name="label")
            ]),
            initializer=Identifier(name="data"),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert "const [{x, y}, label] = data;" in js

    # ========================================================================
    # Complete Program Tests
    # ========================================================================

    def test_destructuring_in_program(self, codegen):
        """Test destructuring in complete program"""
        program = Program(
            imports=[],
            declarations=[
                DestructuringDeclaration(
                    pattern=ArrayPattern(elements=[
                        IdentifierPattern(name="x"),
                        IdentifierPattern(name="y")
                    ]),
                    initializer=ArrayLiteral(elements=[
                        NumberLiteral(value=10, raw="10"),
                        NumberLiteral(value=20, raw="20")
                    ]),
                    is_const=True
                ),
                FunctionDeclaration(
                    name="main",
                    params=[],
                    return_type=None,
                    body=BlockStatement(body=[
                        ExpressionStatement(
                            expression=CallExpression(
                                callee=Identifier(name="console.log"),
                                arguments=[
                                    Identifier(name="x"),
                                    Identifier(name="y")
                                ]
                            )
                        )
                    ]),
                    is_async=False
                )
            ],
            source_file="test.as4"
        )

        js = codegen.generate(program)

        assert "const [x, y] = [10, 20];" in js
        assert "function main()" in js

    def test_destructuring_with_complex_initializer(self, codegen):
        """Test destructuring with complex initializer"""
        decl = DestructuringDeclaration(
            pattern=ObjectPattern(properties={
                "status": IdentifierPattern(name="status"),
                "data": IdentifierPattern(name="data")
            }),
            initializer=AwaitExpression(
                argument=CallExpression(
                    callee=MemberExpression(
                        object=Identifier(name="response"),
                        property=Identifier(name="json"),
                        is_computed=False
                    ),
                    arguments=[]
                )
            ),
            is_const=True
        )

        js = codegen._generate_destructuring_declaration(decl)

        assert "const {status, data} = await response.json();" in js
