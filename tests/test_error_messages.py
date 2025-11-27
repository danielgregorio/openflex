"""
Tests for error message formatting
"""

import pytest
from compiler.errors import (
    CompilerError,
    ParseError,
    TypeError,
    create_parse_error,
    create_type_error
)
from compiler.parser.ast import SourceLocation


class TestErrorFormatting:
    """Test error message formatting"""

    def test_basic_error_format(self):
        """Test basic error formatting"""
        error = CompilerError("Something went wrong")
        formatted = error.format_error(use_color=False)

        assert "✗ Error:" in formatted
        assert "Something went wrong" in formatted

    def test_error_with_location(self):
        """Test error with source location"""
        source = """var count: Number = 0;
var name: String = count;
var total: Number = 10;"""

        location = SourceLocation(
            file="test.as4",
            line=2,
            column=20,
            end_line=2,
            end_column=25
        )

        error = CompilerError(
            "Type mismatch",
            location=location,
            source_code=source
        )

        formatted = error.format_error(use_color=False)

        assert "test.as4:2:20" in formatted
        assert "var name: String = count;" in formatted
        assert "^^^^^" in formatted  # Pointer under 'count'

    def test_error_with_suggestion(self):
        """Test error with suggestion"""
        error = CompilerError(
            "Undefined variable",
            suggestion="Make sure the variable is declared before use"
        )

        formatted = error.format_error(use_color=False)

        assert "💡 Suggestion:" in formatted
        assert "Make sure the variable is declared" in formatted

    def test_parse_error_creation(self):
        """Test parse error creation with context"""
        source = """function test() {
    var x = 10
    return x;
}"""

        location = SourceLocation(
            file="test.as4",
            line=2,
            column=14,
            end_line=2,
            end_column=15
        )

        error = create_parse_error(
            "Missing semicolon",
            source=source,
            location=location,
            error_type="unexpected_token"
        )

        formatted = error.format_error(use_color=False)

        assert "Missing semicolon" in formatted
        assert "var x = 10" in formatted
        assert "💡 Suggestion:" in formatted

    def test_type_error_creation(self):
        """Test type error creation"""
        source = """var count: Number = 0;
var name: String = count;"""

        location = SourceLocation(
            file="test.as4",
            line=2,
            column=20,
            end_line=2,
            end_column=25
        )

        error = create_type_error(
            "Cannot assign Number to String",
            source=source,
            location=location,
            expected_type="String",
            actual_type="Number"
        )

        formatted = error.format_error(use_color=False)

        assert "Cannot assign Number to String" in formatted
        assert "Expected type 'String' but got 'Number'" in formatted

    def test_multiline_context(self):
        """Test error shows context lines"""
        source = """// Line 1
// Line 2
var x: Number = "string";  // Error here
// Line 4
// Line 5"""

        location = SourceLocation(
            file="test.as4",
            line=3,
            column=17,
            end_line=3,
            end_column=25
        )

        error = CompilerError(
            "Type mismatch",
            location=location,
            source_code=source
        )

        formatted = error.format_error(use_color=False)

        # Should show 2 lines before and 2 lines after
        assert "// Line 1" in formatted or "// Line 2" in formatted
        assert "var x: Number = \"string\";" in formatted
        assert "// Line 4" in formatted or "// Line 5" in formatted

    def test_error_at_start_of_file(self):
        """Test error at beginning of file"""
        source = """import invalid;
var x = 10;"""

        location = SourceLocation(
            file="test.as4",
            line=1,
            column=8,
            end_line=1,
            end_column=15
        )

        error = create_parse_error(
            "Invalid import statement",
            source=source,
            location=location,
            error_type="import_not_found"
        )

        formatted = error.format_error(use_color=False)

        assert "Invalid import statement" in formatted
        assert "import invalid;" in formatted

    def test_error_at_end_of_file(self):
        """Test error at end of file"""
        source = """var x = 10;
var y = 20;
function test() {"""  # Missing closing brace

        location = SourceLocation(
            file="test.as4",
            line=3,
            column=18,
            end_line=3,
            end_column=19
        )

        error = create_parse_error(
            "Unexpected end of file",
            source=source,
            location=location,
            error_type="unexpected_eof"
        )

        formatted = error.format_error(use_color=False)

        assert "Unexpected end of file" in formatted
        assert "check for unclosed brackets" in formatted.lower()
