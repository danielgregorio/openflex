#!/usr/bin/env python3
"""
Demo: Beautiful Error Messages in OpenFlex Neo
Shows off the new error formatting system
"""

from compiler.errors import create_parse_error, create_type_error
from compiler.parser.ast import SourceLocation

print("🎨 OpenFlex Neo - Beautiful Error Messages Demo")
print("=" * 60)
print()

# Example 1: Parse Error with Missing Semicolon
print("Example 1: Missing Semicolon")
print("-" * 60)

source1 = """function calculateTotal(items: Array): Number {
    var total = 0
    for (var i = 0; i < items.length; i++) {
        total += items[i].price;
    }
    return total;
}"""

error1 = create_parse_error(
    "Missing semicolon",
    source=source1,
    location=SourceLocation(
        file="shop.as4",
        line=2,
        column=18,
        end_line=2,
        end_column=19
    ),
    error_type="unexpected_token"
)

print(error1.format_error(use_color=True))
print()
print()

# Example 2: Type Error
print("Example 2: Type Mismatch")
print("-" * 60)

source2 = """var count: Number = 0;
var message: String = "Total: ";
var total: String = count + message;"""

error2 = create_type_error(
    "Cannot assign Number to String",
    source=source2,
    location=SourceLocation(
        file="counter.as4",
        line=3,
        column=21,
        end_line=3,
        end_column=37
    ),
    expected_type="String",
    actual_type="Number"
)

print(error2.format_error(use_color=True))
print()
print()

# Example 3: Undefined Variable
print("Example 3: Undefined Variable")
print("-" * 60)

source3 = """function increment(): void {
    count = count + 1;
    trace("Count: " + count);
}"""

error3 = create_parse_error(
    "Variable 'count' is not defined",
    source=source3,
    location=SourceLocation(
        file="app.as4",
        line=2,
        column=5,
        end_line=2,
        end_column=10
    ),
    error_type="undefined_variable"
)

print(error3.format_error(use_color=True))
print()
print()

# Example 4: Unexpected EOF
print("Example 4: Unexpected End of File")
print("-" * 60)

source4 = """class DataModel {
    var items: Array;

    function loadData(): void {
        items = fetchFromAPI();
"""

error4 = create_parse_error(
    "Unexpected end of file",
    source=source4,
    location=SourceLocation(
        file="model.as4",
        line=5,
        column=28,
        end_line=5,
        end_column=29
    ),
    error_type="unexpected_eof"
)

print(error4.format_error(use_color=True))
print()
print()

# Example 5: Invalid Import
print("Example 5: Import Not Found")
print("-" * 60)

source5 = """import com.company.InvalidClass;
import flash.utils.Timer;

class Application {
    // ...
}"""

error5 = create_parse_error(
    "Cannot find module 'com.company.InvalidClass'",
    source=source5,
    location=SourceLocation(
        file="main.as4",
        line=1,
        column=8,
        end_line=1,
        end_column=32
    ),
    error_type="import_not_found"
)

print(error5.format_error(use_color=True))
print()
print()

print("=" * 60)
print("✨ Helpful, beautiful error messages make development faster!")
