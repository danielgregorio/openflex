"""
AS4 Parser using Tree-sitter

This module provides a Python wrapper around the tree-sitter grammar
for ActionScript 4, converting tree-sitter parse trees into our AST.
"""

from typing import Optional, List, Any
from pathlib import Path
import os
import ctypes

try:
    from tree_sitter import Language, Parser as TSParser
except ImportError:
    raise ImportError(
        "tree-sitter is required. Install with: pip install tree-sitter"
    )

from .ast import (
    Program, Statement, Expression, Type,
    ImportDeclaration, ImportSpecifier,
    VariableDeclaration, FunctionDeclaration, Parameter,
    ClassDeclaration, InterfaceDeclaration, TraitDeclaration,
    BlockStatement, ExpressionStatement, ReturnStatement,
    IfStatement, ForStatement, ForInStatement, ForOfStatement, WhileStatement,
    BinaryExpression, UnaryExpression, CallExpression,
    MemberExpression, Identifier, Literal,
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    Decorator, ConditionalCompilation, ConditionExpression,
    ConditionIdentifier, ConditionAnd, ConditionOr, ConditionNot,
    ElifBlock, SourceLocation,
    PrimitiveType, NullableType, UnionType, ArrayType, GenericType,
)
from .types import TYPE_MAP, BuiltinTypes


