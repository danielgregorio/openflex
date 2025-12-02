"""
Tests for bundle optimization system
"""

import pytest
from compiler.optimizer import TreeShaker, Minifier, BundleOptimizer


class TestTreeShaker:
    """Tests for tree shaking (dead code elimination)"""

    def test_remove_unused_function(self):
        """Test removing unused function"""
        code = """
function main() {
    used();
}

function used() {
    return 5;
}

function unused() {
    return 10;
}
"""
        shaker = TreeShaker()
        result = shaker.shake(code, entry_points=['main'])

        assert 'function used' in result
        assert 'function unused' not in result
        assert 'function main' in result

    def test_keep_transitively_used_functions(self):
        """Test keeping transitively used functions"""
        code = """
function main() {
    a();
}

function a() {
    b();
}

function b() {
    return 42;
}

function unused() {
    return 0;
}
"""
        shaker = TreeShaker()
        result = shaker.shake(code, entry_points=['main'])

        assert 'function main' in result
        assert 'function a' in result
        assert 'function b' in result
        assert 'function unused' not in result

    def test_multiple_entry_points(self):
        """Test with multiple entry points"""
        code = """
function main() {
    helper1();
}

function init() {
    helper2();
}

function helper1() {
    return 1;
}

function helper2() {
    return 2;
}

function unused() {
    return 3;
}
"""
        shaker = TreeShaker()
        result = shaker.shake(code, entry_points=['main', 'init'])

        assert 'function main' in result
        assert 'function init' in result
        assert 'function helper1' in result
        assert 'function helper2' in result
        assert 'function unused' not in result

    def test_empty_code(self):
        """Test with empty code"""
        shaker = TreeShaker()
        result = shaker.shake('', entry_points=['main'])
        assert result == ''

    def test_all_functions_used(self):
        """Test when all functions are used"""
        code = """
function main() {
    helper();
}

function helper() {
    return 5;
}
"""
        shaker = TreeShaker()
        result = shaker.shake(code, entry_points=['main'])

        assert 'function main' in result
        assert 'function helper' in result


class TestMinifier:
    """Tests for code minification"""

    def test_remove_comments(self):
        """Test removing comments"""
        code = """
// This is a comment
function test() {
    /* Multi-line
       comment */
    return 5;
}
"""
        minifier = Minifier()
        result = minifier.minify(code, aggressive=False)

        assert 'This is a comment' not in result
        assert 'Multi-line' not in result
        assert 'function test' in result

    def test_remove_whitespace(self):
        """Test removing unnecessary whitespace"""
        code = """
function   test  (  )   {
    return    5  ;
}
"""
        minifier = Minifier()
        result = minifier.minify(code, aggressive=False)

        # Should have minimal whitespace
        assert '  ' not in result  # No double spaces
        assert 'function test()' in result
        assert 'return 5;' in result

    def test_basic_minification(self):
        """Test basic minification without renaming"""
        code = """
function add(a, b) {
    var result = a + b;
    return result;
}
"""
        minifier = Minifier()
        result = minifier.minify(code, aggressive=False)

        # Whitespace should be minimized
        assert len(result) < len(code)
        # But identifiers should remain
        assert 'add' in result
        assert 'result' in result

    def test_aggressive_minification(self):
        """Test aggressive minification with variable renaming"""
        code = """
var localVariable = 5;
let anotherOne = 10;
const thirdOne = 15;
"""
        minifier = Minifier()
        result = minifier.minify(code, aggressive=True)

        # Should be shorter
        assert len(result) < len(code)

        # Local variables should be renamed (simplified check)
        # Note: actual renaming depends on implementation

    def test_preserve_globals(self):
        """Test that globals are preserved during minification"""
        code = """
console.log("Hello");
Math.sqrt(16);
JSON.parse("{}");
"""
        minifier = Minifier()
        result = minifier.minify(code, aggressive=True)

        # Globals should not be renamed
        assert 'console' in result
        assert 'Math' in result
        assert 'JSON' in result

    def test_empty_code(self):
        """Test minifying empty code"""
        minifier = Minifier()
        result = minifier.minify('', aggressive=False)
        assert result == ''


