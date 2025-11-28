"""
OpenFlex Neo - Pattern Matching Compiler
Compiles pattern matching to efficient JavaScript
"""

from typing import List, Set, Optional
from compiler.parser.ast import *


class PatternMatchingCompiler:
    """Compiles pattern matching expressions to JavaScript"""

    def __init__(self):
        self.temp_counter = 0
        self.current_indent = 0

    def _new_temp(self) -> str:
        """Generate a new temporary variable name"""
        self.temp_counter += 1
        return f"_match_temp_{self.temp_counter}"

    def _indent(self) -> str:
        """Get current indentation"""
        return "  " * self.current_indent

    def compile_enum_declaration(self, enum_decl: EnumDeclaration) -> str:
        """
        Compile enum declaration to JavaScript factory functions

        Example:
            enum Option<T> {
                Some(T),
                None
            }

        Compiles to:
            const Option = {
                Some: (value) => ({ _tag: 'Some', value }),
                None: { _tag: 'None' }
            };
        """
        lines = []

        lines.append(f"{self._indent()}const {enum_decl.name} = {{")
        self.current_indent += 1

        for variant in enum_decl.variants:
            if variant.fields:
                # Variant with fields - create factory function
                param_count = len(variant.fields)

                if param_count == 1:
                    params = "value"
                    obj_fields = "value"
                else:
                    params = ", ".join([f"field{i}" for i in range(param_count)])
                    obj_fields = ", ".join([f"field{i}" for i in range(param_count)])

                lines.append(
                    f"{self._indent()}{variant.name}: ({params}) => "
                    f"({{ _tag: '{variant.name}', {obj_fields} }}),"
                )
            else:
                # Variant without fields - create singleton object
                lines.append(f"{self._indent()}{variant.name}: {{ _tag: '{variant.name}' }},")

        self.current_indent -= 1
        lines.append(f"{self._indent()}}};")

        return "\n".join(lines)

    def compile_match_expression(self, match_expr: MatchExpression) -> str:
        """
        Compile match expression to JavaScript

        Example:
            match result {
                Some(value) => value * 2,
                None => 0
            }

        Compiles to:
            (() => {
                const _temp = result;
                if (_temp._tag === 'Some') {
                    const value = _temp.value;
                    return value * 2;
                } else if (_temp._tag === 'None') {
                    return 0;
                } else {
                    throw new Error('Non-exhaustive pattern match');
                }
            })()
        """
        lines = []
        temp_var = self._new_temp()

        # Wrap in IIFE
        lines.append("(() => {")
        self.current_indent += 1

        # Store scrutinee in temp variable
        lines.append(f"{self._indent()}const {temp_var} = {self._compile_expr(match_expr.scrutinee)};")

        # Generate if-else chain for each arm
        for i, arm in enumerate(match_expr.arms):
            condition = self._compile_pattern_test(arm.pattern, temp_var)
            bindings = self._compile_pattern_bindings(arm.pattern, temp_var)

            if i == 0:
                lines.append(f"{self._indent()}if ({condition}) {{")
            elif isinstance(arm.pattern, WildcardPattern):
                # Wildcard is catch-all, no condition needed
                lines.append(f"{self._indent()}}} else {{")
            else:
                lines.append(f"{self._indent()}}} else if ({condition}) {{")

            self.current_indent += 1

            # Add bindings
            for binding in bindings:
                lines.append(f"{self._indent()}{binding}")

            # Add guard if present
            if arm.guard:
                guard_expr = self._compile_expr(arm.guard)
                lines.append(f"{self._indent()}if ({guard_expr}) {{")
                self.current_indent += 1

            # Add body
            body_expr = self._compile_expr(arm.body)
            lines.append(f"{self._indent()}return {body_expr};")

            if arm.guard:
                self.current_indent -= 1
                lines.append(f"{self._indent()}}}")

            self.current_indent -= 1

        # Add non-exhaustive error
        if not any(isinstance(arm.pattern, WildcardPattern) for arm in match_expr.arms):
            lines.append(f"{self._indent()}}} else {{")
            self.current_indent += 1
            lines.append(f"{self._indent()}throw new Error('Non-exhaustive pattern match');")
            self.current_indent -= 1

        lines.append(f"{self._indent()}{'}}'}")

        self.current_indent -= 1
        lines.append(f"{self._indent()}{'}}'})()")

        return "\n".join(lines)

    def _compile_pattern_test(self, pattern: Pattern, temp_var: str) -> str:
        """Generate condition to test if pattern matches"""
        if isinstance(pattern, LiteralPattern):
            return f"{temp_var} === {self._format_literal(pattern.value)}"

        elif isinstance(pattern, IdentifierPattern):
            # Identifier always matches
            return "true"

        elif isinstance(pattern, WildcardPattern):
            # Wildcard always matches
            return "true"

        elif isinstance(pattern, VariantPattern):
            return f"{temp_var}._tag === '{pattern.variant_name}'"

        elif isinstance(pattern, TuplePattern):
            conditions = []
            for i, elem_pattern in enumerate(pattern.elements):
                elem_test = self._compile_pattern_test(elem_pattern, f"{temp_var}[{i}]")
                conditions.append(elem_test)
            return " && ".join(conditions) if conditions else "true"

        elif isinstance(pattern, ArrayPattern):
            return f"Array.isArray({temp_var}) && {temp_var}.length >= {len(pattern.elements)}"

        else:
            return "true"

    def _compile_pattern_bindings(self, pattern: Pattern, temp_var: str) -> List[str]:
        """Generate bindings for pattern variables"""
        bindings = []

        if isinstance(pattern, IdentifierPattern):
            bindings.append(f"const {pattern.name} = {temp_var};")

        elif isinstance(pattern, VariantPattern):
            if pattern.fields:
                for i, field_pattern in enumerate(pattern.fields):
                    if isinstance(field_pattern, IdentifierPattern):
                        if i == 0 and len(pattern.fields) == 1:
                            # Single field - access as .value
                            bindings.append(f"const {field_pattern.name} = {temp_var}.value;")
                        else:
                            # Multiple fields - access as .field0, .field1, etc.
                            bindings.append(f"const {field_pattern.name} = {temp_var}.field{i};")

        elif isinstance(pattern, TuplePattern):
            for i, elem_pattern in enumerate(pattern.elements):
                if isinstance(elem_pattern, IdentifierPattern):
                    bindings.append(f"const {elem_pattern.name} = {temp_var}[{i}];")

        elif isinstance(pattern, ArrayPattern):
            for i, elem_pattern in enumerate(pattern.elements):
                if isinstance(elem_pattern, IdentifierPattern):
                    bindings.append(f"const {elem_pattern.name} = {temp_var}[{i}];")

            if pattern.rest:
                bindings.append(f"const {pattern.rest} = {temp_var}.slice({len(pattern.elements)});")

        return bindings

    def _compile_expr(self, expr: Expression) -> str:
        """Compile expression to JavaScript (placeholder)"""
        # This would delegate to the main code generator
        if isinstance(expr, Literal):
            return self._format_literal(expr.value)
        elif isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, BinaryExpression):
            left = self._compile_expr(expr.left)
            right = self._compile_expr(expr.right)
            return f"{left} {expr.operator} {right}"
        elif isinstance(expr, CallExpression):
            callee = self._compile_expr(expr.callee)
            args = ", ".join([self._compile_expr(arg) for arg in expr.arguments])
            return f"{callee}({args})"
        else:
            return "undefined"

    def _format_literal(self, value: Any) -> str:
        """Format literal value as JavaScript"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif value is None:
            return "null"
        else:
            return str(value)


def check_exhaustiveness(match_expr: MatchExpression, enum_decl: Optional[EnumDeclaration] = None) -> bool:
    """
    Check if match expression is exhaustive

    Returns True if all cases are covered
    """
    patterns = [arm.pattern for arm in match_expr.arms]

    # If there's a wildcard, it's exhaustive
    if any(isinstance(p, WildcardPattern) for p in patterns):
        return True

    # If matching on enum, check all variants are covered
    if enum_decl:
        variant_names = {v.name for v in enum_decl.variants}
        matched_variants = {
            p.variant_name for p in patterns if isinstance(p, VariantPattern)
        }
        return variant_names == matched_variants

    # Otherwise, can't determine exhaustiveness
    return False