class AS4Parser:
    """Parser for ActionScript 4 using tree-sitter"""

    def __init__(self):
        """Initialize the parser with tree-sitter grammar"""
        self.parser = None
        self.language = None
        self._init_parser()

    def _init_parser(self):
        """Initialize tree-sitter parser"""
        # Path to compiled grammar
        grammar_path = Path(__file__).parent / "tree-sitter-as4"
        lib_path = grammar_path / "build" / "as4.so"

        # Check if grammar is built
        if not lib_path.exists():
            raise RuntimeError(
                f"Tree-sitter grammar not built. Please run:\n"
                f"  cd {grammar_path}\n"
                f"  tree-sitter generate\n"
                f"  tree-sitter build\n"
                f"Or use the build script: bash {grammar_path.parent}/build_grammar.sh"
            )

        # Load language
        try:
            # Load the shared library
            lib = ctypes.cdll.LoadLibrary(str(lib_path))

            # Get the language function (tree_sitter_actionscript4)
            lang_func = lib.tree_sitter_actionscript4
            lang_func.restype = ctypes.c_void_p

            # Create Language object
            self.language = Language(lang_func())
            self.parser = TSParser()
            self.parser.language = self.language
        except Exception as e:
            raise RuntimeError(
                f"Failed to load tree-sitter grammar: {e}\n"
                f"Grammar path: {lib_path}\n"
                f"Try running: cd {grammar_path} && tree-sitter generate && tree-sitter build"
            )

    def parse(self, source: str, filename: str = "<input>") -> Program:
        """
        Parse AS4 source code into AST

        Args:
            source: AS4 source code
            filename: Source file name (for error reporting)

        Returns:
            Program AST node
        """
        if not self.parser:
            raise RuntimeError("Parser not initialized")

        # Parse with tree-sitter
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node

        # Convert to our AST
        visitor = ASTVisitor(source, filename)
        return visitor.visit_program(root)

    def parse_file(self, filepath: str) -> Program:
        """Parse AS4 file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.parse(source, filepath)


class ASTVisitor:
    """Visitor to convert tree-sitter nodes to our AST"""

    def __init__(self, source: str, filename: str):
        self.source = source
        self.filename = filename

    def _make_location(self, node) -> SourceLocation:
        """Create SourceLocation from tree-sitter node"""
        return SourceLocation(
            file=self.filename,
            line=node.start_point[0] + 1,
            column=node.start_point[1],
            end_line=node.end_point[0] + 1,
            end_column=node.end_point[1],
        )

    def _get_text(self, node) -> str:
        """Get text content of node"""
        return self.source[node.start_byte:node.end_byte]

    def visit_program(self, node) -> Program:
        """Visit source_file node"""
        statements = []
        imports = []
        declarations = []

        for child in node.children:
            if child.type == 'comment':
                continue

            stmt = self.visit_statement(child)
            if stmt:
                statements.append(stmt)

                # Separate imports from other declarations
                if isinstance(stmt, ImportDeclaration):
                    imports.append(stmt)
                else:
                    declarations.append(stmt)

        # Post-processing: Associate BlockStatements with @computed/@effect VariableDeclarations
        # This handles the syntax: @computed var name: Type { return expr; }
        # where the block_statement comes as a separate sibling node
        from compiler.parser.ast import VariableDeclaration, BlockStatement, ArrowFunction
        i = 0
        while i < len(declarations):
            decl = declarations[i]
            if isinstance(decl, VariableDeclaration):
                # Check if this is @computed or @effect without initializer
                is_computed_or_effect = any(d.name in ('computed', 'effect') for d in decl.decorators)
                if is_computed_or_effect and decl.initializer is None:
                    # Check if next declaration is a BlockStatement
                    if i + 1 < len(declarations) and isinstance(declarations[i + 1], BlockStatement):
                        block = declarations[i + 1]
                        # Wrap the block in an ArrowFunction
                        arrow_func = ArrowFunction(
                            params=[],
                            body=block,
                            is_async=False,
                            loc=block.loc
                        )
                        decl.initializer = arrow_func
                        # Remove the separate BlockStatement from declarations
                        declarations.pop(i + 1)
            i += 1

        return Program(
            imports=imports,
            declarations=declarations,
            source_file=self.filename,
            loc=self._make_location(node) if node.child_count > 0 else None
        )

    def visit_statement(self, node) -> Optional[Statement]:
        """Visit any statement node"""
        handlers = {
            'import_statement': self.visit_import,
            'variable_declaration': self.visit_variable_declaration,
            'function_declaration': self.visit_function_declaration,
            'class_declaration': self.visit_class_declaration,
            'interface_declaration': self.visit_interface_declaration,
            'trait_declaration': self.visit_trait_declaration,
            'conditional_compilation_block': self.visit_conditional_compilation,
            'if_statement': self.visit_if_statement,
            'for_statement': self.visit_for_statement,
            'for_in_statement': self.visit_for_in_statement,
            'for_of_statement': self.visit_for_of_statement,
            'while_statement': self.visit_while_statement,
            'return_statement': self.visit_return_statement,
            'expression_statement': self.visit_expression_statement,
            'block': self.visit_block,
            'block_statement': self.visit_block,  # Alias for block
        }

        handler = handlers.get(node.type)
        if handler:
            return handler(node)

        # Unknown node type - skip for now
        return None

    def visit_import(self, node) -> ImportDeclaration:
        """Visit import_statement node"""
        # Find import_path child
        path_node = node.child_by_field_name('path')
        if not path_node:
            path_node = next((c for c in node.children if c.type == 'import_path'), None)

        if not path_node:
            raise ValueError("Import statement missing path")

        # Extract package path
        path_parts = []
        for child in path_node.children:
            if child.type == 'identifier':
                path_parts.append(self._get_text(child))
            elif self._get_text(child) == '*':
                path_parts.append('*')

        source = '.'.join(path_parts)

        # Check for alias
        alias = None
        alias_node = node.child_by_field_name('alias')
        if alias_node:
            alias = self._get_text(alias_node)

        # For now, create simple import specifier
        # TODO: Handle different import patterns
        imported_name = path_parts[-1] if path_parts else source
        local_name = alias if alias else imported_name

        specifiers = [ImportSpecifier(imported=imported_name, local=local_name)]

        return ImportDeclaration(
            specifiers=specifiers,
            source=source,
            loc=self._make_location(node)
        )

    def visit_variable_declaration(self, node) -> VariableDeclaration:
        """Visit variable_declaration node"""
        # Extract decorators
        decorators = []
        decorator_list = node.child_by_field_name('decorators')
        if not decorator_list:
            # Fallback: find decorator nodes manually
            for child in node.children:
                if child.type == 'decorator_list':
                    decorator_list = child
                    break
        if decorator_list:
            decorators = self.visit_decorator_list(decorator_list)

        # Extract visibility
        visibility = "public"
        for child in node.children:
            if self._get_text(child) in ('public', 'private', 'protected'):
                visibility = self._get_text(child)
                break

        # Extract static
        is_static = any(self._get_text(c) == 'static' for c in node.children)

        # Extract var/const
        is_const = any(self._get_text(c) == 'const' for c in node.children)

        # Extract name
        name_node = node.child_by_field_name('name')
        if not name_node:
            name_node = next((c for c in node.children if c.type == 'identifier'), None)
        name = self._get_text(name_node) if name_node else "unknown"

        # Extract type (look for ':' followed by type node)
        var_type = None
        type_node = node.child_by_field_name('type')
        if not type_node:
            # Fallback: find ':' then get next 'type' node
            for i, child in enumerate(node.children):
                if self._get_text(child) == ':' and i + 1 < len(node.children):
                    next_node = node.children[i + 1]
                    if next_node.type == 'type':
                        type_node = next_node
                        break
        if type_node:
            var_type = self.visit_type(type_node)

        # Extract initializer (look for '=' followed by expression)
        initializer = None
        init_node = node.child_by_field_name('value')
        if not init_node:
            # Fallback: find '=' then get next 'expression' node
            for i, child in enumerate(node.children):
                if self._get_text(child) == '=' and i + 1 < len(node.children):
                    next_node = node.children[i + 1]
                    if next_node.type == 'expression':
                        init_node = next_node
                        break
        if init_node:
            initializer = self.visit_expression(init_node)

        return VariableDeclaration(
            name=name,
            var_type=var_type,
            initializer=initializer,
            is_const=is_const,
            decorators=decorators,
            visibility=visibility,
            is_static=is_static,
            loc=self._make_location(node)
        )

    def visit_function_declaration(self, node) -> FunctionDeclaration:
        """Visit function_declaration node"""
        # Extract decorators
        decorators = []
        decorator_list = node.child_by_field_name('decorators')
        if not decorator_list:
            # Fallback: find decorator nodes manually
            for child in node.children:
                if child.type == 'decorator_list':
                    decorator_list = child
                    break
        if decorator_list:
            decorators = self.visit_decorator_list(decorator_list)

        # Extract visibility
        visibility = "public"
        for child in node.children:
            if self._get_text(child) in ('public', 'private', 'protected'):
                visibility = self._get_text(child)
                break

        # Extract static, async
        is_static = any(self._get_text(c) == 'static' for c in node.children)
        is_async = any(self._get_text(c) == 'async' for c in node.children)

        # Extract name
        name_node = node.child_by_field_name('name')
        if not name_node:
            name_node = next((c for c in node.children if c.type == 'identifier'), None)
        name = self._get_text(name_node) if name_node else "unknown"

        # Extract parameters
        params = []
        param_list = node.child_by_field_name('parameters')
        if not param_list:
            # Fallback: find parameter_list node
            param_list = next((c for c in node.children if c.type == 'parameter_list'), None)
        if param_list:
            params = self.visit_parameter_list(param_list)

        # Extract return type (look for ':' followed by type)
        return_type = None
        type_node = node.child_by_field_name('return_type')
        if not type_node:
            # Fallback: find ':' after parameter_list, then get next 'type' node
            for i, child in enumerate(node.children):
                if self._get_text(child) == ':' and i > 0:
                    # Make sure this ':' is after the parameter list (not inside it)
                    prev_node = node.children[i - 1]
                    if prev_node.type == 'parameter_list' or prev_node.type == ')':
                        if i + 1 < len(node.children):
                            next_node = node.children[i + 1]
                            if next_node.type == 'type':
                                type_node = next_node
                                break
        if type_node:
            return_type = self.visit_type(type_node)

        # Extract body
        body_node = node.child_by_field_name('body')
        if not body_node:
            body_node = next((c for c in node.children if c.type == 'block'), None)
        body = self.visit_block(body_node) if body_node else BlockStatement(body=[])

        return FunctionDeclaration(
            name=name,
            params=params,
            return_type=return_type,
            body=body,
            is_async=is_async,
            visibility=visibility,
            is_static=is_static,
            decorators=decorators,
            loc=self._make_location(node)
        )

    def visit_decorator_list(self, node) -> List[Decorator]:
        """Visit decorator_list node"""
        decorators = []
        for child in node.children:
            if child.type == 'decorator':
                decorators.append(self.visit_decorator(child))
        return decorators

    def visit_decorator(self, node) -> Decorator:
        """Visit decorator node: @reactive, @computed, etc"""
        # Extract decorator name (after @)
        name = None
        for child in node.children:
            if child.type == 'identifier':
                name = self._get_text(child)
                break

        # Extract arguments (if any)
        arguments = []
        arg_list = node.child_by_field_name('arguments')
        if arg_list:
            for child in arg_list.children:
                if child.type == 'expression':
                    arguments.append(self.visit_expression(child))

        return Decorator(
            name=name or "unknown",
            arguments=arguments,
            loc=self._make_location(node)
        )

    def visit_conditional_compilation(self, node) -> ConditionalCompilation:
        """Visit conditional_compilation_block node"""
        # This is simplified - full implementation would handle #if, #elif, #else, #endif
        # For now, just create a placeholder
        condition = ConditionIdentifier(name="WEB")
        then_block = []

        return ConditionalCompilation(
            condition=condition,
            then_block=then_block,
            loc=self._make_location(node)
        )

    def visit_parameter_list(self, node) -> List[Parameter]:
        """Visit parameter_list node"""
        params = []
        for child in node.children:
            if child.type == 'parameter':
                params.append(self.visit_parameter(child))
        return params

    def visit_parameter(self, node) -> Parameter:
        """Visit parameter node"""
        # Extract name
        name_node = node.child_by_field_name('name')
        if not name_node:
            name_node = next((c for c in node.children if c.type == 'identifier'), None)
        name = self._get_text(name_node) if name_node else "unknown"

        # Extract type (look for ':' followed by type node)
        param_type = None
        type_node = node.child_by_field_name('type')
        if not type_node:
            # Fallback: find ':' then get next 'type' node
            for i, child in enumerate(node.children):
                if self._get_text(child) == ':' and i + 1 < len(node.children):
                    next_node = node.children[i + 1]
                    if next_node.type == 'type':
                        type_node = next_node
                        break
        if type_node:
            param_type = self.visit_type(type_node)

        # Extract default value
        default_value = None
        default_node = node.child_by_field_name('default')
        if not default_node:
            # Fallback: find '=' then get next expression
            for i, child in enumerate(node.children):
                if self._get_text(child) == '=' and i + 1 < len(node.children):
                    next_node = node.children[i + 1]
                    if next_node.type not in ('=', ',', ')'):
                        default_node = next_node
                        break
        if default_node:
            default_value = self.visit_expression(default_node)

        # Check for rest parameter (...)
        is_rest = any(self._get_text(c) == '...' for c in node.children)

        return Parameter(
            name=name,
            param_type=param_type,
            default_value=default_value,
            is_rest=is_rest,
            loc=self._make_location(node)
        )

    def visit_type(self, node) -> Type:
        """Visit type node"""
        # If this is a 'type' wrapper, unwrap it to get the actual type
        if node.type == 'type' and len(node.children) > 0:
            return self.visit_type(node.children[0])

        if node.type == 'identifier':
            type_name = self._get_text(node)
            return TYPE_MAP.get(type_name, PrimitiveType(
                kind=PrimitiveType(name=type_name).kind,
                name=type_name
            ))

        elif node.type == 'nullable_type':
            base_node = node.children[0]
            base_type = self.visit_type(base_node)
            return NullableType(
                kind=NullableType(base_type=base_type).kind,
                name=f"{base_type.name}?",
                base_type=base_type
            )

        elif node.type == 'union_type':
            types = []
            for child in node.children:
                if child.type != '|':
                    types.append(self.visit_type(child))
            return UnionType(
                kind=UnionType(types=types).kind,
                name=" | ".join(t.name for t in types),
                types=types
            )

        elif node.type == 'array_type':
            # Array<T>
            element_type = BuiltinTypes.ANY
            for child in node.children:
                if child.type != 'Array' and child.type != '<' and child.type != '>':
                    element_type = self.visit_type(child)
            return ArrayType(
                kind=ArrayType(element_type=element_type).kind,
                name=f"Array<{element_type.name}>",
                element_type=element_type
            )

        # Default: any
        return BuiltinTypes.ANY

    def visit_expression(self, node) -> Optional[Expression]:
        """Visit expression node"""
        # If this is a generic 'expression' wrapper, unwrap it
        if node.type == 'expression' and len(node.children) > 0:
            return self.visit_expression(node.children[0])

        # If this is a 'literal' wrapper, unwrap it
        if node.type == 'literal' and len(node.children) > 0:
            return self.visit_expression(node.children[0])

        if node.type == 'identifier':
            return Identifier(name=self._get_text(node), loc=self._make_location(node))

        elif node.type == 'number':
            text = self._get_text(node)
            # Strip whitespace and validate before converting to float
            stripped = text.strip()
            if not stripped:
                # Tree-sitter sometimes creates ghost nodes - skip them
                # This is likely a parsing artifact, return a placeholder
                print(f"WARNING: Skipping empty number node at {self._make_location(node)}")
                # Return 0 as a fallback
                return NumberLiteral(
                    value=0,
                    raw='0',
                    loc=self._make_location(node)
                )
            return NumberLiteral(
                value=float(stripped),
                raw=text,
                loc=self._make_location(node)
            )

        elif node.type == 'string':
            text = self._get_text(node)
            # Remove quotes
            value = text[1:-1] if len(text) >= 2 else text
            return StringLiteral(
                value=value,
                raw=text,
                loc=self._make_location(node)
            )

        elif node.type == 'boolean':
            text = self._get_text(node)
            return BooleanLiteral(
                value=text == 'true',
                raw=text,
                loc=self._make_location(node)
            )

        elif node.type == 'null':
            return NullLiteral(value=None, raw='null', loc=self._make_location(node))

        elif node.type == 'binary_expression':
            return self.visit_binary_expression(node)

        elif node.type == 'unary_expression':
            return self.visit_unary_expression(node)

        elif node.type == 'call_expression':
            return self.visit_call_expression(node)

        elif node.type == 'member_expression':
            return self.visit_member_expression(node)

        elif node.type == 'array_literal':
            return self.visit_array_literal(node)

        elif node.type == 'object_literal':
            return self.visit_object_literal(node)

        elif node.type == 'arrow_function':
            return self.visit_arrow_function(node)

        elif node.type == 'await_expression':
            return self.visit_await_expression(node)

        elif node.type == 'new_expression':
            return self.visit_new_expression(node)

        elif node.type == 'ternary_expression':
            return self.visit_ternary_expression(node)

        elif node.type == 'parenthesized_expression':
            # Unwrap parentheses
            for child in node.children:
                if child.type != '(' and child.type != ')':
                    return self.visit_expression(child)

        # Unknown expression type
        return None

    def visit_binary_expression(self, node) -> BinaryExpression:
        """Visit binary_expression node"""
        left = None
        operator = None
        right = None

        for child in node.children:
            if child.type == 'expression' or child.type in ('identifier', 'number', 'string'):
                if left is None:
                    left = self.visit_expression(child)
                else:
                    right = self.visit_expression(child)
            elif self._get_text(child) in ('+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '='):
                operator = self._get_text(child)

        return BinaryExpression(
            operator=operator or '+',
            left=left or Identifier(name="unknown"),
            right=right or Identifier(name="unknown"),
            loc=self._make_location(node)
        )

    def visit_unary_expression(self, node) -> UnaryExpression:
        """Visit unary_expression node"""
        operator = None
        operand = None
        is_prefix = True

        for i, child in enumerate(node.children):
            text = self._get_text(child)
            if text in ('-', '!', '++', '--'):
                operator = text
                is_prefix = (i == 0)
            elif child.type in ('expression', 'identifier', 'number'):
                operand = self.visit_expression(child)

        return UnaryExpression(
            operator=operator or '-',
            operand=operand or Identifier(name="unknown"),
            is_prefix=is_prefix,
            loc=self._make_location(node)
        )

    def visit_call_expression(self, node) -> CallExpression:
        """Visit call_expression node"""
        callee = None
        arguments = []

        for child in node.children:
            if child.type in ('identifier', 'member_expression', 'expression'):
                if callee is None:
                    callee = self.visit_expression(child)
            elif child.type == 'argument_list':
                arguments = self.visit_argument_list(child)

        return CallExpression(
            callee=callee or Identifier(name="unknown"),
            arguments=arguments,
            loc=self._make_location(node)
        )

    def visit_argument_list(self, node) -> List[Expression]:
        """Visit argument_list node"""
        arguments = []
        for child in node.children:
            if child.type != '(' and child.type != ')' and child.type != ',':
                expr = self.visit_expression(child)
                if expr:
                    arguments.append(expr)
        return arguments

    def visit_member_expression(self, node) -> MemberExpression:
        """Visit member_expression node"""
        object_expr = None
        property_expr = None
        is_computed = False

        for child in node.children:
            text = self._get_text(child)
            if text == '.':
                continue
            elif text == '[':
                is_computed = True
            elif text == ']':
                continue
            elif object_expr is None:
                object_expr = self.visit_expression(child)
            else:
                if is_computed:
                    property_expr = self.visit_expression(child)
                else:
                    property_expr = Identifier(name=text)

        return MemberExpression(
            object=object_expr or Identifier(name="unknown"),
            property=property_expr or Identifier(name="unknown"),
            is_computed=is_computed,
            loc=self._make_location(node)
        )

    def visit_array_literal(self, node) -> 'ArrayLiteral':
        """Visit array_literal node"""
        from .ast import ArrayLiteral
        elements = []
        for child in node.children:
            if child.type != '[' and child.type != ']' and child.type != ',':
                expr = self.visit_expression(child)
                if expr:
                    elements.append(expr)

        return ArrayLiteral(elements=elements, loc=self._make_location(node))

    def visit_object_literal(self, node) -> 'ObjectLiteral':
        """Visit object_literal node"""
        from .ast import ObjectLiteral, Property
        properties = []
        for child in node.children:
            if child.type == 'property':
                prop = self.visit_property(child)
                if prop:
                    properties.append(prop)

        return ObjectLiteral(properties=properties, loc=self._make_location(node))

    def visit_property(self, node) -> 'Property':
        """Visit property node"""
        from .ast import Property
        key = None
        value = None
        is_computed = False

        for child in node.children:
            if child.type == ':':
                continue
            elif child.type == '[':
                is_computed = True
            elif child.type == ']':
                continue
            elif key is None:
                if child.type == 'identifier':
                    key = Identifier(name=self._get_text(child))
                elif child.type == 'string':
                    key = self.visit_expression(child)
                else:
                    key = self.visit_expression(child)
            else:
                value = self.visit_expression(child)

        return Property(
            key=key or Identifier(name="unknown"),
            value=value or Identifier(name="unknown"),
            is_computed=is_computed,
            loc=self._make_location(node)
        )

    def visit_arrow_function(self, node) -> 'ArrowFunction':
        """Visit arrow_function node"""
        from .ast import ArrowFunction
        params = []
        body = None

        for child in node.children:
            if child.type == 'parameter_list':
                params = self.visit_parameter_list(child)
            elif child.type == 'identifier':
                # Single parameter without parens
                params = [Parameter(name=self._get_text(child), param_type=None)]
            elif child.type == '=>':
                continue
            elif child.type == 'block':
                body = self.visit_block(child)
            else:
                # Expression body
                body = self.visit_expression(child)

        return ArrowFunction(
            params=params,
            body=body or BlockStatement(body=[]),
            is_async=False,
            loc=self._make_location(node)
        )

    def visit_await_expression(self, node) -> 'AwaitExpression':
        """Visit await_expression node"""
        from .ast import AwaitExpression
        argument = None
        for child in node.children:
            if self._get_text(child) != 'await':
                argument = self.visit_expression(child)
                break

        return AwaitExpression(
            argument=argument or Identifier(name="unknown"),
            loc=self._make_location(node)
        )

    def visit_new_expression(self, node) -> 'NewExpression':
        """Visit new_expression node"""
        from .ast import NewExpression
        callee = None
        arguments = []

        for child in node.children:
            if self._get_text(child) == 'new':
                continue
            elif child.type == 'type' or child.type == 'identifier':
                if callee is None:
                    callee = self.visit_expression(child) if child.type != 'type' else Identifier(name=self._get_text(child))
            elif child.type == 'argument_list':
                arguments = self.visit_argument_list(child)

        return NewExpression(
            callee=callee or Identifier(name="unknown"),
            arguments=arguments,
            loc=self._make_location(node)
        )

    def visit_ternary_expression(self, node) -> 'ConditionalExpression':
        """Visit ternary_expression node"""
        from .ast import ConditionalExpression
        test = None
        consequent = None
        alternate = None

        parts = []
        for child in node.children:
            if child.type not in ('?', ':'):
                expr = self.visit_expression(child)
                if expr:
                    parts.append(expr)

        if len(parts) >= 3:
            test = parts[0]
            consequent = parts[1]
            alternate = parts[2]

        return ConditionalExpression(
            test=test or Identifier(name="true"),
            consequent=consequent or Identifier(name="unknown"),
            alternate=alternate or Identifier(name="unknown"),
            loc=self._make_location(node)
        )

    def visit_block(self, node) -> BlockStatement:
        """Visit block node"""
        statements = []
        for child in node.children:
            if child.type == '{' or child.type == '}':
                continue
            stmt = self.visit_statement(child)
            if stmt:
                statements.append(stmt)

        return BlockStatement(body=statements, loc=self._make_location(node))

    def visit_if_statement(self, node) -> IfStatement:
        """Visit if_statement node"""
        # DEBUG: Log children
        #print(f"DEBUG if_statement children:")
        #for i, child in enumerate(node.children):
        #    print(f"  {i}: {child.type} = {self._get_text(child)[:30]}")

        # Extract test condition
        test = None
        test_node = node.child_by_field_name('condition')
        if not test_node:
            # Fallback: find expression between parentheses
            in_parens = False
            for child in node.children:
                if child.type == '(':
                    in_parens = True
                elif child.type == ')':
                    in_parens = False
                elif in_parens and child.type not in ('(', ')'):
                    test_node = child
                    break

        if test_node:
            test = self.visit_expression(test_node)

        # Extract consequent
        consequent = None
        then_node = node.child_by_field_name('consequence')
        if not then_node:
            # Fallback: find first statement-like node after closing paren
            found_closing_paren = False
            for child in node.children:
                if child.type == ')':
                    found_closing_paren = True
                elif found_closing_paren and child.type not in ('if', '(', ')', 'else'):
                    then_node = child
                    break

        if then_node:
            consequent = self.visit_statement(then_node)

        # Extract alternate (else)
        alternate = None
        else_node = node.child_by_field_name('alternative')
        if not else_node:
            # Fallback: find statement after 'else' keyword
            found_else = False
            for child in node.children:
                if self._get_text(child) == 'else':
                    found_else = True
                elif found_else and child.type not in ('else',):
                    else_node = child
                    break

        if else_node:
            alternate = self.visit_statement(else_node)

        return IfStatement(
            test=test or Identifier(name="true"),  # Fallback
            consequent=consequent or BlockStatement(body=[]),
            alternate=alternate,
            loc=self._make_location(node)
        )

    def visit_for_statement(self, node) -> ForStatement:
        """Visit for_statement node: for (init; test; update) body"""
        # Parse: for ( init ; test ; update ) statement
        # Children: 'for', '(', init?, ';', test?, ';', update?, ')', statement

        init = None
        test = None
        update = None
        body = BlockStatement(body=[])

        # Find the components by iterating through children
        in_parens = False
        semicolon_count = 0

        for i, child in enumerate(node.children):
            if child.type == '(':
                in_parens = True
            elif child.type == ')':
                in_parens = False
            elif child.type == ';' and in_parens:
                semicolon_count += 1
            elif in_parens and child.type not in ('(', ')', ';', 'for'):
                # Determine which component this is based on semicolon count
                if semicolon_count == 0:
                    # This is the init
                    if child.type == 'variable_declaration':
                        init = self.visit_variable_declaration(child)
                    else:
                        init = self.visit_expression(child)
                elif semicolon_count == 1:
                    # This is the test
                    test = self.visit_expression(child)
                elif semicolon_count == 2:
                    # This is the update
                    update = self.visit_expression(child)
            elif not in_parens and child.type != 'for':
                # This is the body statement
                body = self.visit_statement(child)

        return ForStatement(
            init=init,
            test=test,
            update=update,
            body=body,
            loc=self._make_location(node)
        )

    def visit_while_statement(self, node) -> WhileStatement:
        """Visit while_statement node: while (test) body"""
        # Parse: while ( expression ) statement
        # Children: 'while', '(', expression, ')', statement

        test = None
        body = BlockStatement(body=[])

        in_parens = False
        for child in node.children:
            if child.type == '(':
                in_parens = True
            elif child.type == ')':
                in_parens = False
            elif in_parens and child.type not in ('(', ')'):
                # This is the test expression
                test = self.visit_expression(child)
            elif not in_parens and child.type not in ('while', '(', ')'):
                # This is the body statement
                body = self.visit_statement(child)

        if test is None:
            test = Identifier(name="true")  # Fallback

        return WhileStatement(test=test, body=body, loc=self._make_location(node))

    def visit_for_in_statement(self, node) -> 'ForInStatement':
        """Visit for_in_statement node: for (left in right) body"""
        # Parse: for ( (var x | x) in expression ) statement
        # Children: 'for', '(', (variable_declaration | identifier), 'in', expression, ')', statement

        left = None
        right = None
        body = BlockStatement(body=[])

        in_parens = False
        found_in_keyword = False

        for child in node.children:
            if child.type == '(':
                in_parens = True
            elif child.type == ')':
                in_parens = False
            elif in_parens and child.type == 'in':
                found_in_keyword = True
            elif in_parens and not found_in_keyword:
                # This is the left side (before 'in')
                if child.type == 'variable_declaration':
                    left = self.visit_variable_declaration(child)
                elif child.type == 'identifier':
                    left = Identifier(name=self._get_text(child))
            elif in_parens and found_in_keyword and child.type not in ('in',):
                # This is the right side (after 'in')
                right = self.visit_expression(child)
            elif not in_parens and child.type not in ('for', '(', ')'):
                # This is the body statement
                body = self.visit_statement(child)

        return ForInStatement(
            left=left or Identifier(name="unknown"),
            right=right or Identifier(name="unknown"),
            body=body,
            loc=self._make_location(node)
        )

    def visit_for_of_statement(self, node) -> 'ForOfStatement':
        """Visit for_of_statement node: for (left of right) body"""
        # Parse: for ( (var x | x) of expression ) statement
        # Children: 'for', '(', (variable_declaration | identifier), 'of', expression, ')', statement

        left = None
        right = None
        body = BlockStatement(body=[])

        in_parens = False
        found_of_keyword = False

        for child in node.children:
            if child.type == '(':
                in_parens = True
            elif child.type == ')':
                in_parens = False
            elif in_parens and child.type == 'of':
                found_of_keyword = True
            elif in_parens and not found_of_keyword:
                # This is the left side (before 'of')
                if child.type == 'variable_declaration':
                    left = self.visit_variable_declaration(child)
                elif child.type == 'identifier':
                    left = Identifier(name=self._get_text(child))
            elif in_parens and found_of_keyword and child.type not in ('of',):
                # This is the right side (after 'of')
                right = self.visit_expression(child)
            elif not in_parens and child.type not in ('for', '(', ')'):
                # This is the body statement
                body = self.visit_statement(child)

        return ForOfStatement(
            left=left or Identifier(name="unknown"),
            right=right or Identifier(name="unknown"),
            body=body,
            loc=self._make_location(node)
        )

    def visit_return_statement(self, node) -> ReturnStatement:
        """Visit return_statement node"""
        argument = None
        arg_node = node.child_by_field_name('argument')

        if not arg_node:
            # Fallback: find first expression child (skip 'return' keyword and ';')
            for child in node.children:
                if child.type not in ('return', ';'):
                    arg_node = child
                    break

        if arg_node:
            argument = self.visit_expression(arg_node)

        return ReturnStatement(argument=argument, loc=self._make_location(node))

    def visit_expression_statement(self, node) -> ExpressionStatement:
        """Visit expression_statement node"""
        expr = None
        for child in node.children:
            if child.type != ';':
                expr = self.visit_expression(child)
                break

        return ExpressionStatement(
            expression=expr or Identifier(name="unknown"),
            loc=self._make_location(node)
        )

    # Stubs for not-yet-implemented nodes
    def visit_class_declaration(self, node) -> Optional[Statement]:
        """Visit class_declaration node"""
        # Extract visibility (optional)
        visibility = "public"
        for child in node.children:
            if self._get_text(child) in ('public', 'private', 'protected'):
                visibility = self._get_text(child)
                break

        # Extract class name
        name = "UnknownClass"
        for child in node.children:
            if child.type == 'identifier':
                name = self._get_text(child)
                break

        # Extract super class (extends clause)
        super_class = None
        extends_found = False
        for i, child in enumerate(node.children):
            if self._get_text(child) == 'extends':
                extends_found = True
            elif extends_found and child.type == 'type':
                # Get the identifier from the type node
                for subchild in child.children:
                    if subchild.type == 'identifier':
                        super_class = Identifier(name=self._get_text(subchild))
                        break
                break

        # Extract implements clause
        implements = []
        implements_found = False
        for i, child in enumerate(node.children):
            if self._get_text(child) == 'implements':
                implements_found = True
            elif implements_found and child.type == 'type':
                # Get the identifier from the type node
                for subchild in child.children:
                    if subchild.type == 'identifier':
                        implements.append(Identifier(name=self._get_text(subchild)))

        # Extract class body members
        members = []
        body_node = next((c for c in node.children if c.type == 'class_body'), None)
        if body_node:
            for child in body_node.children:
                if child.type == 'property_declaration':
                    # Property declaration (no var/const keyword)
                    prop_decl = self.visit_property_declaration(child)
                    if prop_decl:
                        members.append(prop_decl)
                elif child.type == 'method_declaration':
                    # Method declaration (no function keyword)
                    method_decl = self.visit_method_declaration(child)
                    if method_decl:
                        members.append(method_decl)
                elif child.type == 'variable_declaration':
                    # Fallback: old-style variable declaration
                    var_decl = self.visit_variable_declaration(child)
                    if var_decl:
                        members.append(var_decl)
                elif child.type == 'function_declaration':
                    # Fallback: old-style function declaration
                    func_decl = self.visit_function_declaration(child)
                    if func_decl:
                        members.append(func_decl)
                elif child.type == 'constructor_declaration':
                    # Constructor
                    ctor = self.visit_constructor_declaration(child)
                    if ctor:
                        members.append(ctor)

        return ClassDeclaration(
            name=name,
            super_class=super_class,
            implements=implements,
            members=members,
            loc=self._make_location(node)
        )

    def visit_property_declaration(self, node) -> Optional[VariableDeclaration]:
        """Visit property_declaration node (class members without var/const)"""
        # Extract decorators
        decorators = []
        for child in node.children:
            if child.type == 'decorator_list':
                decorators = self.visit_decorator_list(child)
                break

        # Extract visibility
        visibility = None
        for child in node.children:
            if child.type == 'visibility':
                visibility = self._get_text(child.children[0])
                break

        # Extract name
        name = None
        for child in node.children:
            if child.type == 'identifier':
                name = self._get_text(child)
                break

        if not name:
            return None

        # Extract type annotation
        type_annotation = None
        type_node = node.child_by_field_name('type')
        if type_node:
            type_annotation = self._get_text(type_node)

        # Extract initializer
        initializer = None
        value_node = node.child_by_field_name('value')
        if value_node:
            initializer = self.visit_expression(value_node)

        return VariableDeclaration(
            name=name,
            var_type=type_annotation,
            initializer=initializer,
            is_const=False,  # Properties are mutable by default
            decorators=decorators,
            loc=self._make_location(node)
        )

    def visit_method_declaration(self, node) -> Optional[FunctionDeclaration]:
        """Visit method_declaration node (class methods without 'function' keyword)"""
        # Extract decorators
        decorators = []
        decorators_node = node.child_by_field_name('decorators')
        if decorators_node:
            decorators = self.visit_decorator_list(decorators_node)

        # Extract visibility
        visibility = None
        visibility_node = node.child_by_field_name('visibility')
        if visibility_node:
            visibility = self._get_text(visibility_node.children[0])

        # Check for async
        is_async = any(self._get_text(c) == 'async' for c in node.children if c.type == 'async')

        # Extract name
        name = None
        name_node = node.child_by_field_name('name')
        if name_node:
            name = self._get_text(name_node)

        if not name:
            return None

        # Extract parameters
        params = []
        params_node = node.child_by_field_name('parameters')
        if params_node:
            for child in params_node.children:
                if child.type == 'parameter':
                    param = self.visit_parameter(child)
                    if param:
                        params.append(param)

        # Extract return type
        return_type = None
        return_type_node = node.child_by_field_name('return_type')
        if return_type_node:
            return_type = self._get_text(return_type_node)

        # Extract body
        body = None
        body_node = node.child_by_field_name('body')
        if body_node:
            body = self.visit_block(body_node)

        return FunctionDeclaration(
            name=name,
            params=params,
            return_type=return_type,
            body=body,
            is_async=is_async,
            decorators=decorators,
            loc=self._make_location(node)
        )

    def visit_constructor_declaration(self, node) -> Optional[FunctionDeclaration]:
        """Visit constructor_declaration node"""
        # Extract visibility
        visibility = None
        for child in node.children:
            if child.type == 'visibility':
                visibility = self._get_text(child.children[0])
                break

        # Extract parameters
        params = []
        for child in node.children:
            if child.type == 'parameter_list':
                for param_child in child.children:
                    if param_child.type == 'parameter':
                        param = self.visit_parameter(param_child)
                        if param:
                            params.append(param)

        # Extract body
        body = None
        for child in node.children:
            if child.type == 'block':
                body = self.visit_block(child)
                break

        return FunctionDeclaration(
            name='constructor',
            params=params,
            return_type=None,
            body=body,
            is_async=False,
            decorators=[],
            loc=self._make_location(node)
        )

    def visit_interface_declaration(self, node) -> Optional[Statement]:
        return None

    def visit_trait_declaration(self, node) -> Optional[Statement]:
        return None
