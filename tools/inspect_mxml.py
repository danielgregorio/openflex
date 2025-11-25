#!/usr/bin/env python3
"""
MXML Inspector - Visual debugging tool for MXML Neo parser

Usage:
    python tools/inspect_mxml.py examples/hello-world/App.mxml
    python tools/inspect_mxml.py examples/counter/App.mxml --verbose
"""

import sys
import argparse
from pathlib import Path
from dataclasses import fields

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from compiler.parser.mxml_parser import MXMLParser, MXMLComponent
from compiler.parser.ast import *


class MXMLInspector:
    """Visual inspection tool for MXML parsing"""

    def __init__(self, verbose=False):
        self.parser = MXMLParser()
        self.verbose = verbose

    def inspect_file(self, filepath: str):
        """Inspect an MXML file and print detailed analysis"""
        print(f"\n{'='*80}")
        print(f"🔍 Inspecting: {filepath}")
        print(f"{'='*80}\n")

        try:
            app = self.parser.parse_file(filepath)

            self._print_metadata(app)
            self._print_component_tree(app.root_component)
            self._print_scripts(app)
            self._print_styles(app)

            print(f"\n{'='*80}")
            print("✅ Parsing completed successfully!")
            print(f"{'='*80}\n")

        except Exception as e:
            print(f"\n❌ Parsing failed!")
            print(f"Error: {e}\n")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False

        return True

    def _print_metadata(self, app):
        """Print application metadata"""
        print("📋 Metadata")
        print("-" * 80)

        if app.metadata:
            for key, value in app.metadata.items():
                print(f"  {key}: {value}")
        else:
            print("  (none)")

        print()

    def _print_component_tree(self, component: MXMLComponent, indent=0):
        """Recursively print component tree"""
        if indent == 0:
            print("🌳 Component Tree")
            print("-" * 80)

        prefix = "  " * indent

        # Component tag
        print(f"{prefix}├─ <{component.tag}>")

        # Properties
        if component.properties:
            for key, value in component.properties.items():
                if isinstance(value, dict) and 'binding' in value:
                    print(f"{prefix}│  ├─ {key}={{{{binding: {value['binding']}}}}}")
                else:
                    display_value = str(value)
                    if len(display_value) > 50:
                        display_value = display_value[:47] + "..."
                    print(f"{prefix}│  ├─ {key}={repr(display_value)}")

        # Children
        for child in component.children:
            self._print_component_tree(child, indent + 1)

        if indent == 0:
            print()

    def _print_scripts(self, app):
        """Print parsed AS4 scripts"""
        print("📜 Scripts (AS4)")
        print("-" * 80)

        if not app.script_ast:
            print("  (no scripts)")
            print()
            return

        # Print imports
        if app.script_ast.imports:
            print("  Imports:")
            for imp in app.script_ast.imports:
                print(f"    - {imp}")

        # Print declarations
        print(f"  Declarations: {len(app.script_ast.declarations)}")

        for decl in app.script_ast.declarations:
            self._print_declaration(decl, indent=2)

        print()

    def _print_declaration(self, decl, indent=2):
        """Print a single declaration"""
        prefix = " " * indent

        if isinstance(decl, VariableDeclaration):
            decorators = f"@{', @'.join(d.name for d in decl.decorators)} " if decl.decorators else ""
            const_str = "const" if decl.is_const else "var"
            type_str = f": {decl.var_type.name if decl.var_type else '?'}"
            init_str = f" = {self._expr_to_str(decl.initializer)}" if decl.initializer else ""

            print(f"{prefix}├─ {decorators}{const_str} {decl.name}{type_str}{init_str}")

        elif isinstance(decl, FunctionDeclaration):
            decorators = f"@{', @'.join(d.name for d in decl.decorators)} " if decl.decorators else ""
            async_str = "async " if decl.is_async else ""
            params = ", ".join(f"{p.name}: {p.param_type.name if p.param_type else '?'}" for p in decl.params)
            return_type = f": {decl.return_type.name if decl.return_type else 'void'}"

            print(f"{prefix}├─ {decorators}{async_str}function {decl.name}({params}){return_type}")

            if self.verbose and decl.body:
                print(f"{prefix}│  └─ body: {len(decl.body.body)} statements")

        elif isinstance(decl, ClassDeclaration):
            print(f"{prefix}├─ class {decl.name}")

        else:
            print(f"{prefix}├─ {type(decl).__name__}")

    def _expr_to_str(self, expr, max_len=40) -> str:
        """Convert expression to string representation"""
        if expr is None:
            return "null"

        if isinstance(expr, Literal):
            return repr(expr.value)

        if isinstance(expr, Identifier):
            return expr.name

        if isinstance(expr, BinaryExpression):
            left = self._expr_to_str(expr.left)
            right = self._expr_to_str(expr.right)
            return f"{left} {expr.operator} {right}"

        if isinstance(expr, CallExpression):
            callee = self._expr_to_str(expr.callee)
            args = ", ".join(self._expr_to_str(arg) for arg in expr.arguments[:2])
            if len(expr.arguments) > 2:
                args += ", ..."
            return f"{callee}({args})"

        result = f"{type(expr).__name__}(...)"
        if len(result) > max_len:
            result = result[:max_len-3] + "..."

        return result

    def _print_styles(self, app):
        """Print CSS styles"""
        print("🎨 Styles (CSS)")
        print("-" * 80)

        if not app.styles:
            print("  (no styles)")
        else:
            print(f"  {len(app.styles)} style rules found")

            if self.verbose:
                for selector, rules in list(app.styles.items())[:5]:  # Show first 5
                    print(f"    .{selector} {{")
                    print(f"      {rules}")
                    print(f"    }}")

        print()

    def compare_files(self, file1: str, file2: str):
        """Compare two MXML files"""
        print(f"\n{'='*80}")
        print(f"🔄 Comparing Files")
        print(f"{'='*80}\n")

        try:
            app1 = self.parser.parse_file(file1)
            app2 = self.parser.parse_file(file2)

            print(f"File 1: {file1}")
            print(f"  - Components: {self._count_components(app1.root_component)}")
            print(f"  - Scripts: {'Yes' if app1.script_ast else 'No'}")
            print(f"  - Declarations: {len(app1.script_ast.declarations) if app1.script_ast else 0}")

            print(f"\nFile 2: {file2}")
            print(f"  - Components: {self._count_components(app2.root_component)}")
            print(f"  - Scripts: {'Yes' if app2.script_ast else 'No'}")
            print(f"  - Declarations: {len(app2.script_ast.declarations) if app2.script_ast else 0}")

        except Exception as e:
            print(f"❌ Comparison failed: {e}")
            return False

        return True

    def _count_components(self, component: MXMLComponent) -> int:
        """Recursively count components"""
        count = 1
        for child in component.children:
            count += self._count_components(child)
        return count


def main():
    parser = argparse.ArgumentParser(
        description="MXML Inspector - Debug and visualize MXML parsing"
    )
    parser.add_argument(
        'file',
        help='MXML file to inspect'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '-c', '--compare',
        help='Compare with another MXML file'
    )

    args = parser.parse_args()

    inspector = MXMLInspector(verbose=args.verbose)

    if args.compare:
        inspector.compare_files(args.file, args.compare)
    else:
        success = inspector.inspect_file(args.file)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
