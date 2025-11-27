#!/usr/bin/env python3
"""
OpenFlex Neo - MXML Compiler
Compiles MXML files to Web Components with Reactivity
"""

import sys
import os
from compiler.enhanced_mxml_compiler import EnhancedMXMLCompiler


def main():
    if len(sys.argv) < 2:
        print("Usage: python compile-mxml.py <input.mxml> [output.js]")
        print()
        print("Example:")
        print("  python compile-mxml.py examples/simple.mxml examples/simple-component.js")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Auto-generate output filename
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}-component.js"

    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    print(f"🚀 OpenFlex Neo MXML Compiler")
    print(f"   Input:  {input_file}")
    print(f"   Output: {output_file}")
    print()

    # Read MXML source
    with open(input_file, 'r') as f:
        mxml_source = f.read()

    # Compile
    compiler = EnhancedMXMLCompiler()
    try:
        js_output = compiler.compile(mxml_source, input_file)

        # Write output
        with open(output_file, 'w') as f:
            f.write(js_output)

        print(f"✅ Compilation successful!")
        print(f"   Generated {len(js_output)} bytes of JavaScript")
        print()
        print("To use in browser:")
        print(f"  1. Include runtime: <script src='runtime/openflex-runtime-browser.js'></script>")
        print(f"  2. Include component: <script src='{output_file}'></script>")
        print(f"  3. Use element: <app-root></app-root>")

    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
