"""
Tests for Reactivity Code Generation
"""

import pytest
from compiler.parser.as4_parser import AS4Parser
from compiler.codegen.js_codegen import JSCodeGenerator


class TestReactivityCodegen:
    """Tests for reactive code generation"""

    @pytest.fixture
    def parser(self):
        """Create AS4 parser instance"""
        return AS4Parser()

    @pytest.fixture
    def codegen(self):
        """Create JS code generator instance"""
        return JSCodeGenerator()

    def test_reactive_variable(self, parser, codegen):
        """Test @reactive variable generation"""
        source = """
        @reactive var count: Number = 0;
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "const count = new Signal(0);" in js
        assert "const { Signal, Computed, createEffect }" in js

    def test_reactive_string_variable(self, parser, codegen):
        """Test @reactive with string"""
        source = """
        @reactive var message: String = "Hello";
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert 'const message = new Signal("Hello");' in js

    def test_computed_variable(self, parser, codegen):
        """Test @computed variable generation"""
        source = """
        @reactive var count: Number = 0;
        @computed var doubled: Number = count * 2;
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "const count = new Signal(0);" in js
        assert "const doubled = new Computed(() => count.value * 2);" in js

    def test_effect_decorator(self, parser, codegen):
        """Test @effect function generation"""
        source = """
        @reactive var count: Number = 0;

        @effect
        function logCount(): void {
            trace(count);
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "createEffect(() => logCount());" in js
        assert "function logCount()" in js
        assert "trace(count.value);" in js

    def test_auto_value_read(self, parser, codegen):
        """Test auto .value transformation for reading"""
        source = """
        @reactive var count: Number = 0;

        function getCount(): Number {
            return count;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "return count.value;" in js

    def test_auto_value_write(self, parser, codegen):
        """Test auto .value transformation for writing"""
        source = """
        @reactive var count: Number = 0;

        function increment(): void {
            count = count + 1;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "count.value = count.value + 1;" in js

    def test_computed_with_multiple_dependencies(self, parser, codegen):
        """Test @computed with multiple reactive dependencies"""
        source = """
        @reactive var a: Number = 1;
        @reactive var b: Number = 2;
        @computed var sum: Number = a + b;
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "const a = new Signal(1);" in js
        assert "const b = new Signal(2);" in js
        assert "const sum = new Computed(() => a.value + b.value);" in js

    def test_non_reactive_variables_not_transformed(self, parser, codegen):
        """Test that non-reactive variables don't get .value"""
        source = """
        var x: Number = 0;

        function increment(): void {
            x = x + 1;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "let x = 0;" in js
        assert "x = x + 1;" in js
        assert "x.value" not in js

    def test_mixed_reactive_and_normal(self, parser, codegen):
        """Test mixing reactive and normal variables"""
        source = """
        @reactive var count: Number = 0;
        var multiplier: Number = 2;

        function compute(): Number {
            return count * multiplier;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        assert "const count = new Signal(0);" in js
        assert "let multiplier = 2;" in js
        assert "return count.value * multiplier;" in js

    def test_complete_reactivity_example(self, parser, codegen):
        """Test complete reactivity with all features"""
        source = """
        @reactive var count: Number = 0;
        @computed var doubled: Number = count * 2;

        @effect
        function logCount(): void {
            trace(count);
        }

        function increment(): void {
            count = count + 1;
        }
        """

        ast = parser.parse(source)
        js = codegen.generate(ast)

        # Check all parts
        assert "const count = new Signal(0);" in js
        assert "const doubled = new Computed(() => count.value * 2);" in js
        assert "createEffect(() => logCount());" in js
        assert "count.value = count.value + 1;" in js
        assert "const { Signal, Computed, createEffect }" in js
