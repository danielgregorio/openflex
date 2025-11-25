"""
OpenFlex AST (Abstract Syntax Tree) Definitions

This module defines all AST node types for ActionScript 4.
Inspired by TypeScript AST and Rust's HIR (High-level IR).
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Any
from enum import Enum


# ============================================================================
# Base Types
# ============================================================================

@dataclass
class SourceLocation:
    """Location in source code for error reporting"""
    file: str
    line: int
    column: int
    end_line: int
    end_column: int


class ASTNode:
    """Base class for all AST nodes"""
    pass


# ============================================================================
# Decorators (for @reactive, @computed, @effect)
# ============================================================================

@dataclass
class Decorator(ASTNode):
    """Decorator: @reactive, @computed, @effect, etc"""
    name: str
    arguments: List['Expression'] = field(default_factory=list)
    loc: Optional[SourceLocation] = None


# ============================================================================
# Conditional Compilation (#if blocks)
# ============================================================================

@dataclass
class ConditionalCompilation(ASTNode):
    """Conditional compilation block: #if FLAG ... #endif"""
    condition: 'ConditionExpression'
    then_block: List['Statement']
    elif_blocks: List['ElifBlock'] = field(default_factory=list)
    else_block: Optional[List['Statement']] = None
    loc: Optional[SourceLocation] = None


@dataclass
class ElifBlock(ASTNode):
    """#elif block"""
    condition: 'ConditionExpression'
    block: List['Statement']
    loc: Optional[SourceLocation] = None


@dataclass
class ConditionExpression(ASTNode):
    """Condition expression for #if: FLAG, !FLAG, (A && B), etc"""
    loc: Optional[SourceLocation] = None


@dataclass
class ConditionIdentifier:
    """Simple flag: WEB, MOBILE, DEBUG"""
    name: str
    loc: Optional[SourceLocation] = None


@dataclass
class ConditionNot:
    """NOT condition: !FLAG"""
    operand: 'ConditionExpression'
    loc: Optional[SourceLocation] = None


@dataclass
class ConditionAnd:
    """AND condition: A && B"""
    left: 'ConditionExpression'
    right: 'ConditionExpression'
    loc: Optional[SourceLocation] = None


@dataclass
class ConditionOr:
    """OR condition: A || B"""
    left: 'ConditionExpression'
    right: 'ConditionExpression'
    loc: Optional[SourceLocation] = None


# ============================================================================
# Types
# ============================================================================

class TypeKind(Enum):
    """Type categories"""
    PRIMITIVE = "primitive"
    CLASS = "class"
    INTERFACE = "interface"
    FUNCTION = "function"
    ARRAY = "array"
    GENERIC = "generic"
    UNION = "union"
    NULLABLE = "nullable"
    ANY = "any"
    VOID = "void"


@dataclass
class Type(ASTNode):
    """Base type class"""
    kind: TypeKind = None
    name: str = ""
    loc: Optional[SourceLocation] = None


@dataclass
class PrimitiveType(Type):
    """Primitive types: Number, String, Boolean, etc"""
    pass


@dataclass
class ArrayType(Type):
    """Array<T> type"""
    element_type: Optional[Type] = None

    def __post_init__(self):
        if self.element_type:
            self.kind = TypeKind.ARRAY
            self.name = f"Array<{self.element_type.name}>"


@dataclass
class FunctionType(Type):
    """Function type: (params) => return_type"""
    param_types: List[Type] = field(default_factory=list)
    return_type: Optional[Type] = None

    def __post_init__(self):
        self.kind = TypeKind.FUNCTION


@dataclass
class UnionType(Type):
    """Union type: T | U"""
    types: List[Type] = field(default_factory=list)

    def __post_init__(self):
        self.kind = TypeKind.UNION
        if self.types:
            self.name = " | ".join(t.name for t in self.types)


@dataclass
class NullableType(Type):
    """Nullable type: T?"""
    base_type: Optional[Type] = None

    def __post_init__(self):
        self.kind = TypeKind.NULLABLE
        if self.base_type:
            self.name = f"{self.base_type.name}?"


