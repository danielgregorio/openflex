"""
Tests for async/await compilation
"""

import pytest
from compiler.codegen.js_codegen import JSCodeGenerator
from compiler.parser.ast import *


class TestAsyncAwait:
    """Tests for async/await code generation"""

    @pytest.fixture
    def codegen(self):
        """Create code generator"""
        return JSCodeGenerator()

    def test_async_function_declaration(self, codegen):
        """Test async function declaration"""
        func = FunctionDeclaration(
            name="fetchData",
            params=[],
            return_type=None,
            body=BlockStatement(body=[
                ReturnStatement(
                    argument=StringLiteral(value="data", raw='"data"')
                )
            ]),
            is_async=True
        )

        js = codegen._generate_function_declaration(func)

        assert "async function fetchData()" in js
        assert "return \"data\";" in js

    def test_sync_function_declaration(self, codegen):
        """Test normal (non-async) function declaration"""
        func = FunctionDeclaration(
            name="getData",
            params=[],
            return_type=None,
            body=BlockStatement(body=[
                ReturnStatement(
                    argument=StringLiteral(value="data", raw='"data"')
                )
            ]),
            is_async=False
        )

        js = codegen._generate_function_declaration(func)

        assert "async" not in js
        assert "function getData()" in js

    def test_async_function_with_params(self, codegen):
        """Test async function with parameters"""
        func = FunctionDeclaration(
            name="fetchUser",
            params=[
                Parameter(name="id", param_type=Type(name="Number")),
                Parameter(name="cache", param_type=Type(name="Boolean"),
                         default_value=BooleanLiteral(value=True, raw="true"))
            ],
            return_type=None,
            body=BlockStatement(body=[]),
            is_async=True
        )

        js = codegen._generate_function_declaration(func)

        assert "async function fetchUser(id, cache = true)" in js

    def test_await_expression(self, codegen):
        """Test await expression generation"""
        await_expr = AwaitExpression(
            argument=CallExpression(
                callee=Identifier(name="fetch"),
                arguments=[StringLiteral(value="/api/data", raw='"/api/data"')]
            )
        )

        js = codegen._generate_expression(await_expr)

        assert js == 'await fetch("/api/data")'

    def test_await_identifier(self, codegen):
        """Test await on simple identifier"""
        await_expr = AwaitExpression(
            argument=Identifier(name="promise")
        )

        js = codegen._generate_expression(await_expr)

        assert js == "await promise"

    def test_async_arrow_function_expression_body(self, codegen):
        """Test async arrow function with expression body"""
        arrow = ArrowFunction(
            params=[Parameter(name="x", param_type=None)],
            body=BinaryExpression(
                operator="*",
                left=Identifier(name="x"),
                right=NumberLiteral(value=2, raw="2")
            ),
            is_async=True
        )

        js = codegen._generate_arrow_function(arrow)

        assert js == "async x => x * 2"

    def test_async_arrow_function_block_body(self, codegen):
        """Test async arrow function with block body"""
        arrow = ArrowFunction(
            params=[Parameter(name="url", param_type=None)],
            body=BlockStatement(body=[
                ReturnStatement(
                    argument=AwaitExpression(
                        argument=CallExpression(
                            callee=Identifier(name="fetch"),
                            arguments=[Identifier(name="url")]
                        )
                    )
                )
            ]),
            is_async=True
        )

        js = codegen._generate_arrow_function(arrow)

        assert "async url =>" in js
        assert "await fetch(url)" in js
        assert "return" in js

    def test_sync_arrow_function(self, codegen):
        """Test normal (non-async) arrow function"""
        arrow = ArrowFunction(
            params=[Parameter(name="x", param_type=None)],
            body=BinaryExpression(
                operator="+",
                left=Identifier(name="x"),
                right=NumberLiteral(value=1, raw="1")
            ),
            is_async=False
        )

        js = codegen._generate_arrow_function(arrow)

        assert "async" not in js
        assert js == "x => x + 1"

    def test_arrow_function_multiple_params(self, codegen):
        """Test arrow function with multiple parameters"""
        arrow = ArrowFunction(
            params=[
                Parameter(name="a", param_type=None),
                Parameter(name="b", param_type=None)
            ],
            body=BinaryExpression(
                operator="+",
                left=Identifier(name="a"),
                right=Identifier(name="b")
            ),
            is_async=True
        )

        js = codegen._generate_arrow_function(arrow)

        assert js == "async (a, b) => a + b"

    def test_arrow_function_with_default_param(self, codegen):
        """Test arrow function with default parameter"""
        arrow = ArrowFunction(
            params=[
                Parameter(name="x", param_type=None),
                Parameter(name="y", param_type=None,
                         default_value=NumberLiteral(value=10, raw="10"))
            ],
            body=Identifier(name="x"),
            is_async=False
        )

        js = codegen._generate_arrow_function(arrow)

        assert js == "(x, y = 10) => x"

    def test_nested_await_expressions(self, codegen):
        """Test nested await expressions"""
        func = FunctionDeclaration(
            name="fetchAndParse",
            params=[],
            return_type=None,
            body=BlockStatement(body=[
                VariableDeclaration(
                    name="response",
                    var_type=None,
                    initializer=AwaitExpression(
                        argument=CallExpression(
                            callee=Identifier(name="fetch"),
                            arguments=[StringLiteral(value="/api/data", raw='"/api/data"')]
                        )
                    ),
                    is_const=True
                ),
                VariableDeclaration(
                    name="data",
                    var_type=None,
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
                ),
                ReturnStatement(argument=Identifier(name="data"))
            ]),
            is_async=True
        )

        js = codegen._generate_function_declaration(func)

        assert "async function fetchAndParse()" in js
        assert "const response = await fetch(\"/api/data\");" in js
        assert "const data = await response.json();" in js
        assert "return data;" in js

    def test_complete_async_program(self, codegen):
        """Test complete program with async functions"""
        program = Program(
            imports=[],
            declarations=[
                FunctionDeclaration(
                    name="delay",
                    params=[Parameter(name="ms", param_type=Type(name="Number"))],
                    return_type=None,
                    body=BlockStatement(body=[
                        ReturnStatement(
                            argument=NewExpression(
                                callee=Identifier(name="Promise"),
                                arguments=[
                                    ArrowFunction(
                                        params=[Parameter(name="resolve", param_type=None)],
                                        body=CallExpression(
                                            callee=Identifier(name="setTimeout"),
                                            arguments=[
                                                Identifier(name="resolve"),
                                                Identifier(name="ms")
                                            ]
                                        ),
                                        is_async=False
                                    )
                                ]
                            )
                        )
                    ]),
                    is_async=False
                ),
                FunctionDeclaration(
                    name="main",
                    params=[],
                    return_type=None,
                    body=BlockStatement(body=[
                        ExpressionStatement(
                            expression=CallExpression(
                                callee=MemberExpression(
                                    object=Identifier(name="console"),
                                    property=Identifier(name="log"),
                                    is_computed=False
                                ),
                                arguments=[StringLiteral(value="Starting...", raw='"Starting..."')]
                            )
                        ),
                        ExpressionStatement(
                            expression=AwaitExpression(
                                argument=CallExpression(
                                    callee=Identifier(name="delay"),
                                    arguments=[NumberLiteral(value=1000, raw="1000")]
                                )
                            )
                        ),
                        ExpressionStatement(
                            expression=CallExpression(
                                callee=MemberExpression(
                                    object=Identifier(name="console"),
                                    property=Identifier(name="log"),
                                    is_computed=False
                                ),
                                arguments=[StringLiteral(value="Done!", raw='"Done!"')]
                            )
                        )
                    ]),
                    is_async=True
                )
            ],
            source_file="test.as4"
        )

        js = codegen.generate(program)

        assert "function delay(ms)" in js
        assert "new Promise" in js
        assert "setTimeout" in js
        assert "async function main()" in js
        assert "await delay(1000)" in js
        assert 'console.log("Starting...")' in js
        assert 'console.log("Done!")' in js
