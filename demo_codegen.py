#!/usr/bin/env python3
"""
Demo: Code Generation
Demonstrates parsing AS4 and generating JavaScript
"""

from pathlib import Path
from compiler.parser.as4_parser import AS4Parser
from compiler.codegen.js_codegen import JSCodeGenerator


def main():
    # Read hello-world example
    example_file = Path("examples/hello-world.as4")

    if not example_file.exists():
        print(f"❌ Example file not found: {example_file}")
        return

    print("=" * 60)
    print("OpenFlex Neo - Code Generation Demo")
    print("=" * 60)
    print()

    # Read source
    source = example_file.read_text()
    print("📄 Input AS4 code:")
    print("-" * 60)
    print(source)
    print("-" * 60)
    print()

    # Parse
    print("🔍 Parsing AS4...")
    parser = AS4Parser()
    ast = parser.parse(source, str(example_file))
    print(f"✅ Parsed successfully! Found {len(ast.declarations)} declarations")
    print()

    # Generate JavaScript
    print("⚙️  Generating JavaScript...")
    codegen = JSCodeGenerator()
    js_code = codegen.generate(ast)
    print("✅ Generated successfully!")
    print()

    # Output
    print("📄 Output JavaScript:")
    print("-" * 60)
    print(js_code)
    print("-" * 60)
    print()

    # Write output file
    output_file = Path("examples/hello-world.js")
    output_file.write_text(js_code)
    print(f"💾 Saved to: {output_file}")
    print()

    print("✨ Code generation complete!")


if __name__ == "__main__":
    main()
