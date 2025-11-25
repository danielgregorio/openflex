"""
Type Checker for ActionScript 4 (OpenFlex Neo)

Validates types, null safety, and semantic correctness.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

from compiler.parser.ast import *
from compiler.parser.types import BuiltinTypes, TYPE_MAP


class TypeCheckError(Exception):
    """Type checking error with location information"""

    def __init__(self, message: str, loc: Optional[SourceLocation] = None):
        self.message = message
        self.loc = loc
        super().__init__(self._format_message())

    def _format_message(self):
        if self.loc:
            return f"{self.loc.file}:{self.loc.line}:{self.loc.column}: {self.message}"
        return self.message


@dataclass
class TypeEnvironment:
    """Type environment for tracking variable and function types"""

    # Variable types
    variables: Dict[str, Type] = field(default_factory=dict)

    # Function signatures
    functions: Dict[str, FunctionType] = field(default_factory=dict)

    # Class/interface types
    classes: Dict[str, Type] = field(default_factory=dict)

    # Parent scope
    parent: Optional['TypeEnvironment'] = None

    def lookup_variable(self, name: str) -> Optional[Type]:
        """Look up variable type in this scope or parent scopes"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.lookup_variable(name)
        return None

    def lookup_function(self, name: str) -> Optional[FunctionType]:
        """Look up function type"""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.lookup_function(name)
        return None

    def define_variable(self, name: str, type: Type):
        """Define a variable in this scope"""
        self.variables[name] = type

    def define_function(self, name: str, type: FunctionType):
        """Define a function in this scope"""
        self.functions[name] = type

    def create_child_scope(self) -> 'TypeEnvironment':
        """Create a child scope"""
        return TypeEnvironment(parent=self)