@dataclass
class GenericType(Type):
    """Generic type: Map<K, V>"""
    base: Optional[Type] = None
    type_params: List[Type] = field(default_factory=list)

    def __post_init__(self):
        self.kind = TypeKind.GENERIC
        params = ", ".join(t.name for t in self.type_params)
        self.name = f"{self.base.name}<{params}>"


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class Expression(ASTNode):
    """Base expression class"""
    pass


@dataclass
class Identifier(Expression):
    """Variable/function name"""
    name: str
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class Literal(Expression):
    """Literal value"""
    value: Any
    raw: str
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class NumberLiteral(Literal):
    """Number literal: 42, 3.14"""
    pass


@dataclass
class StringLiteral(Literal):
    """String literal: "hello", 'world'"""
    pass


@dataclass
class BooleanLiteral(Literal):
    """Boolean literal: true, false"""
    pass


@dataclass
class NullLiteral(Literal):
    """null literal"""
    def __post_init__(self):
        self.value = None


@dataclass
class ArrayLiteral(Expression):
    """Array literal: [1, 2, 3]"""
    elements: List[Expression]
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class ObjectLiteral(Expression):
    """Object literal: { name: "Alice", age: 30 }"""
    properties: List['Property']
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class Property(ASTNode):
    """Object property"""
    key: Union[Identifier, StringLiteral]
    value: Expression
    is_computed: bool = False  # { [key]: value }
    loc: Optional[SourceLocation] = None


@dataclass
class BinaryExpression(Expression):
    """Binary operation: a + b, x > y"""
    operator: str
    left: Expression
    right: Expression
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class UnaryExpression(Expression):
    """Unary operation: -x, !flag, ++i"""
    operator: str
    operand: Expression
    is_prefix: bool = True
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class CallExpression(Expression):
    """Function call: foo(1, 2)"""
    callee: Expression
    arguments: List[Expression]
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class MemberExpression(Expression):
    """Member access: obj.prop, arr[0]"""
    object: Expression
    property: Expression
    is_computed: bool = False  # arr[0] vs obj.prop
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class ConditionalExpression(Expression):
    """Ternary: condition ? true_expr : false_expr"""
    test: Expression
    consequent: Expression
    alternate: Expression
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class ArrowFunction(Expression):
    """Arrow function: (x) => x * 2"""
    params: List['Parameter']
    body: Union[Expression, 'BlockStatement']
    is_async: bool = False
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class AwaitExpression(Expression):
    """Await expression: await promise"""
    argument: Expression
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class NewExpression(Expression):
    """New expression: new User("Alice")"""
    callee: Expression
    arguments: List[Expression]
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


@dataclass
class TemplateString(Expression):
    """Template string: `Hello ${name}`"""
    parts: List[Union[StringLiteral, Expression]]
    type: Optional[Type] = None
    loc: Optional[SourceLocation] = None


# ============================================================================
# Statements
# ============================================================================

@dataclass
class Statement(ASTNode):
    """Base statement class"""
    pass


@dataclass
class BlockStatement(Statement):
    """Block: { ... }"""
    body: List[Statement]
    loc: Optional[SourceLocation] = None


@dataclass
class ExpressionStatement(Statement):
    """Expression as statement"""
    expression: Expression
    loc: Optional[SourceLocation] = None


@dataclass
class VariableDeclaration(Statement):
    """Variable declaration: var x: Number = 5"""
    name: str
    var_type: Optional[Type]
    initializer: Optional[Expression]
    is_const: bool = False
    is_bindable: bool = False  # [Bindable] metadata (deprecated, use @reactive)
    decorators: List[Decorator] = field(default_factory=list)  # @reactive, @computed, etc
    visibility: str = "public"  # public, private, protected
    is_static: bool = False
    loc: Optional[SourceLocation] = None


@dataclass
class FunctionDeclaration(Statement):
    """Function declaration"""
    name: str
    params: List['Parameter']
    return_type: Optional[Type]
    body: BlockStatement
    is_async: bool = False
    visibility: str = "public"  # public, private, protected
    is_static: bool = False
    decorators: List[Decorator] = field(default_factory=list)  # @effect, etc
    loc: Optional[SourceLocation] = None


@dataclass
class Parameter(ASTNode):
    """Function parameter"""
    name: str
    param_type: Optional[Type]
    default_value: Optional[Expression] = None
    is_rest: bool = False  # ...args
    loc: Optional[SourceLocation] = None