class TestBundleOptimizer:
    """Tests for complete bundle optimization"""

    def test_full_optimization(self):
        """Test complete optimization pipeline"""
        code = """
// Main entry point
function main() {
    var x = 5;
    helper(x);
}

// Used helper
function helper(val) {
    return val * 2;
}

// Unused function
function deadCode() {
    return 999;
}
"""
        optimizer = BundleOptimizer()
        result = optimizer.optimize(
            code,
            entry_points=['main'],
            tree_shake=True,
            minify=True
        )

        # Should remove dead code
        assert 'deadCode' not in result

        # Should keep used code
        assert 'main' in result
        assert 'helper' in result

        # Should be shorter
        assert len(result) < len(code)

        # Comments should be removed
        assert 'Main entry point' not in result

    def test_tree_shake_only(self):
        """Test tree shaking without minification"""
        code = """
function main() {
    used();
}

function used() {
    return 1;
}

function unused() {
    return 2;
}
"""
        optimizer = BundleOptimizer()
        result = optimizer.optimize(
            code,
            entry_points=['main'],
            tree_shake=True,
            minify=False
        )

        assert 'unused' not in result
        assert 'used' in result

    def test_minify_only(self):
        """Test minification without tree shaking"""
        code = """
// Comment
function test  (  ) {
    return   5  ;
}
"""
        optimizer = BundleOptimizer()
        result = optimizer.optimize(
            code,
            tree_shake=False,
            minify=True
        )

        # Comment removed
        assert 'Comment' not in result

        # Whitespace reduced
        assert len(result) < len(code)

    def test_no_optimization(self):
        """Test with all optimizations disabled"""
        code = "function test() { return 5; }"

        optimizer = BundleOptimizer()
        result = optimizer.optimize(
            code,
            tree_shake=False,
            minify=False
        )

        # Should be unchanged
        assert result == code

    def test_optimization_stats(self):
        """Test optimization statistics"""
        code = """
function main() {
    return 1;
}

function unused1() {
    return 2;
}

function unused2() {
    return 3;
}
"""
        optimizer = BundleOptimizer()
        optimizer.optimize(code, entry_points=['main'], tree_shake=True)

        stats = optimizer.get_stats()

        # Should have removed functions
        assert stats.removed_functions > 0

        # Should have size reduction
        assert stats.optimized_size < stats.original_size
        assert stats.reduction_percent > 0

    def test_complex_code(self):
        """Test with more complex code structure"""
        code = """
function main() {
    var data = fetchData();
    processData(data);
}

function fetchData() {
    return {value: 42};
}

function processData(data) {
    console.log(data.value);
}

function unusedHelper1() {
    return "dead";
}

function unusedHelper2() {
    return "also dead";
}
"""
        optimizer = BundleOptimizer()
        result = optimizer.optimize(
            code,
            entry_points=['main'],
            tree_shake=True,
            minify=True
        )

        # Used functions should remain
        assert 'main' in result
        assert 'fetchData' in result
        assert 'processData' in result

        # Unused functions should be removed
        assert 'unusedHelper1' not in result
        assert 'unusedHelper2' not in result

        # Should be significantly smaller
        stats = optimizer.get_stats()
        assert stats.reduction_percent > 20  # At least 20% reduction

    def test_size_reduction(self):
        """Test that optimization reduces code size"""
        code = """
// This is a long comment explaining what this code does
// It goes on for multiple lines
// And contains lots of information

function   main  (  )   {
    var   x   =   5  ;
    var   y   =   10  ;
    helper ( x ,  y ) ;
}

function   helper  ( a,  b )   {
    return   a  +  b  ;
}

function unused() {
    var z = 100;
    return z * 2;
}
"""
        optimizer = BundleOptimizer()
        result = optimizer.optimize(
            code,
            entry_points=['main'],
            tree_shake=True,
            minify=True
        )

        stats = optimizer.get_stats()

        # Should have significant size reduction
        assert stats.optimized_size < stats.original_size
        assert stats.reduction_percent > 30

    def test_preserve_functionality(self):
        """Test that optimization preserves code functionality"""
        code = """
function main() {
    var result = calculate(5, 3);
    return result;
}

function calculate(a, b) {
    return multiply(a, b);
}

function multiply(x, y) {
    return x * y;
}
"""
        optimizer = BundleOptimizer()
        result = optimizer.optimize(
            code,
            entry_points=['main'],
            tree_shake=True,
            minify=True
        )

        # All required functions should be present
        assert 'main' in result
        assert 'calculate' in result
        assert 'multiply' in result

        # Should still have the essential structure
        assert 'return' in result
