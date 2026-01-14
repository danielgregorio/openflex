#!/usr/bin/env python3
"""Debug tree-sitter parse tree"""

from tree_sitter import Language, Parser
from pathlib import Path
import os

def print_tree(node, source, indent=0, max_depth=6):
    """Recursively print tree structure"""
    if indent > max_depth:
        return

    text = source[node.start_byte:node.end_byte]
    # Truncate long text
    if len(text) > 50:
        text = text[:47] + "..."
    text = repr(text)

    print("  " * indent + f"{node.type:30} {text}")

    for child in node.children:
        print_tree(child, source, indent + 1, max_depth)

def debug_class(source_code: str):
    """Debug parsing of a simple class"""

    # Load the language
    grammar_path = Path(__file__).parent / "compiler" / "parser" / "tree-sitter-as4"
    so_file = grammar_path / "build" / "as4.so"

    if not so_file.exists():
        print(f"ERROR: {so_file} not found!")
        return

    AS4_LANGUAGE = Language(str(so_file), 'as4')

    parser = Parser()
    parser.set_language(AS4_LANGUAGE)

    tree = parser.parse(bytes(source_code, "utf8"))
    root = tree.root_node

    print(f"Root: {root.type}")
    print(f"Children: {len(root.children)}\n")

    print_tree(root, source_code, max_depth=8)

if __name__ == "__main__":
    # Simple class example
    code = """
class StoreAPI {
    private baseUrl: String = "/api";
    private token: String = "";

    setAuthToken(token: String): void {
        this.token = token;
    }
}
"""

    print("=" * 60)
    print("SIMPLE CLASS TEST")
    print("=" * 60)
    debug_class(code)
