#!/usr/bin/env python3
"""Debug tree-sitter parse tree using AS4Parser"""

from compiler.parser.as4_parser import AS4Parser

def print_tree(node, source, indent=0, max_depth=7):
    """Recursively print tree structure"""
    if indent > max_depth:
        return

    text = source[node.start_byte:node.end_byte]
    # Truncate long text
    if len(text) > 40:
        text = text[:37] + "..."
    text = repr(text)

    print("  " * indent + f"{node.type:25} {text}")

    for child in node.children:
        print_tree(child, source, indent + 1, max_depth)

def debug_class(source_code: str):
    """Debug parsing of a simple class"""

    parser = AS4Parser()

    # Get the tree-sitter tree
    tree = parser.parser.parse(bytes(source_code, "utf8"))
    root = tree.root_node

    print(f"Root: {root.type}")
    print(f"Children: {len(root.children)}\n")

    print_tree(root, source_code, max_depth=10)

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

    print("=" * 70)
    print("SIMPLE CLASS TEST - Tree-sitter Output")
    print("=" * 70)
    debug_class(code)
