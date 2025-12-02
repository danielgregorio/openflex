"""
Tests for optional chaining (?.) and nullish coalescing (??) operators
"""

import pytest
from compiler.codegen.js_codegen import JSCodeGenerator
from compiler.parser.ast import *


class TestOptionalChaining:
    """Tests for ?. and ?? operators"""

    @pytest.fixture
    def codegen(self):
        """Create code generator"""
        return JSCodeGenerator()

    # ========================================================================
    # Optional Chaining Tests (?.)
    # ========================================================================

    def test_simple_optional_chaining(self, codegen):
        """Test simple optional chaining: obj?.prop"""
        expr = OptionalMemberExpression(
            object=Identifier(name="obj"),
            property=Identifier(name="prop"),
            is_computed=False
        )

        js = codegen._generate_expression(expr)

        assert js == "obj?.prop"

    def test_optional_chaining_computed(self, codegen):
        """Test optional chaining with computed property: obj?.[key]"""
        expr = OptionalMemberExpression(
            object=Identifier(name="obj"),
            property=Identifier(name="key"),
            is_computed=True
        )

        js = codegen._generate_expression(expr)

        assert js == "obj?.[key]"

    def test_nested_optional_chaining(self, codegen):
        """Test nested optional chaining: obj?.prop?.nested"""
        expr = OptionalMemberExpression(
            object=OptionalMemberExpression(
                object=Identifier(name="obj"),
                property=Identifier(name="prop"),
                is_computed=False
            ),
            property=Identifier(name="nested"),
            is_computed=False
        )

        js = codegen._generate_expression(expr)

        assert js == "obj?.prop?.nested"

    def test_optional_chaining_with_call(self, codegen):
        """Test optional chaining with function call: obj?.method()"""
        expr = OptionalCallExpression(
            callee=OptionalMemberExpression(
                object=Identifier(name="obj"),
                property=Identifier(name="method"),
                is_computed=False
            ),
            arguments=[]
        )

        js = codegen._generate_expression(expr)

        assert js == "obj?.method?.()"

    def test_optional_call_with_arguments(self, codegen):
        """Test optional call with arguments: func?.(arg1, arg2)"""
        expr = OptionalCallExpression(
            callee=Identifier(name="func"),
            arguments=[
                NumberLiteral(value=1, raw="1"),
                StringLiteral(value="test", raw='"test"')
            ]
        )

        js = codegen._generate_expression(expr)

        assert js == 'func?.(1, "test")'

    def test_deep_optional_chaining(self, codegen):
        """Test deep optional chaining: a?.b?.c?.d"""
        expr = OptionalMemberExpression(
            object=OptionalMemberExpression(
                object=OptionalMemberExpression(
                    object=Identifier(name="a"),
                    property=Identifier(name="b"),
                    is_computed=False
                ),
                property=Identifier(name="c"),
                is_computed=False
            ),
            property=Identifier(name="d"),
            is_computed=False
        )

        js = codegen._generate_expression(expr)

        assert js == "a?.b?.c?.d"

    def test_optional_chaining_with_array_access(self, codegen):
        """Test optional chaining with array access: arr?.[0]?.value"""
        expr = OptionalMemberExpression(
            object=OptionalMemberExpression(
                object=Identifier(name="arr"),
                property=NumberLiteral(value=0, raw="0"),
                is_computed=True
            ),
            property=Identifier(name="value"),
            is_computed=False
        )

        js = codegen._generate_expression(expr)

        assert js == "arr?.[0]?.value"

    # ========================================================================
    # Nullish Coalescing Tests (??)
    # ========================================================================

    def test_simple_nullish_coalescing(self, codegen):
        """Test simple nullish coalescing: value ?? defaultValue"""
        expr = BinaryExpression(
            operator="??",
            left=Identifier(name="value"),
            right=StringLiteral(value="default", raw='"default"')
        )

        js = codegen._generate_expression(expr)

        assert js == 'value ?? "default"'

    def test_nullish_coalescing_with_number(self, codegen):
        """Test nullish coalescing with number: count ?? 0"""
        expr = BinaryExpression(
            operator="??",
            left=Identifier(name="count"),
            right=NumberLiteral(value=0, raw="0")
        )

        js = codegen._generate_expression(expr)

        assert js == "count ?? 0"

    def test_chained_nullish_coalescing(self, codegen):
        """Test chained nullish coalescing: a ?? b ?? c"""
        expr = BinaryExpression(
            operator="??",
            left=BinaryExpression(
                operator="??",
                left=Identifier(name="a"),
                right=Identifier(name="b")
            ),
            right=Identifier(name="c")
        )

        js = codegen._generate_expression(expr)

        assert js == "a ?? b ?? c"

    def test_nullish_with_expression(self, codegen):
        """Test nullish coalescing with complex expression"""
        expr = BinaryExpression(
            operator="??",
            left=Identifier(name="value"),
            right=CallExpression(
                callee=Identifier(name="getDefault"),
                arguments=[]
            )
        )

        js = codegen._generate_expression(expr)

        assert js == "value ?? getDefault()"

    # ========================================================================
    # Combined Tests (?. and ??)
    # ========================================================================

    def test_optional_chaining_with_nullish_coalescing(self, codegen):
        """Test combining ?. and ??: obj?.prop ?? defaultValue"""
        expr = BinaryExpression(
            operator="??",
            left=OptionalMemberExpression(
                object=Identifier(name="obj"),
                property=Identifier(name="prop"),
                is_computed=False
            ),
            right=StringLiteral(value="default", raw='"default"')
        )

        js = codegen._generate_expression(expr)

        assert js == 'obj?.prop ?? "default"'

    def test_complex_optional_with_nullish(self, codegen):
        """Test complex combination: user?.profile?.name ?? "Guest" """
        expr = BinaryExpression(
            operator="??",
            left=OptionalMemberExpression(
                object=OptionalMemberExpression(
                    object=Identifier(name="user"),
                    property=Identifier(name="profile"),
                    is_computed=False
                ),
                property=Identifier(name="name"),
                is_computed=False
            ),
            right=StringLiteral(value="Guest", raw='"Guest"')
        )

        js = codegen._generate_expression(expr)

        assert js == 'user?.profile?.name ?? "Guest"'

    def test_optional_call_with_nullish(self, codegen):
        """Test optional call with nullish: getValue?.() ?? 0"""
        expr = BinaryExpression(
            operator="??",
            left=OptionalCallExpression(
                callee=Identifier(name="getValue"),
                arguments=[]
            ),
            right=NumberLiteral(value=0, raw="0")
        )

        js = codegen._generate_expression(expr)

        assert js == "getValue?.() ?? 0"

    # ========================================================================
    # In Variable Declarations
    # ========================================================================

    def test_optional_in_variable_declaration(self, codegen):
        """Test optional chaining in variable declaration"""
        decl = VariableDeclaration(
            name="name",
            var_type=None,
            initializer=OptionalMemberExpression(
                object=Identifier(name="user"),
                property=Identifier(name="name"),
                is_computed=False
            ),
            is_const=True
        )

        js = codegen._generate_variable_declaration(decl)

        assert js == "const name = user?.name;"

    def test_nullish_in_variable_declaration(self, codegen):
        """Test nullish coalescing in variable declaration"""
        decl = VariableDeclaration(
            name="timeout",
            var_type=None,
            initializer=BinaryExpression(
                operator="??",
                left=OptionalMemberExpression(
                    object=Identifier(name="config"),
                    property=Identifier(name="timeout"),
                    is_computed=False
                ),
                right=NumberLiteral(value=5000, raw="5000")
            ),
            is_const=True
        )

        js = codegen._generate_variable_declaration(decl)

        assert js == "const timeout = config?.timeout ?? 5000;"

    # ========================================================================
    # Complete Program Tests
    # ========================================================================

    def test_complete_program_with_optional_chaining(self, codegen):
        """Test complete program with optional chaining and nullish coalescing"""
        program = Program(
            imports=[],
            declarations=[
                FunctionDeclaration(
                    name="getUserName",
                    params=[Parameter(name="user", param_type=None)],
                    return_type=None,
                    body=BlockStatement(body=[
                        ReturnStatement(
                            argument=BinaryExpression(
                                operator="??",
                                left=OptionalMemberExpression(
                                    object=OptionalMemberExpression(
                                        object=Identifier(name="user"),
                                        property=Identifier(name="profile"),
                                        is_computed=False
                                    ),
                                    property=Identifier(name="name"),
                                    is_computed=False
                                ),
                                right=StringLiteral(value="Anonymous", raw='"Anonymous"')
                            )
                        )
                    ]),
                    is_async=False
                )
            ],
            source_file="test.as4"
        )

        js = codegen.generate(program)

        assert "function getUserName(user)" in js
        assert 'return user?.profile?.name ?? "Anonymous";' in js
