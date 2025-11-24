"""
OpenFlex Type System - Built-in Types

Defines all primitive types and type utilities.
"""

from .ast import Type, TypeKind, PrimitiveType, ArrayType, UnionType, NullableType


# ============================================================================
# Primitive Types
# ============================================================================

class BuiltinTypes:
    """Built-in primitive types"""

    # Numeric types
    NUMBER = PrimitiveType(kind=TypeKind.PRIMITIVE, name="Number")
    INT = PrimitiveType(kind=TypeKind.PRIMITIVE, name="int")
    UINT = PrimitiveType(kind=TypeKind.PRIMITIVE, name="uint")

    # String and Boolean
    STRING = PrimitiveType(kind=TypeKind.PRIMITIVE, name="String")
    BOOLEAN = PrimitiveType(kind=TypeKind.PRIMITIVE, name="Boolean")

    # Special types
    VOID = PrimitiveType(kind=TypeKind.VOID, name="void")
    ANY = PrimitiveType(kind=TypeKind.ANY, name="any")
    NULL = PrimitiveType(kind=TypeKind.PRIMITIVE, name="null")
    UNDEFINED = PrimitiveType(kind=TypeKind.PRIMITIVE, name="undefined")

    # Object types
    OBJECT = PrimitiveType(kind=TypeKind.PRIMITIVE, name="Object")
    ARRAY = PrimitiveType(kind=TypeKind.PRIMITIVE, name="Array")
    FUNCTION = PrimitiveType(kind=TypeKind.PRIMITIVE, name="Function")

    # Collections
    MAP = PrimitiveType(kind=TypeKind.CLASS, name="Map")
    SET = PrimitiveType(kind=TypeKind.CLASS, name="Set")

    # Promise (for async)
    PROMISE = PrimitiveType(kind=TypeKind.CLASS, name="Promise")


# Map from type name to Type object
TYPE_MAP = {
    "Number": BuiltinTypes.NUMBER,
    "int": BuiltinTypes.INT,
    "uint": BuiltinTypes.UINT,
    "String": BuiltinTypes.STRING,
    "Boolean": BuiltinTypes.BOOLEAN,
    "void": BuiltinTypes.VOID,
    "any": BuiltinTypes.ANY,
    "Object": BuiltinTypes.OBJECT,
    "Array": BuiltinTypes.ARRAY,
    "Function": BuiltinTypes.FUNCTION,
    "Map": BuiltinTypes.MAP,
    "Set": BuiltinTypes.SET,
    "Promise": BuiltinTypes.PROMISE,
}


def get_type(name: str) -> Type:
    """Get built-in type by name"""
    return TYPE_MAP.get(name, BuiltinTypes.ANY)


def is_numeric(type: Type) -> bool:
    """Check if type is numeric"""
    return type.name in ("Number", "int", "uint")


def is_assignable(source: Type, target: Type) -> bool:
    """Check if source type can be assigned to target type"""

    # any is compatible with everything
    if target.kind == TypeKind.ANY or source.kind == TypeKind.ANY:
        return True

    # Same type
    if source.name == target.name:
        return True

    # Numeric types are compatible
    if is_numeric(source) and is_numeric(target):
        return True

    # Nullable types
    if target.kind == TypeKind.NULLABLE:
        return is_assignable(source, target.base_type)

    # Union types
    if target.kind == TypeKind.UNION:
        return any(is_assignable(source, t) for t in target.types)

    # TODO: Check subtyping, interfaces, etc

    return False


def make_nullable(type: Type) -> NullableType:
    """Make a type nullable: T -> T?"""
    return NullableType(kind=TypeKind.NULLABLE, name=f"{type.name}?", base_type=type)


def make_array(element_type: Type) -> ArrayType:
    """Make an array type: T -> Array<T>"""
    return ArrayType(
        kind=TypeKind.ARRAY,
        name=f"Array<{element_type.name}>",
        element_type=element_type
    )


def make_union(types: list[Type]) -> UnionType:
    """Make a union type: T | U | V"""
    return UnionType(
        kind=TypeKind.UNION,
        name=" | ".join(t.name for t in types),
        types=types
    )