@dataclass
class ReturnStatement(Statement):
    """Return statement"""
    argument: Optional[Expression]
    loc: Optional[SourceLocation] = None


@dataclass
class IfStatement(Statement):
    """If statement"""
    test: Expression
    consequent: Statement
    alternate: Optional[Statement] = None
    loc: Optional[SourceLocation] = None


@dataclass
class WhileStatement(Statement):
    """While loop"""
    test: Expression
    body: Statement
    loc: Optional[SourceLocation] = None


@dataclass
class ForStatement(Statement):
    """For loop"""
    init: Optional[Union[VariableDeclaration, Expression]]
    test: Optional[Expression]
    update: Optional[Expression]
    body: Statement
    loc: Optional[SourceLocation] = None


@dataclass
class ForInStatement(Statement):
    """For-in loop: for (key in obj)"""
    left: Union[VariableDeclaration, Identifier]
    right: Expression
    body: Statement
    loc: Optional[SourceLocation] = None


@dataclass
class ForOfStatement(Statement):
    """For-of loop: for (item of array)"""
    left: Union[VariableDeclaration, Identifier]
    right: Expression
    body: Statement
    loc: Optional[SourceLocation] = None


@dataclass
class BreakStatement(Statement):
    """Break statement"""
    label: Optional[str] = None


@dataclass
class ContinueStatement(Statement):
    """Continue statement"""
    label: Optional[str] = None


@dataclass
class ThrowStatement(Statement):
    """Throw statement"""
    argument: Expression


@dataclass
class TryStatement(Statement):
    """Try-catch-finally"""
    block: BlockStatement
    handler: Optional['CatchClause'] = None
    finalizer: Optional[BlockStatement] = None
    loc: Optional[SourceLocation] = None


@dataclass
class CatchClause(ASTNode):
    """Catch clause"""
    param: Optional[str]
    param_type: Optional[Type]
    body: BlockStatement
    loc: Optional[SourceLocation] = None


@dataclass
class MatchStatement(Statement):
    """Pattern matching (AS4 extension)"""
    discriminant: Expression
    cases: List['MatchCase']


@dataclass
class MatchCase(ASTNode):
    """Match case"""
    pattern: 'Pattern'
    body: Statement


@dataclass
class Pattern(ASTNode):
    """Pattern for matching"""
    pass


# ============================================================================
# Declarations
# ============================================================================

@dataclass
class ImportDeclaration(Statement):
    """Import statement: import { foo } from "module" """
    specifiers: List['ImportSpecifier']
    source: str


@dataclass
class ImportSpecifier(ASTNode):
    """Import specifier"""
    imported: str
    local: str


@dataclass
class ClassDeclaration(Statement):
    """Class declaration"""
    name: str
    super_class: Optional[Identifier]
    implements: List[Identifier]
    members: List[Union['PropertyDeclaration', FunctionDeclaration]]
    type_parameters: List['TypeParameter'] = field(default_factory=list)


@dataclass
class PropertyDeclaration(Statement):
    """Class property"""
    name: str
    prop_type: Optional[Type]
    initializer: Optional[Expression]
    visibility: str = "public"
    is_static: bool = False
    is_readonly: bool = False
    is_bindable: bool = False


@dataclass
class InterfaceDeclaration(Statement):
    """Interface declaration"""
    name: str
    extends: List[Identifier]
    members: List['InterfaceMember']
    type_parameters: List['TypeParameter'] = field(default_factory=list)


@dataclass
class InterfaceMember(ASTNode):
    """Interface member"""
    name: str
    member_type: Type


@dataclass
class TypeParameter(ASTNode):
    """Generic type parameter: <T extends Foo>"""
    name: str
    constraint: Optional[Type] = None
    default: Optional[Type] = None


@dataclass
class TraitDeclaration(Statement):
    """Trait declaration (AS4 extension)"""
    name: str
    members: List[Union[FunctionDeclaration, PropertyDeclaration]]


# ============================================================================
# Program
# ============================================================================

@dataclass
class Program(ASTNode):
    """Root AST node"""
    imports: List[ImportDeclaration]
    declarations: List[Statement]
    source_file: str
    loc: Optional[SourceLocation] = None
