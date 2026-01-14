#!/usr/bin/env python3
"""
Direct compilation script - bypasses the fake CLI
"""

import sys
from pathlib import Path

# Import compiler modules directly
from compiler.parser.as4_parser import AS4Parser
from compiler.analyzer.type_checker import TypeChecker
from compiler.codegen.js_codegen import JSCodeGenerator

def compile_as4_file(input_file: str, output_file: str):
    """Compile an AS4 file to JavaScript"""

    print(f"🔨 Compiling: {input_file}")
    print(f"📄 Output: {output_file}\n")

    try:
        # Step 1: Parse
        print("1️⃣ Parsing ActionScript...")
        parser = AS4Parser()

        with open(input_file, 'r') as f:
            source_code = f.read()

        ast = parser.parse(source_code, input_file)
        print(f"   ✅ Parsed {len(source_code)} characters")

        # Step 2: Type Check
        print("2️⃣ Type checking...")
        type_checker = TypeChecker()
        type_checker.check_program(ast)

        if type_checker.errors:
            print(f"   ⚠️  Found {len(type_checker.errors)} type errors:")
            for error in type_checker.errors[:5]:  # Show first 5
                print(f"      - {error}")
            if len(type_checker.errors) > 5:
                print(f"      ... and {len(type_checker.errors) - 5} more")
        else:
            print("   ✅ No type errors")

        # Step 3: Generate Code
        print("3️⃣ Generating JavaScript...")
        codegen = JSCodeGenerator()
        js_code = codegen.generate(ast)
        print(f"   ✅ Generated {len(js_code)} characters of JavaScript")

        # Step 4: Write Output
        print("4️⃣ Writing output...")
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(js_code)

        print(f"   ✅ Written to {output_file}")

        print("\n✅ Compilation successful!")
        return True

    except Exception as e:
        print(f"\n❌ Compilation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compile-app.py <input.as4> <output.js>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    success = compile_as4_file(input_file, output_file)
    sys.exit(0 if success else 1)
