#!/usr/bin/env python3
"""
Fix dataclass inheritance issues in ast.py
"""

import re

def fix_ast_file():
    with open('compiler/parser/ast.py', 'r') as f:
        content = f.read()

    # Remove 'type: Optional[Type] = None' from Expression base class
    content = re.sub(
        r'@dataclass\nclass Expression\(ASTNode\):\n    """Base expression class"""\n    type: Optional\[Type\] = None',
        r'@dataclass\nclass Expression(ASTNode):\n    """Base expression class"""\n    pass',
        content
    )

    # Add type and loc fields to all Expression subclasses that have required fields
    # Pattern: find @dataclass\nclass SomeName(Expression): with required fields

    # For classes that inherit from Expression and have required fields,
    # add type and loc at the end
    patterns_to_fix = [
        (r'(@dataclass\nclass Identifier\(Expression\):\n    """[^"]+"""\n    name: str)\n',
         r'\1\n    type: Optional[Type] = None\n    loc: Optional[SourceLocation] = None\n'),
        (r'(@dataclass\nclass Literal\(Expression\):\n    """[^"]+"""\n    value: Any\n    raw: str)\n',
         r'\1\n    type: Optional[Type] = None\n    loc: Optional[SourceLocation] = None\n'),
    ]

    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Write back
    with open('compiler/parser/ast.py', 'w') as f:
        f.write(content)

    print("Fixed ast.py")

if __name__ == '__main__':
    fix_ast_file()
