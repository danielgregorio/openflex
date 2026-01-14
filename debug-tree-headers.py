#!/usr/bin/env python3
"""Debug tree-sitter parsing of headers variable"""

from compiler.parser.as4_parser import AS4Parser

def debug_tree():
    """Debug tree-sitter output for headers"""

    code = """const headers = {
    "Content-Type": "application/json",
    ...(options.headers ?? {})
};"""

    parser = AS4Parser()

    # Get the tree-sitter tree directly
    tree = parser.parser.parse(bytes(code, "utf8"))
    root = tree.root_node

    def print_node(node, source, indent=0, max_depth=8):
        if indent > max_depth:
            return

        text = source[node.start_byte:node.end_byte]
        if len(text) > 60:
            text = text[:57] + "..."
        text = repr(text)

        print("  " * indent + f"{node.type:25} {text}")

        for child in node.children:
            print_node(child, source, indent + 1, max_depth)

    print("=== Tree-sitter Parse Tree ===\n")
    print_node(root, code)

if __name__ == "__main__":
    debug_tree()
