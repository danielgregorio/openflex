"""
AS4 Parser using Tree-sitter

This module provides a Python wrapper around the tree-sitter grammar
for ActionScript 4, converting tree-sitter parse trees into our AST.
"""

from typing import Optional, List, Any
from pathlib import Path
import os

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
    IfStatement, ForStatement, WhileStatement,
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

        # Build language if not exists
        if not lib_path.exists():
            print("Building tree-sitter grammar...")
            self._build_grammar(grammar_path, lib_path)

        # Load language
        try:
            self.language = Language(str(lib_path), "actionscript4")
            self.parser = TSParser()
            self.parser.set_language(self.language)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load tree-sitter grammar: {e}\n"
                f"Try running: cd {grammar_path} && tree-sitter generate && tree-sitter build"
            )

    def _build_grammar(self, grammar_path: Path, output_path: Path):
        """Build tree-sitter grammar"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            Language.build_library(
                str(output_path),
                [str(grammar_path)]
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to build grammar: {e}\n"
                f"Make sure tree-sitter CLI is installed: npm install -g tree-sitter-cli"
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
            'while_statement': self.visit_while_statement,
            'return_statement': self.visit_return_statement,
            'expression_statement': self.visit_expression_statement,
            'block': self.visit_block,
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

        # Extract type
        var_type = None
        type_node = node.child_by_field_name('type')
        if type_node:
            var_type = self.visit_type(type_node)

        # Extract initializer
        initializer = None
        init_node = node.child_by_field_name('value')
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
        if param_list:
            params = self.visit_parameter_list(param_list)

        # Extract return type
        return_type = None
        type_node = node.child_by_field_name('return_type')
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

        # Extract type
        param_type = None
        type_node = node.child_by_field_name('type')
        if type_node:
            param_type = self.visit_type(type_node)

        # Extract default value
        default_value = None
        default_node = node.child_by_field_name('default')
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
        if node.type == 'identifier':
            return Identifier(name=self._get_text(node), loc=self._make_location(node))

        elif node.type == 'number':
            text = self._get_text(node)
            return NumberLiteral(
                value=float(text),
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

        # More expression types to implement...
        return None

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
        # Extract test condition
        test = None
        test_node = node.child_by_field_name('condition')
        if test_node:
            test = self.visit_expression(test_node)

        # Extract consequent
        consequent = None
        then_node = node.child_by_field_name('consequence')
        if then_node:
            consequent = self.visit_statement(then_node)

        # Extract alternate (else)
        alternate = None
        else_node = node.child_by_field_name('alternative')
        if else_node:
            alternate = self.visit_statement(else_node)

        return IfStatement(
            test=test or Identifier(name="true"),  # Fallback
            consequent=consequent or BlockStatement(body=[]),
            alternate=alternate,
            loc=self._make_location(node)
        )

    def visit_for_statement(self, node) -> ForStatement:
        """Visit for_statement node - simplified"""
        return ForStatement(
            init=None,
            test=None,
            update=None,
            body=BlockStatement(body=[]),
            loc=self._make_location(node)
        )

    def visit_while_statement(self, node) -> WhileStatement:
        """Visit while_statement node - simplified"""
        test = Identifier(name="true")
        body = BlockStatement(body=[])
        return WhileStatement(test=test, body=body, loc=self._make_location(node))

    def visit_return_statement(self, node) -> ReturnStatement:
        """Visit return_statement node"""
        argument = None
        arg_node = node.child_by_field_name('argument')
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
        return None

    def visit_interface_declaration(self, node) -> Optional[Statement]:
        return None

    def visit_trait_declaration(self, node) -> Optional[Statement]:
        return None
