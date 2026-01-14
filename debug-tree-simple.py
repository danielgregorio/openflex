#!/usr/bin/env python3
"""Debug tree-sitter parsing of simple file"""

from compiler.parser.as4_parser import AS4Parser

def debug_tree():
    """Debug tree-sitter output"""

    with open("test-simple.as4", "r") as f:
        code = f.read()

    parser = AS4Parser()

    # Get the tree-sitter tree directly
    tree = parser.parser.parse(bytes(code, "utf8"))
    root = tree.root_node

    def print_node(node, source, indent=0, max_depth=15):
        if indent > max_depth:
            return

        text = source[node.start_byte:node.end_byte]
        if len(text) > 50:
            text = text[:47] + "..."
        text = repr(text)

        error_marker = " ← ERROR" if node.type == "ERROR" or node.is_missing else ""
        print("  " * indent + f"{node.type:25} {text}{error_marker}")

        for child in node.children:
            print_node(child, source, indent + 1, max_depth)

    print("=== Tree-sitter Parse Tree (test-simple.as4) ===\n")
    print_node(root, code, max_depth=12)

if __name__ == "__main__":
    debug_tree()
