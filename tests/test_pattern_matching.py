"""
Tests for pattern matching compilation
"""

import pytest
from compiler.pattern_matching import PatternMatchingCompiler, check_exhaustiveness
from compiler.parser.ast import *


class TestPatternMatchingCompiler:
    """Tests for pattern matching compilation"""

    @pytest.fixture
    def compiler(self):
        """Create pattern matching compiler"""
        return PatternMatchingCompiler()

    def test_enum_declaration_simple(self, compiler):
        """Test simple enum without fields"""
        enum_decl = EnumDeclaration(
            name="Color",
            variants=[
                EnumVariant(name="Red", fields=[]),
                EnumVariant(name="Green", fields=[]),
                EnumVariant(name="Blue", fields=[])
            ]
        )

        js = compiler.compile_enum_declaration(enum_decl)

        assert "const Color = {" in js
        assert "Red: { _tag: 'Red' }" in js
        assert "Green: { _tag: 'Green' }" in js
        assert "Blue: { _tag: 'Blue' }" in js

    def test_enum_declaration_with_fields(self, compiler):
        """Test enum with fields"""
        enum_decl = EnumDeclaration(
            name="Option",
            variants=[
                EnumVariant(name="Some", fields=[Type(name="T")]),
                EnumVariant(name="None", fields=[])
            ]
        )

        js = compiler.compile_enum_declaration(enum_decl)

        assert "const Option = {" in js
        assert "Some: (value) => ({ _tag: 'Some', value })" in js
        assert "None: { _tag: 'None' }" in js

    def test_enum_declaration_multiple_fields(self, compiler):
        """Test enum variant with multiple fields"""
        enum_decl = EnumDeclaration(
            name="Point",
            variants=[
                EnumVariant(name="Point2D", fields=[Type(name="Number"), Type(name="Number")]),
            ]
        )

        js = compiler.compile_enum_declaration(enum_decl)

        assert "Point2D: (field0, field1) => ({ _tag: 'Point2D', field0, field1 })" in js

    def test_match_expression_simple(self, compiler):
        """Test simple match expression"""
        match_expr = MatchExpression(
            scrutinee=Identifier(name="color"),
            arms=[
                MatchArm(
                    pattern=VariantPattern(variant_name="Red"),
                    body=Literal(value="red", raw='"red"')
                ),
                MatchArm(
                    pattern=VariantPattern(variant_name="Green"),
                    body=Literal(value="green", raw='"green"')
                ),
                MatchArm(
                    pattern=WildcardPattern(),
                    body=Literal(value="unknown", raw='"unknown"')
                )
            ]
        )

        js = compiler.compile_match_expression(match_expr)

        assert "const _match_temp_" in js
        assert "if (_match_temp_1._tag === 'Red')" in js
        assert "else if (_match_temp_1._tag === 'Green')" in js
        assert "else {" in js
        assert "return" in js

    def test_match_expression_with_binding(self, compiler):
        """Test match with variable binding"""
        match_expr = MatchExpression(
            scrutinee=Identifier(name="option"),
            arms=[
                MatchArm(
                    pattern=VariantPattern(
                        variant_name="Some",
                        fields=[IdentifierPattern(name="value")]
                    ),
                    body=Identifier(name="value")
                ),
                MatchArm(
                    pattern=VariantPattern(variant_name="None"),
                    body=Literal(value=0, raw="0")
                )
            ]
        )

        js = compiler.compile_match_expression(match_expr)

        assert "if (_match_temp_" in js and "._tag === 'Some')" in js
        assert "const value = _match_temp_" in js and ".value;" in js
        assert "return value;" in js

    def test_match_expression_with_guard(self, compiler):
        """Test match with guard clause"""
        match_expr = MatchExpression(
            scrutinee=Identifier(name="n"),
            arms=[
                MatchArm(
                    pattern=IdentifierPattern(name="x"),
                    guard=BinaryExpression(
                        operator=">",
                        left=Identifier(name="x"),
                        right=Literal(value=0, raw="0")
                    ),
                    body=Literal(value="positive", raw='"\"positive\""')
                ),
                MatchArm(
                    pattern=WildcardPattern(),
                    body=Literal(value="non-positive", raw='"\"non-positive\""')
                )
            ]
        )

        js = compiler.compile_match_expression(match_expr)

        assert "if (x > 0)" in js
        assert "return \"positive\";" in js

    def test_literal_pattern(self, compiler):
        """Test literal pattern matching"""
        pattern = LiteralPattern(value=42)
        condition = compiler._compile_pattern_test(pattern, "temp")

        assert condition == "temp === 42"

    def test_identifier_pattern(self, compiler):
        """Test identifier pattern (always matches)"""
        pattern = IdentifierPattern(name="x")
        condition = compiler._compile_pattern_test(pattern, "temp")

        assert condition == "true"

        bindings = compiler._compile_pattern_bindings(pattern, "temp")
        assert len(bindings) == 1
        assert bindings[0] == "const x = temp;"

    def test_wildcard_pattern(self, compiler):
        """Test wildcard pattern (always matches)"""
        pattern = WildcardPattern()
        condition = compiler._compile_pattern_test(pattern, "temp")

        assert condition == "true"

    def test_variant_pattern(self, compiler):
        """Test variant pattern matching"""
        pattern = VariantPattern(variant_name="Some")
        condition = compiler._compile_pattern_test(pattern, "temp")

        assert condition == "temp._tag === 'Some'"

    def test_array_pattern(self, compiler):
        """Test array pattern matching"""
        pattern = ArrayPattern(
            elements=[
                IdentifierPattern(name="first"),
                IdentifierPattern(name="second")
            ]
        )

        condition = compiler._compile_pattern_test(pattern, "arr")
        assert "Array.isArray(arr)" in condition
        assert "arr.length >= 2" in condition

        bindings = compiler._compile_pattern_bindings(pattern, "arr")
        assert "const first = arr[0];" in bindings
        assert "const second = arr[1];" in bindings

    def test_array_pattern_with_rest(self, compiler):
        """Test array pattern with rest element"""
        pattern = ArrayPattern(
            elements=[IdentifierPattern(name="first")],
            rest="rest"
        )

        bindings = compiler._compile_pattern_bindings(pattern, "arr")
        assert "const first = arr[0];" in bindings
        assert "const rest = arr.slice(1);" in bindings

    def test_exhaustiveness_with_wildcard(self):
        """Test exhaustiveness checking with wildcard"""
        match_expr = MatchExpression(
            scrutinee=Identifier(name="x"),
            arms=[
                MatchArm(pattern=VariantPattern(variant_name="Some"), body=Literal(value=1, raw="1")),
                MatchArm(pattern=WildcardPattern(), body=Literal(value=0, raw="0"))
            ]
        )

        assert check_exhaustiveness(match_expr) is True

    def test_exhaustiveness_with_all_variants(self):
        """Test exhaustiveness checking with all variants covered"""
        enum_decl = EnumDeclaration(
            name="Option",
            variants=[
                EnumVariant(name="Some", fields=[]),
                EnumVariant(name="None", fields=[])
            ]
        )

        match_expr = MatchExpression(
            scrutinee=Identifier(name="x"),
            arms=[
                MatchArm(pattern=VariantPattern(variant_name="Some"), body=Literal(value=1, raw="1")),
                MatchArm(pattern=VariantPattern(variant_name="None"), body=Literal(value=0, raw="0"))
            ]
        )

        assert check_exhaustiveness(match_expr, enum_decl) is True

    def test_exhaustiveness_missing_variant(self):
        """Test exhaustiveness checking with missing variant"""
        enum_decl = EnumDeclaration(
            name="Color",
            variants=[
                EnumVariant(name="Red", fields=[]),
                EnumVariant(name="Green", fields=[]),
                EnumVariant(name="Blue", fields=[])
            ]
        )

        match_expr = MatchExpression(
            scrutinee=Identifier(name="x"),
            arms=[
                MatchArm(pattern=VariantPattern(variant_name="Red"), body=Literal(value=1, raw="1")),
                MatchArm(pattern=VariantPattern(variant_name="Green"), body=Literal(value=2, raw="2"))
                # Missing Blue!
            ]
        )

        assert check_exhaustiveness(match_expr, enum_decl) is False

    def test_iife_wrapper(self, compiler):
        """Test that match expressions are wrapped in IIFE"""
        match_expr = MatchExpression(
            scrutinee=Identifier(name="x"),
            arms=[
                MatchArm(pattern=WildcardPattern(), body=Literal(value=42, raw="42"))
            ]
        )

        js = compiler.compile_match_expression(match_expr)

        # Should start with IIFE
        assert js.strip().startswith("(() => {")
        # Should end with IIFE call
        assert js.strip().endswith("})()")
