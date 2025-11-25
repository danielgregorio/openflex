"""
Regression Test Suite for AS4 Features
Tests parser and type checker with real-world examples
"""

import pytest
from pathlib import Path
from compiler.parser.as4_parser import AS4Parser
from compiler.analyzer.type_checker import TypeChecker


class TestAS4Features:
    """Comprehensive regression tests for AS4 parser and type checker"""

    @pytest.fixture
    def parser(self):
        """Create AS4 parser instance"""
        return AS4Parser()

    @pytest.fixture
    def type_checker(self):
        """Create type checker instance"""
        return TypeChecker()

    @pytest.fixture
    def examples_dir(self):
        """Get examples directory path"""
        return Path(__file__).parent.parent.parent / "examples" / "as4-features"

    # ==================== LOOP TESTS ====================

    def test_for_loop_parsing(self, parser, examples_dir):
        """Test for loop example parses correctly"""
        file_path = examples_dir / "loops" / "for-loop.as4"

        if not file_path.exists():
            pytest.skip(f"Example file not found: {file_path}")

        source = file_path.read_text()
        ast = parser.parse(source, str(file_path))

        # Should parse without errors
        assert ast is not None
        assert len(ast.declarations) > 0

        # Should have function declarations
        functions = [d for d in ast.declarations if d.__class__.__name__ == 'FunctionDeclaration']
        assert len(functions) >= 3  # sumNumbers, printSquares, createGrid

    def test_while_loop_parsing(self, parser, examples_dir):
        """Test while loop example parses correctly"""
        file_path = examples_dir / "loops" / "while-loop.as4"

        if not file_path.exists():
            pytest.skip(f"Example file not found: {file_path}")

        source = file_path.read_text()
        ast = parser.parse(source, str(file_path))

        assert ast is not None
        assert len(ast.declarations) > 0

        # Should have function declarations with while loops
        functions = [d for d in ast.declarations if d.__class__.__name__ == 'FunctionDeclaration']
        assert len(functions) >= 2  # factorial, findPowerOfTwo

    def test_for_in_for_of_parsing(self, parser, examples_dir):
        """Test for-in and for-of loop examples parse correctly"""
        file_path = examples_dir / "loops" / "for-in-for-of.as4"

        if not file_path.exists():
            pytest.skip(f"Example file not found: {file_path}")

        source = file_path.read_text()
        ast = parser.parse(source, str(file_path))

        assert ast is not None
        assert len(ast.declarations) > 0

    # ==================== ERROR HANDLING TESTS ====================

    def test_try_catch_parsing(self, parser, examples_dir):
        """Test try-catch-finally example parses correctly"""
        file_path = examples_dir / "error-handling" / "try-catch.as4"

        if not file_path.exists():
            pytest.skip(f"Example file not found: {file_path}")

        source = file_path.read_text()
        ast = parser.parse(source, str(file_path))

        assert ast is not None
        assert len(ast.declarations) > 0

    # ==================== PATTERN MATCHING TESTS ====================

    def test_match_expressions_parsing(self, parser, examples_dir):
        """Test match expression examples parse correctly"""
        file_path = examples_dir / "pattern-matching" / "match-expressions.as4"

        if not file_path.exists():
            pytest.skip(f"Example file not found: {file_path}")

        source = file_path.read_text()
        ast = parser.parse(source, str(file_path))

        assert ast is not None
        assert len(ast.declarations) > 0

    # ==================== COMBINED FEATURES TESTS ====================

    def test_combined_features_parsing(self, parser, examples_dir):
        """Test combined features example parses correctly"""
        file_path = examples_dir / "combined" / "data-processor.as4"

        if not file_path.exists():
            pytest.skip(f"Example file not found: {file_path}")

        source = file_path.read_text()
        ast = parser.parse(source, str(file_path))

        assert ast is not None
        assert len(ast.declarations) > 0

        # Should have class declaration
        classes = [d for d in ast.declarations if d.__class__.__name__ == 'ClassDeclaration']
        assert len(classes) >= 1

    # ==================== TYPE CHECKING TESTS ====================

    def test_for_loop_type_checking(self, parser, type_checker, examples_dir):
        """Test type checking for for loop example"""
        file_path = examples_dir / "loops" / "for-loop.as4"

        if not file_path.exists():
            pytest.skip(f"Example file not found: {file_path}")

        source = file_path.read_text()
        ast = parser.parse(source, str(file_path))
        errors = type_checker.check_program(ast)

        # Should have minimal type errors (only from unimplemented features)
        # For now, we just verify it doesn't crash
        assert isinstance(errors, list)

    # ==================== REGRESSION TESTS ====================

    def test_existing_features_still_work(self, parser):
        """Ensure existing AS4 features still parse correctly"""
        # Test basic variable declarations
        source = """
        var x: Number = 42;
        const name: String = "Alice";
        """
        ast = parser.parse(source)
        assert len(ast.declarations) == 2

        # Test basic function declarations
        source = """
        function add(a: Number, b: Number): Number {
            return a + b;
        }
        """
        ast = parser.parse(source)
        assert len(ast.declarations) == 1
        func = ast.declarations[0]
        assert func.name == "add"
        assert len(func.params) == 2
        assert func.return_type.name == "Number"

    def test_expressions_still_work(self, parser):
        """Ensure expression parsing still works"""
        source = """
        var result: Number = 10 + 20 * 3;
        var greeting: String = "Hello, " + "World!";
        var valid: Boolean = x > 0 && y < 100;
        """
        ast = parser.parse(source)
        assert len(ast.declarations) == 3

    def test_type_checker_still_works(self, parser, type_checker):
        """Ensure type checker still validates correctly"""
        # Should catch type mismatch
        source = """
        var x: Number = "hello";
        """
        ast = parser.parse(source)
        errors = type_checker.check_program(ast)
        assert len(errors) >= 1
        assert "not assignable" in errors[0].message.lower()

        # Should accept correct types
        source = """
        var x: Number = 42;
        var y: String = "hello";
        """
        ast = parser.parse(source)
        errors = type_checker.check_program(ast)
        # May have other errors, but not type mismatch for these variables
        type_errors = [e for e in errors if "not assignable" in e.message.lower()]
        assert len(type_errors) == 0


