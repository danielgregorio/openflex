#!/usr/bin/env python3
"""Debug the headers variable declaration"""

from compiler.parser.as4_parser import AS4Parser
from compiler.codegen.js_codegen import JSCodeGenerator

def debug_headers():
    """Debug what's being parsed for headers variable"""

    code = """
class StoreAPI {
    private async request(endpoint: String, options: Object = {}): Promise<Object> {
        const url = this.baseUrl + endpoint;
        const token = this.getAuthToken();

        const headers = {
            "Content-Type": "application/json",
            ...(options.headers ?? {})
        };

        if (token) {
            headers["Authorization"] = "Bearer " + token;
        }

        return {};
    }

    async getProducts(category: String = ""): Promise<Array<Product>> {
        const endpoint = category ? "/products?category=" + category : "/products";
        return [];
    }
}
"""

    parser = AS4Parser()
    ast = parser.parse(code, "test.as4")

    for decl in ast.declarations:
        if decl.__class__.__name__ == 'ClassDeclaration':
            for member in decl.members:
                if getattr(member, 'name', None) == 'request':
                    print(f"=== Request Method Body ===")
                    for i, stmt in enumerate(member.body.body):
                        print(f"\n{i+1}. {stmt.__class__.__name__}")

                        if stmt.__class__.__name__ == 'VariableDeclaration':
                            print(f"   Name: {stmt.name}")
                            print(f"   Type: {stmt.var_type}")
                            print(f"   Has initializer: {stmt.initializer is not None}")

                            if stmt.name == 'headers' and stmt.initializer:
                                print(f"   Initializer type: {stmt.initializer.__class__.__name__}")

                                # Generate just this variable
                                codegen = JSCodeGenerator()
                                var_code = codegen._generate_variable_declaration(stmt)
                                print(f"   Generated: {var_code}")

if __name__ == "__main__":
    debug_headers()
