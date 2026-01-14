#!/usr/bin/env python3
"""Debug ghost number nodes in simple code"""

from compiler.parser.as4_parser import AS4Parser

def debug_ghost():
    """Find ghost number nodes"""

    code = """
async function test(): Promise<void> {
    console.log("Test");
    const x = getToken();
    if (x) {
        console.log("OK");
    }
}
"""

    parser = AS4Parser()
    tree = parser.parser.parse(bytes(code, "utf8"))
    root = tree.root_node

    def find_nodes(node, source, path=""):
        """Find all number nodes"""
        current_path = f"{path}/{node.type}"

        if node.type == 'number':
            text = source[node.start_byte:node.end_byte]
            print(f"FOUND NUMBER: {repr(text)} at {node.start_point}")
            print(f"  Path: {current_path}")
            print(f"  Parent: {node.parent.type if node.parent else 'None'}")
            print()

        for child in node.children:
            find_nodes(child, source, current_path)

    print("=== Searching for number nodes ===\n")
    find_nodes(root, code)

if __name__ == "__main__":
    debug_ghost()
