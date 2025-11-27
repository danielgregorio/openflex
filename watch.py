#!/usr/bin/env python3
"""
OpenFlex Neo - Watch Mode
Auto-compile AS4 and MXML files on changes
"""

import sys
import os
from pathlib import Path
from datetime import datetime

from compiler.watcher import FileWatcher
from compiler.parser.as4_parser import AS4Parser
from compiler.codegen.js_codegen import JSCodeGenerator
from compiler.enhanced_mxml_compiler import EnhancedMXMLCompiler
from compiler.errors import CompilerError


def compile_as4(file_path: str) -> bool:
    """
    Compile AS4 file to JavaScript

    Args:
        file_path: Path to AS4 file

    Returns:
        True if compilation succeeded
    """
    try:
        # Read source
        with open(file_path, 'r') as f:
            source = f.read()

        # Parse
        parser = AS4Parser()
        ast = parser.parse(source, file_path)

        # Generate code
        codegen = JSCodeGenerator()
        js_code = codegen.generate(ast)

        # Write output
        output_path = file_path.replace('.as4', '.js')
        with open(output_path, 'w') as f:
            f.write(js_code)

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"   [{timestamp}] ✅ Compiled to {output_path}")
        return True

    except CompilerError as e:
        print(f"   {e.format_error(use_color=True)}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def compile_mxml(file_path: str) -> bool:
    """
    Compile MXML file to Web Component

    Args:
        file_path: Path to MXML file

    Returns:
        True if compilation succeeded
    """
    try:
        # Read source
        with open(file_path, 'r') as f:
            source = f.read()

        # Compile
        compiler = EnhancedMXMLCompiler()
        js_code = compiler.compile(source, file_path)

        # Write output
        output_path = file_path.replace('.mxml', '-component.js')
        with open(output_path, 'w') as f:
            f.write(js_code)

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"   [{timestamp}] ✅ Compiled to {output_path}")
        return True

    except CompilerError as e:
        print(f"   {e.format_error(use_color=True)}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def on_file_change(file_path: str):
    """Handle file change event"""
    ext = os.path.splitext(file_path)[1]

    if ext == '.as4':
        compile_as4(file_path)
    elif ext == '.mxml':
        compile_mxml(file_path)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python watch.py <directory>")
        print()
        print("Examples:")
        print("  python watch.py examples/")
        print("  python watch.py src/")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        sys.exit(1)

    print("🚀 OpenFlex Neo - Watch Mode")
    print("=" * 60)
    print()

    # Create watcher
    watcher = FileWatcher(poll_interval=0.5)

    # Watch AS4 files
    as4_files = list(Path(directory).rglob("*.as4"))
    for file_path in as4_files:
        watcher.watch(str(file_path), on_file_change)

    # Watch MXML files
    mxml_files = list(Path(directory).rglob("*.mxml"))
    for file_path in mxml_files:
        watcher.watch(str(file_path), on_file_change)

    total_files = len(as4_files) + len(mxml_files)

    if total_files == 0:
        print(f"No AS4 or MXML files found in {directory}")
        sys.exit(1)

    print(f"📁 Watching directory: {directory}")
    print(f"   AS4 files:  {len(as4_files)}")
    print(f"   MXML files: {len(mxml_files)}")
    print()

    def on_start():
        """Initial compilation of all files"""
        print("🔨 Initial compilation...")
        print()

        for file_path in as4_files:
            print(f"📄 Compiling {file_path}...")
            compile_as4(str(file_path))

        for file_path in mxml_files:
            print(f"📄 Compiling {file_path}...")
            compile_mxml(str(file_path))

        print()

    # Run watcher
    watcher.run(on_start=on_start)


if __name__ == '__main__':
    main()
