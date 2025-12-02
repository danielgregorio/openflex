"""
Bundle Optimization System
Tree shaking, minification, and module concatenation
"""

import re
from typing import List, Set, Dict, Optional
from dataclasses import dataclass


@dataclass
class OptimizationStats:
    """Statistics about bundle optimization"""
    original_size: int
    optimized_size: int
    removed_functions: int
    removed_variables: int
    removed_imports: int

    @property
    def reduction_percent(self) -> float:
        """Calculate size reduction percentage"""
        if self.original_size == 0:
            return 0.0
        return ((self.original_size - self.optimized_size) / self.original_size) * 100


class TreeShaker:
    """
    Dead code elimination via tree shaking
    Removes unused functions, variables, and imports
    """

    def __init__(self):
        self.used_identifiers: Set[str] = set()
        self.defined_functions: Dict[str, str] = {}
        self.defined_variables: Dict[str, str] = {}
        self.imports: Dict[str, str] = {}

    def analyze_usage(self, code: str) -> None:
        """Analyze code to find used identifiers"""
        # Find all identifier usages (simplified - real implementation would use AST)
        # Remove function declarations first so we don't count the function name itself as used
        code_without_decls = re.sub(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', 'function(', code)

        # This matches function calls, variable references, etc.
        identifier_pattern = r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
        matches = re.findall(identifier_pattern, code_without_decls)

        # Add to used identifiers
        for identifier in matches:
            # Skip keywords
            if identifier not in ['function', 'var', 'const', 'let', 'if', 'else',
                                   'for', 'while', 'return', 'class', 'new', 'this']:
                self.used_identifiers.add(identifier)

    def extract_definitions(self, code: str) -> None:
        """Extract function and variable definitions"""
        # Extract function declarations - handle nested braces properly
        lines = code.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            func_match = re.match(r'\s*function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', line)
            if func_match:
                func_name = func_match.group(1)
                # Find matching closing brace
                brace_count = 0
                start_line = i
                found_open = False

                for j in range(i, len(lines)):
                    for char in lines[j]:
                        if char == '{':
                            brace_count += 1
                            found_open = True
                        elif char == '}':
                            brace_count -= 1
                            if found_open and brace_count == 0:
                                # Found matching close
                                func_code = '\n'.join(lines[start_line:j+1])
                                self.defined_functions[func_name] = func_code
                                i = j
                                break
                    if found_open and brace_count == 0:
                        break
            i += 1

        # Extract variable declarations
        var_pattern = r'(?:var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*='
        for match in re.finditer(var_pattern, code):
            var_name = match.group(1)
            self.defined_variables[var_name] = match.group(0)

        # Extract imports
        import_pattern = r'import\s+\{([^}]+)\}\s+from\s+["\']([^"\']+)["\']'
        for match in re.finditer(import_pattern, code):
            imports = match.group(1).split(',')
            for imp in imports:
                imp = imp.strip()
                self.imports[imp] = match.group(0)

    def shake(self, code: str, entry_points: Optional[List[str]] = None) -> str:
        """
        Remove unused code (tree shaking)

        Args:
            code: Source code to optimize
            entry_points: List of entry point function names (default: ['main'])

        Returns:
            Optimized code with dead code removed
        """
        if entry_points is None:
            entry_points = ['main']

        # Extract all definitions
        self.extract_definitions(code)

        # Mark entry points as used
        for entry in entry_points:
            self.used_identifiers.add(entry)

        # Analyze code to find all used identifiers
        self.analyze_usage(code)

        # Recursively mark dependencies as used
        changed = True
        while changed:
            changed = False
            for identifier in list(self.used_identifiers):
                # If this is a defined function, analyze its body
                if identifier in self.defined_functions:
                    func_code = self.defined_functions[identifier]
                    old_size = len(self.used_identifiers)
                    self.analyze_usage(func_code)
                    if len(self.used_identifiers) > old_size:
                        changed = True

        # Remove unused functions by rebuilding only with used ones
        # Split code into lines for better control
        lines = code.split('\n')
        result_lines = []
        skip_until_line = -1

        for i, line in enumerate(lines):
            # If we're in a skipped function, continue
            if i < skip_until_line:
                continue

            # Check if this line starts a function
            func_match = re.match(r'\s*function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', line)
            if func_match:
                func_name = func_match.group(1)

                # If this function is unused, skip it
                if func_name in self.defined_functions and func_name not in self.used_identifiers:
                    # Find the end of this function
                    brace_count = 0
                    found_open = False
                    for j in range(i, len(lines)):
                        for char in lines[j]:
                            if char == '{':
                                brace_count += 1
                                found_open = True
                            elif char == '}':
                                brace_count -= 1
                                if found_open and brace_count == 0:
                                    skip_until_line = j + 1
                                    break
                        if found_open and brace_count == 0:
                            break
                    continue

            result_lines.append(line)

        # Join lines and clean up extra whitespace
        result = '\n'.join(result_lines)
        result = re.sub(r'\n\n+', '\n\n', result)

        return result.strip()


class Minifier:
    """
    Code minification - removes whitespace and shortens identifiers
    """

    def __init__(self):
        self.identifier_map: Dict[str, str] = {}
        self.next_id = 0

    def _generate_short_name(self) -> str:
        """Generate short identifier name"""
        # Generate: a, b, c, ..., z, aa, ab, ...
        chars = 'abcdefghijklmnopqrstuvwxyz'
        result = ''
        n = self.next_id
        self.next_id += 1

        if n == 0:
            return 'a'

        while n >= 0:
            result = chars[n % 26] + result
            n = n // 26 - 1
            if n < 0:
                break

        return result

    def minify(self, code: str, aggressive: bool = False) -> str:
        """
        Minify code

        Args:
            code: Source code to minify
            aggressive: If True, also rename identifiers

        Returns:
            Minified code
        """
        result = code

        # Remove comments
        result = re.sub(r'//.*?$', '', result, flags=re.MULTILINE)
        result = re.sub(r'/\*.*?\*/', '', result, flags=re.DOTALL)

        # Remove unnecessary whitespace
        result = re.sub(r'[ \t]+', ' ', result)  # Multiple spaces to single
        result = re.sub(r' *([{};,()[\]]) *', r'\1', result)  # Around punctuation
        result = re.sub(r'\n+', '\n', result)  # Multiple newlines to single
        result = re.sub(r'^\s+', '', result, flags=re.MULTILINE)  # Leading whitespace

        # Remove newlines where safe
        result = re.sub(r'\n([{}();,])', r'\1', result)
        result = re.sub(r'([{}();,])\n', r'\1', result)

        if aggressive:
            # Rename local variables (simplified - real minifier would use AST)
            # This is a basic implementation
            var_pattern = r'\b(var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\b'

            for match in re.finditer(var_pattern, result):
                original_name = match.group(2)
                # Don't rename common globals or keywords
                if original_name not in ['console', 'window', 'document', 'Array',
                                          'Object', 'String', 'Number', 'Boolean',
                                          'Math', 'JSON', 'Date', 'Error']:
                    if original_name not in self.identifier_map:
                        self.identifier_map[original_name] = self._generate_short_name()

            # Apply renamings
            for original, shortened in self.identifier_map.items():
                # Use word boundaries to avoid partial replacements
                result = re.sub(rf'\b{original}\b', shortened, result)

        return result.strip()


class BundleOptimizer:
    """
    Complete bundle optimization pipeline
    Combines tree shaking and minification
    """

    def __init__(self):
        self.tree_shaker = TreeShaker()
        self.minifier = Minifier()
        self.stats = OptimizationStats(0, 0, 0, 0, 0)

    def optimize(
        self,
        code: str,
        entry_points: Optional[List[str]] = None,
        tree_shake: bool = True,
        minify: bool = True,
        aggressive_minify: bool = False
    ) -> str:
        """
        Optimize bundle with tree shaking and minification

        Args:
            code: Source code to optimize
            entry_points: Entry point functions (default: ['main'])
            tree_shake: Enable tree shaking
            minify: Enable minification
            aggressive_minify: Enable aggressive minification (rename vars)

        Returns:
            Optimized code
        """
        original_size = len(code)
        result = code

        # Count original definitions
        original_funcs = len(re.findall(r'function\s+\w+', code))
        original_vars = len(re.findall(r'(?:var|let|const)\s+\w+', code))
        original_imports = len(re.findall(r'import\s+', code))

        # Tree shaking
        if tree_shake:
            result = self.tree_shaker.shake(result, entry_points)

        # Minification
        if minify:
            result = self.minifier.minify(result, aggressive=aggressive_minify)

        # Count after optimization
        optimized_funcs = len(re.findall(r'function\s+\w+', result))
        optimized_vars = len(re.findall(r'(?:var|let|const)\s+\w+', result))
        optimized_imports = len(re.findall(r'import\s+', result))

        # Update stats
        self.stats = OptimizationStats(
            original_size=original_size,
            optimized_size=len(result),
            removed_functions=original_funcs - optimized_funcs,
            removed_variables=original_vars - optimized_vars,
            removed_imports=original_imports - optimized_imports
        )

        return result

    def get_stats(self) -> OptimizationStats:
        """Get optimization statistics"""
        return self.stats
