#!/usr/bin/env python3
"""Debug script to inspect AST structure"""

from compiler.parser.as4_parser import AS4Parser
import json

def inspect_ast(input_file: str):
    """Parse and print AST structure"""

    print(f"🔍 Parsing: {input_file}\n")

    parser = AS4Parser()
    with open(input_file, 'r') as f:
        source_code = f.read()

    ast = parser.parse(source_code, input_file)

    print(f"Program has {len(ast.declarations)} top-level declarations:\n")

    for i, decl in enumerate(ast.declarations[:20]):  # Show first 20
        print(f"{i+1:3}. {decl.__class__.__name__:30} ", end="")

        if hasattr(decl, 'name'):
            print(f"name='{decl.name}'", end="")

        if isinstance(decl, type(ast.declarations[0]).__bases__[0]) and hasattr(decl, 'members'):
            print(f" ({len(decl.members)} members)", end="")

        # Show type annotation if present
        if hasattr(decl, 'type_annotation') and decl.type_annotation:
            print(f" type={decl.type_annotation}", end="")

        # Show return type if present
        if hasattr(decl, 'return_type') and decl.return_type:
            print(f" returns={decl.return_type}", end="")

        print()

    if len(ast.declarations) > 20:
        print(f"... and {len(ast.declarations) - 20} more")

    # Check first class
    for decl in ast.declarations:
        if decl.__class__.__name__ == 'ClassDeclaration':
            print(f"\n📦 First class '{decl.name}' has {len(decl.members)} members:")
            for j, member in enumerate(decl.members[:10]):
                print(f"  {j+1:2}. {member.__class__.__name__:30} ", end="")
                if hasattr(member, 'name'):
                    print(f"name='{member.name}'", end="")
                if hasattr(member, 'type_annotation') and member.type_annotation:
                    print(f" type={member.type_annotation}", end="")
                print()
            if len(decl.members) > 10:
                print(f"  ... and {len(decl.members) - 10} more")
            break

    return ast

if __name__ == "__main__":
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else "examples/ecommerce/store.as4"
    inspect_ast(file_path)
