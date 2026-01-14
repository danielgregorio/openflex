#!/usr/bin/env python3
"""Debug specific AST node to understand parsing issue"""

from compiler.parser.as4_parser import AS4Parser
from compiler.codegen.js_codegen import JSCodeGenerator

def debug_method(source_code: str):
    """Parse and inspect a specific method"""

    parser = AS4Parser()
    ast = parser.parse(source_code, "test.as4")

    print("=== AST Structure ===")
    print(f"Total declarations: {len(ast.declarations)}\n")

    # Find StoreAPI class
    for decl in ast.declarations:
        if decl.__class__.__name__ == 'ClassDeclaration' and decl.name == 'StoreAPI':
            print(f"Found StoreAPI class with {len(decl.members)} members\n")

            # Find request method
            for i, member in enumerate(decl.members):
                print(f"{i+1}. {member.__class__.__name__} name='{getattr(member, 'name', 'N/A')}'")

                if getattr(member, 'name', None) == 'request':
                    print(f"\n=== Request Method Details ===")
                    print(f"Async: {member.is_async}")
                    print(f"Params: {len(member.params)}")
                    print(f"Return type: {member.return_type}")

                    if member.body:
                        print(f"Body statements: {len(member.body.body)}")
                        for j, stmt in enumerate(member.body.body):
                            print(f"  {j+1}. {stmt.__class__.__name__}", end="")
                            if hasattr(stmt, 'name'):
                                print(f" name='{stmt.name}'", end="")
                            print()

                    print(f"\n=== Generated JavaScript ===")
                    codegen = JSCodeGenerator()
                    js_code = codegen._generate_function_declaration(member)
                    print(js_code[:500])
                    break
            break

# Minimal test case
code = """
class StoreAPI {
    private baseUrl: String = "/api";

    private async request(endpoint: String, options: Object = {}): Promise<Object> {
        const url = this.baseUrl + endpoint;
        const token = this.getAuthToken();

        const headers = {
            "Content-Type": "application/json",
            ...(options.headers ?? {})
        };

        return {};
    }

    async getProducts(category: String = ""): Promise<Array<Product>> {
        const endpoint = category ? "/products?category=" + category : "/products";
        return [];
    }
}
"""

debug_method(code)
