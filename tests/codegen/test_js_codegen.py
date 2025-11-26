"""
Tests for JavaScript Code Generator
"""

import pytest
from compiler.parser.as4_parser import AS4Parser
from compiler.codegen.js_codegen import JSCodeGenerator


class TestJSCodeGenerator:
    """Tests for JavaScript code generation"""

    @pytest.fixture
    def parser(self):
        """Create AS4 parser instance"""
        return AS4Parser()

    @pytest.fixture
    def codegen(self):
        """Create JS code generator instance"""
        return JSCodeGenerator()

    def test_simple_variable_declaration(self, parser, codegen):
        """Test variable declaration generation"""
        source = """
        var x: Number = 42;
        const name: String = "Alice";
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "let x = 42;" in js
        assert 'const name = "Alice";' in js

    def test_function_declaration(self, parser, codegen):
        """Test function declaration generation"""
        source = """
        function add(a: Number, b: Number): Number {
            return a + b;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "function add(a, b)" in js
        assert "return a + b;" in js

    def test_function_with_default_params(self, parser, codegen):
        """Test function with default parameters"""
        source = """
        function greet(name: String = "World"): String {
            return "Hello, " + name;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert 'function greet(name = "World")' in js

    def test_binary_expressions(self, parser, codegen):
        """Test binary expression generation"""
        source = """
        var sum: Number = 10 + 20;
        var product: Number = 5 * 3;
        var message: String = "Hello" + " " + "World";
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "let sum = 10 + 20;" in js
        assert "let product = 5 * 3;" in js

    def test_if_statement(self, parser, codegen):
        """Test if statement generation"""
        source = """
        function checkAge(age: Number): String {
            if (age >= 18) {
                return "Adult";
            } else {
                return "Minor";
            }
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "if (age >= 18)" in js
        assert 'return "Adult";' in js
        assert "else" in js
        assert 'return "Minor";' in js

    def test_for_loop(self, parser, codegen):
        """Test for loop generation"""
        source = """
        function sum(n: Number): Number {
            var total: Number = 0;
            for (var i: Number = 0; i < n; i++) {
                total = total + i;
            }
            return total;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "for (let i = 0; i < n; i++)" in js
        assert "total = total + i;" in js

    def test_while_loop(self, parser, codegen):
        """Test while loop generation"""
        source = """
        function countdown(n: Number): void {
            while (n > 0) {
                trace(n);
                n = n - 1;
            }
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "while (n > 0)" in js
        assert "trace(n);" in js

    def test_call_expression(self, parser, codegen):
        """Test function call generation"""
        source = """
        function main(): void {
            trace("Hello");
            var result: Number = add(1, 2);
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert 'trace("Hello");' in js
        assert "let result = add(1, 2);" in js

    def test_array_literal(self, parser, codegen):
        """Test array literal generation"""
        source = """
        var numbers: Array<Number> = [1, 2, 3, 4, 5];
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "let numbers = [1, 2, 3, 4, 5];" in js

    def test_class_declaration(self, parser, codegen):
        """Test class declaration generation"""
        source = """
        class Person {
            var name: String;
            var age: Number;

            function greet(): String {
                return "Hello, I'm " + name;
            }
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "class Person" in js
        assert "name;" in js
        assert "age;" in js
        assert "greet()" in js

    def test_class_with_extends(self, parser, codegen):
        """Test class inheritance generation"""
        source = """
        class Student extends Person {
            var grade: Number;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "class Student extends Person" in js
        assert "grade;" in js

    def test_hello_world_example(self, parser, codegen):
        """Test complete hello world example"""
        source = """
        function greet(name: String): String {
            return "Hello, " + name + "!";
        }

        function main(): void {
            const message: String = greet("World");
            trace(message);
        }

        main();
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        # Check that all parts are present
        assert "function greet(name)" in js
        assert 'return "Hello, " + name + "!";' in js
        assert "function main()" in js
        assert 'const message = greet("World");' in js
        assert "trace(message);" in js
        assert "main();" in js

        # Verify it's valid JavaScript (basic checks)
        assert js.count("{") == js.count("}")  # Balanced braces