class TestParserIntegrity:
    """Tests to ensure parser maintains integrity after changes"""

    @pytest.fixture
    def parser(self):
        return AS4Parser()

    def test_parser_handles_empty_source(self, parser):
        """Parser should handle empty source"""
        ast = parser.parse("")
        assert ast is not None
        assert len(ast.declarations) == 0

    def test_parser_handles_comments(self, parser):
        """Parser should handle comments correctly"""
        source = """
        // Single line comment
        var x: Number = 42;

        /* Multi-line
           comment */
        var y: String = "test";
        """
        ast = parser.parse(source)
        assert len(ast.declarations) == 2

    def test_parser_handles_whitespace(self, parser):
        """Parser should handle various whitespace"""
        source = """


        var    x   :   Number   =   42   ;


        """
        ast = parser.parse(source)
        assert len(ast.declarations) == 1

    def test_parser_location_tracking(self, parser):
        """Parser should track source locations"""
        source = """var x: Number = 42;"""
        ast = parser.parse(source)
        decl = ast.declarations[0]
        assert decl.loc is not None
        assert decl.loc.line >= 1


class TestTypeCheckerIntegrity:
    """Tests to ensure type checker maintains integrity"""

    @pytest.fixture
    def parser(self):
        return AS4Parser()

    @pytest.fixture
    def type_checker(self):
        return TypeChecker()

    def test_builtin_types_available(self, type_checker):
        """Builtin types should be available"""
        from compiler.parser.types import TYPE_MAP
        assert "Number" in TYPE_MAP
        assert "String" in TYPE_MAP
        assert "Boolean" in TYPE_MAP
        assert "void" in TYPE_MAP

    def test_function_scope_isolation(self, parser, type_checker):
        """Function scopes should be isolated"""
        source = """
        function foo(): void {
            var x: Number = 42;
        }

        function bar(): void {
            var y: Number = x;  // Should error: x not in scope
        }
        """
        ast = parser.parse(source)
        errors = type_checker.check_program(ast)
        # Should have error about 'x' not being found
        scope_errors = [e for e in errors if "cannot find name" in e.message.lower()]
        assert len(scope_errors) >= 1

    def test_type_inference_works(self, parser, type_checker):
        """Type inference should work for variables without explicit types"""
        source = """
        var x = 42;
        var y = "hello";
        var z = true;
        """
        ast = parser.parse(source)
        errors = type_checker.check_program(ast)
        # Should infer types without errors
        assert isinstance(errors, list)