class TypeChecker:
    """Type checker for AS4 code"""

    def __init__(self):
        self.env = TypeEnvironment()
        self.errors: List[TypeCheckError] = []
        self.current_function_return_type: Optional[Type] = None

        # Initialize builtin types
        self._init_builtins()

    def _init_builtins(self):
        """Initialize builtin types and functions"""
        # Builtin types are already in TYPE_MAP
        # Add builtin functions like trace, etc.
        trace_type = FunctionType(
            param_types=[TYPE_MAP['any']],
            return_type=TYPE_MAP['void']
        )
        self.env.define_function('trace', trace_type)

    def check_program(self, program: Program) -> List[TypeCheckError]:
        """Type check entire program, return errors"""
        self.errors = []

        try:
            # Check imports
            for import_decl in program.imports:
                self._check_import(import_decl)

            # Check declarations
            for decl in program.declarations:
                self._check_statement(decl)

        except TypeCheckError as e:
            self.errors.append(e)

        return self.errors

    def _check_import(self, import_decl: ImportDeclaration):
        """Check import statement"""
        # For now, just record imported types
        # TODO: Load type information from imported modules
        pass

    def _check_statement(self, stmt: Statement):
        """Type check a statement"""
        if isinstance(stmt, VariableDeclaration):
            self._check_variable_declaration(stmt)
        elif isinstance(stmt, FunctionDeclaration):
            self._check_function_declaration(stmt)
        elif isinstance(stmt, ClassDeclaration):
            self._check_class_declaration(stmt)
        elif isinstance(stmt, ExpressionStatement):
            self._check_expression(stmt.expression)
        elif isinstance(stmt, ReturnStatement):
            self._check_return_statement(stmt)
        elif isinstance(stmt, IfStatement):
            self._check_if_statement(stmt)
        elif isinstance(stmt, BlockStatement):
            self._check_block_statement(stmt)
        # Add more statement types as needed

    def _check_variable_declaration(self, var_decl: VariableDeclaration):
        """Type check variable declaration"""
        # Check decorators
        self._check_decorators(var_decl.decorators, ['reactive', 'computed'])

        # Infer or validate type
        if var_decl.var_type:
            var_type = var_decl.var_type
        elif var_decl.initializer:
            # Type inference
            var_type = self._infer_type(var_decl.initializer)
        else:
            var_type = TYPE_MAP['any']

        # Check initializer type matches declaration
        if var_decl.initializer:
            init_type = self._check_expression(var_decl.initializer)
            if not self._is_assignable(var_type, init_type):
                self._error(
                    f"Type '{self._type_name(init_type)}' is not assignable to type '{self._type_name(var_type)}'",
                    var_decl.loc
                )

        # Check const has initializer
        if var_decl.is_const and not var_decl.initializer:
            self._error(
                f"Const variable '{var_decl.name}' must have an initializer",
                var_decl.loc
            )

        # Register variable
        self.env.define_variable(var_decl.name, var_type)

    def _check_function_declaration(self, func_decl: FunctionDeclaration):
        """Type check function declaration"""
        # Create function type
        param_types = [p.param_type or TYPE_MAP['any'] for p in func_decl.params]
        return_type = func_decl.return_type or TYPE_MAP['void']

        func_type = FunctionType(
            param_types=param_types,
            return_type=return_type
        )

        # Register function
        self.env.define_function(func_decl.name, func_type)

        # Check body in new scope
        child_env = self.env.create_child_scope()
        prev_env = self.env
        prev_return_type = self.current_function_return_type

        self.env = child_env
        self.current_function_return_type = return_type

        # Register parameters
        for param in func_decl.params:
            param_type = param.param_type or TYPE_MAP['any']
            self.env.define_variable(param.name, param_type)

        # Check body
        self._check_block_statement(func_decl.body)

        self.env = prev_env
        self.current_function_return_type = prev_return_type

    def _check_class_declaration(self, class_decl: ClassDeclaration):
        """Type check class declaration"""
        # TODO: Implement class type checking
        pass

    def _check_return_statement(self, return_stmt: ReturnStatement):
        """Type check return statement"""
        if not self.current_function_return_type:
            self._error("Return statement outside function", return_stmt.loc)
            return

        if return_stmt.argument:
            return_type = self._check_expression(return_stmt.argument)

            if not self._is_assignable(self.current_function_return_type, return_type):
                self._error(
                    f"Return type '{self._type_name(return_type)}' is not assignable to "
                    f"function return type '{self._type_name(self.current_function_return_type)}'",
                    return_stmt.loc
                )
        else:
            # void return
            if self.current_function_return_type.kind != TypeKind.VOID:
                self._error(
                    f"Function expects return type '{self._type_name(self.current_function_return_type)}', "
                    f"but got void return",
                    return_stmt.loc
                )

    def _check_if_statement(self, if_stmt: IfStatement):
        """Type check if statement"""
        # Check condition is boolean
        test_type = self._check_expression(if_stmt.test)
        # Allow any truthy value for now

        # Check branches
        self._check_statement(if_stmt.consequent)
        if if_stmt.alternate:
            self._check_statement(if_stmt.alternate)

    def _check_block_statement(self, block: BlockStatement):
        """Type check block statement"""
        for stmt in block.body:
            self._check_statement(stmt)

    def _check_expression(self, expr: Expression) -> Type:
        """Type check expression and return its type"""
        if isinstance(expr, Literal):
            return self._check_literal(expr)
        elif isinstance(expr, Identifier):
            return self._check_identifier(expr)
        elif isinstance(expr, BinaryExpression):
            return self._check_binary_expression(expr)
        elif isinstance(expr, UnaryExpression):
            return self._check_unary_expression(expr)
        elif isinstance(expr, CallExpression):
            return self._check_call_expression(expr)
        elif isinstance(expr, MemberExpression):
            return self._check_member_expression(expr)
        elif isinstance(expr, ArrayLiteral):
            return self._check_array_literal(expr)
        elif isinstance(expr, ObjectLiteral):
            return self._check_object_literal(expr)
        elif isinstance(expr, ConditionalExpression):
            return self._check_conditional_expression(expr)
        else:
            # Unknown expression type
            return TYPE_MAP['any']

    def _check_literal(self, literal: Literal) -> Type:
        """Type check literal"""
        if isinstance(literal, NumberLiteral):
            return TYPE_MAP['Number']
        elif isinstance(literal, StringLiteral):
            return TYPE_MAP['String']
        elif isinstance(literal, BooleanLiteral):
            return TYPE_MAP['Boolean']
        elif isinstance(literal, NullLiteral):
            # null is a special case - lowercase in TYPE_MAP
            return TYPE_MAP.get('null', TYPE_MAP['any'])
        return TYPE_MAP['any']

    def _check_identifier(self, ident: Identifier) -> Type:
        """Type check identifier"""
        var_type = self.env.lookup_variable(ident.name)
        if not var_type:
            self._error(f"Cannot find name '{ident.name}'", ident.loc)
            return TYPE_MAP['any']
        return var_type

    def _check_binary_expression(self, binary: BinaryExpression) -> Type:
        """Type check binary expression"""
        left_type = self._check_expression(binary.left)
        right_type = self._check_expression(binary.right)

        # Arithmetic operators
        if binary.operator in ['+', '-', '*', '/', '%', '**']:
            if binary.operator == '+':
                # String concatenation or number addition
                if left_type.name == 'String' or right_type.name == 'String':
                    return TYPE_MAP['String']
            return TYPE_MAP['Number']

        # Comparison operators
        elif binary.operator in ['<', '<=', '>', '>=', '==', '!=', '===', '!==']:
            return TYPE_MAP['Boolean']

        # Logical operators
        elif binary.operator in ['&&', '||']:
            return TYPE_MAP['Boolean']

        # Assignment
        elif binary.operator == '=':
            if not self._is_assignable(left_type, right_type):
                self._error(
                    f"Type '{self._type_name(right_type)}' is not assignable to "
                    f"type '{self._type_name(left_type)}'",
                    binary.loc
                )
            return left_type

        return TYPE_MAP['any']

    def _check_unary_expression(self, unary: UnaryExpression) -> Type:
        """Type check unary expression"""
        operand_type = self._check_expression(unary.operand)

        if unary.operator in ['+', '-', '++', '--']:
            return TYPE_MAP['Number']
        elif unary.operator == '!':
            return TYPE_MAP['Boolean']
        elif unary.operator == 'typeof':
            return TYPE_MAP['String']

        return TYPE_MAP['any']

    def _check_call_expression(self, call: CallExpression) -> Type:
        """Type check function call"""
        # Get callee type
        if isinstance(call.callee, Identifier):
            func_type = self.env.lookup_function(call.callee.name)
            if not func_type:
                self._error(f"Cannot find function '{call.callee.name}'", call.loc)
                return TYPE_MAP['any']

            # Check argument count
            if len(call.arguments) != len(func_type.param_types):
                self._error(
                    f"Expected {len(func_type.param_types)} arguments, "
                    f"but got {len(call.arguments)}",
                    call.loc
                )

            # Check argument types
            for i, (arg, param_type) in enumerate(zip(call.arguments, func_type.param_types)):
                arg_type = self._check_expression(arg)
                if not self._is_assignable(param_type, arg_type):
                    self._error(
                        f"Argument {i+1}: Type '{self._type_name(arg_type)}' is not assignable to "
                        f"parameter type '{self._type_name(param_type)}'",
                        call.loc
                    )

            return func_type.return_type
        else:
            # Method call or complex callee
            return TYPE_MAP['any']

    def _check_member_expression(self, member: MemberExpression) -> Type:
        """Type check member access"""
        obj_type = self._check_expression(member.object)
        # TODO: Implement proper member type checking with class/interface types
        return TYPE_MAP['any']

    def _check_array_literal(self, array: ArrayLiteral) -> Type:
        """Type check array literal"""
        if not array.elements:
            return ArrayType(element_type=TYPE_MAP['any'])

        # Infer element type from first element
        element_type = self._check_expression(array.elements[0])

        # Check all elements have compatible type
        for elem in array.elements[1:]:
            elem_type = self._check_expression(elem)
            if not self._is_assignable(element_type, elem_type):
                # Mixed types, use any
                element_type = TYPE_MAP['any']
                break

        return ArrayType(element_type=element_type)

    def _check_object_literal(self, obj: ObjectLiteral) -> Type:
        """Type check object literal"""
        # TODO: Create object type from properties
        return TYPE_MAP['object']

    def _check_conditional_expression(self, cond: ConditionalExpression) -> Type:
        """Type check ternary expression"""
        self._check_expression(cond.test)
        consequent_type = self._check_expression(cond.consequent)
        alternate_type = self._check_expression(cond.alternate)

        # Return common type
        if self._types_equal(consequent_type, alternate_type):
            return consequent_type

        return TYPE_MAP['any']

    def _check_decorators(self, decorators: List[Decorator], allowed: List[str]):
        """Check decorators are valid"""
        for decorator in decorators:
            if decorator.name not in allowed and decorator.name not in ['reactive', 'computed', 'effect']:
                self._error(f"Unknown decorator '@{decorator.name}'")

    def _infer_type(self, expr: Expression) -> Type:
        """Infer type from expression"""
        return self._check_expression(expr)

    def _is_assignable(self, target: Type, source: Type) -> bool:
        """Check if source type is assignable to target type"""
        # any is assignable to/from anything
        if target.kind == TypeKind.ANY or source.kind == TypeKind.ANY:
            return True

        # Exact type match
        if self._types_equal(target, source):
            return True

        # null is assignable to nullable types
        if source.name == 'null':
            return isinstance(target, NullableType) or target.kind == TypeKind.ANY

        # Nullable type handling
        if isinstance(target, NullableType):
            return self._is_assignable(target.base_type, source)

        # Primitive type matching by name
        if target.kind == TypeKind.PRIMITIVE and source.kind == TypeKind.PRIMITIVE:
            return target.name == source.name

        return False

    def _types_equal(self, type1: Type, type2: Type) -> bool:
        """Check if two types are equal"""
        if type1.kind != type2.kind:
            return False

        if isinstance(type1, ArrayType) and isinstance(type2, ArrayType):
            return self._types_equal(type1.element_type, type2.element_type)

        if isinstance(type1, NullableType) and isinstance(type2, NullableType):
            return self._types_equal(type1.base_type, type2.base_type)

        if isinstance(type1, UnionType) and isinstance(type2, UnionType):
            return set(t.name for t in type1.types) == set(t.name for t in type2.types)

        return type1.name == type2.name

    def _type_name(self, type: Type) -> str:
        """Get human-readable type name"""
        if isinstance(type, ArrayType):
            return f"Array<{self._type_name(type.element_type)}>"
        if isinstance(type, NullableType):
            return f"{self._type_name(type.base_type)}?"
        if isinstance(type, UnionType):
            return " | ".join(self._type_name(t) for t in type.types)
        return type.name

    def _error(self, message: str, loc: Optional[SourceLocation] = None):
        """Record a type error"""
        error = TypeCheckError(message, loc)
        self.errors.append(error)
        if len(self.errors) > 100:  # Prevent infinite errors
            raise TypeCheckError("Too many type errors")
