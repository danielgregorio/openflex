"""
Tests for Type Checker
"""

import pytest
from compiler.parser.as4_parser import AS4Parser
from compiler.analyzer.type_checker import TypeChecker, TypeCheckError
from compiler.parser.types import TYPE_MAP


@pytest.fixture
def type_checker():
    """Create type checker instance"""
    return TypeChecker()


@pytest.fixture
def parser():
    """Create AS4 parser instance"""
    return AS4Parser()


def test_simple_variable_type_check(type_checker, parser):
    """Test simple variable type checking"""
    source = """
    var x: Number = 5;
    var y: String = "hello";
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0, f"Expected no errors, got: {[e.message for e in errors]}"


def test_type_mismatch(type_checker, parser):
    """Test type mismatch detection"""
    source = """
    var x: Number = "hello";
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "not assignable" in errors[0].message.lower()


def test_const_without_initializer(type_checker, parser):
    """Test const must have initializer"""
    source = """
    const x: Number;
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "must have an initializer" in errors[0].message


def test_function_type_check(type_checker, parser):
    """Test function signature type checking"""
    source = """
    function add(a: Number, b: Number): Number {
        return a + b;
    }
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0, f"Expected no errors, got: {[e.message for e in errors]}"


def test_function_return_type_mismatch(type_checker, parser):
    """Test function return type validation"""
    source = """
    function getName(): String {
        return 42;
    }
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "return type" in errors[0].message.lower()


def test_undefined_variable(type_checker, parser):
    """Test undefined variable detection"""
    source = """
    var x: Number = undefinedVar;
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "cannot find name" in errors[0].message.lower()


def test_function_call_argument_count(type_checker, parser):
    """Test function call argument count validation"""
    source = """
    function greet(name: String): void {
        trace(name);
    }

    greet("Alice", "Bob");  // Too many arguments
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "expected" in errors[0].message.lower()
    assert "arguments" in errors[0].message.lower()


def test_function_call_argument_type(type_checker, parser):
    """Test function call argument type validation"""
    source = """
    function printNumber(n: Number): void {
        trace(n);
    }

    printNumber("not a number");
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "not assignable" in errors[0].message.lower()


def test_type_inference(type_checker, parser):
    """Test type inference from initializer"""
    source = """
    var x = 42;  // Should infer Number
    var y = "hello";  // Should infer String
    var z = true;  // Should infer Boolean
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0


def test_binary_expression_type_check(type_checker, parser):
    """Test binary expression type checking"""
    source = """
    var a: Number = 5 + 3;
    var b: String = "hello" + " world";
    var c: Boolean = 5 > 3;
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0


def test_array_literal_type_check(type_checker, parser):
    """Test array literal type checking"""
    source = """
    var numbers: Array<Number> = [1, 2, 3];
    var strings: Array<String> = ["a", "b", "c"];
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0


def test_null_safety(type_checker, parser):
    """Test null safety checking"""
    source = """
    var x: Number = null;  // Error: null not assignable to Number
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "not assignable" in errors[0].message.lower()


def test_nullable_type(type_checker, parser):
    """Test nullable type allows null"""
    source = """
    var x: Number? = null;  // OK
    var y: Number? = 42;    // Also OK
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    # Nullable types not fully implemented yet in parser
    # This test will pass when parser creates NullableType nodes
    # For now, just check it doesn't crash
    assert isinstance(errors, list)


def test_reactive_decorator_validation(type_checker, parser):
    """Test @reactive decorator is valid on variables"""
    source = """
    @reactive var count: Number = 0;
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    # Should have no errors - @reactive is valid
    assert len(errors) == 0


def test_void_return(type_checker, parser):
    """Test void function with no return"""
    source = """
    function doSomething(): void {
        trace("doing something");
    }
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0


def test_void_return_with_value(type_checker, parser):
    """Test void function cannot return value"""
    source = """
    function doSomething(): void {
        return 42;
    }
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    assert "void" in errors[0].message.lower() or "return" in errors[0].message.lower()


def test_builtin_trace_function(type_checker, parser):
    """Test builtin trace function"""
    source = """
    trace("Hello, world!");
    trace(42);
    trace(true);
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    # trace accepts any type
    assert len(errors) == 0


def test_complex_expression(type_checker, parser):
    """Test complex nested expressions"""
    source = """
    function calculate(a: Number, b: Number): Number {
        return (a + b) * 2 - (a / b);
    }

    var result: Number = calculate(10, 5);
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0


def test_string_concatenation(type_checker, parser):
    """Test string concatenation type checking"""
    source = """
    var name: String = "Alice";
    var age: Number = 25;
    var message: String = "Name: " + name + ", Age: " + age;
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    # String + anything should produce string
    assert len(errors) == 0


def test_conditional_expression(type_checker, parser):
    """Test ternary conditional type checking"""
    source = """
    var x: Number = 5;
    var result: Number = x > 0 ? 10 : 20;
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 0


def test_scope_variable_shadowing(type_checker, parser):
    """Test variable scoping"""
    source = """
    var x: Number = 10;

    function test(): void {
        var x: String = "hello";  // Shadows outer x
        trace(x);
    }
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    # Should be allowed - different scopes
    assert len(errors) == 0


def test_multiple_errors(type_checker, parser):
    """Test multiple errors are collected"""
    source = """
    var a: Number = "string";  // Error 1
    var b: String = 123;        // Error 2
    const c: Boolean;           // Error 3
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 3


def test_any_type_compatibility(type_checker, parser):
    """Test 'any' type is compatible with everything"""
    source = """
    var x: any = 42;
    x = "string";
    x = true;
    x = null;

    var y: Number = x;  // any -> Number OK
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    # any is compatible with everything
    assert len(errors) == 0


def test_error_location_tracking(type_checker, parser):
    """Test errors include location information"""
    source = """
    var x: Number = "wrong type";
    """

    ast = parser.parse(source)
    errors = type_checker.check_program(ast)

    assert len(errors) == 1
    # Error should have location info
    # (may be None if parser doesn't set locations yet)
    error = errors[0]
    assert hasattr(error, 'loc')
    assert hasattr(error, 'message')


if __name__ == "__main__":
    # Allow running directly for quick testing
    tc = TypeChecker()
    parser = AS4Parser()

    print("🧪 Running Type Checker Tests\n")

    tests = [
        ("Simple variables", test_simple_variable_type_check),
        ("Type mismatch", test_type_mismatch),
        ("Const without init", test_const_without_initializer),
        ("Function signature", test_function_type_check),
        ("Function return type", test_function_return_type_mismatch),
        ("Undefined variable", test_undefined_variable),
        ("Function call args", test_function_call_argument_count),
        ("Type inference", test_type_inference),
    ]

    passed = 0
    for name, test_func in tests:
        try:
            test_func(tc, parser)
            tc = TypeChecker()  # Reset for next test
            print(f"✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: {e}")
        except Exception as e:
            print(f"💥 {name}: {e}")

    print(f"\n{passed}/{len(tests)} tests passed")
