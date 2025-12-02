"""
Tests for incremental compilation system
"""

import pytest
import os
import tempfile
import time
import shutil
from pathlib import Path
from compiler.incremental import IncrementalCompiler, CacheEntry


class TestIncrementalCompiler:
    """Tests for incremental compilation"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp = tempfile.mkdtemp()
        yield temp
        # Cleanup
        shutil.rmtree(temp)

    @pytest.fixture
    def compiler(self, temp_dir):
        """Create incremental compiler with temp cache"""
        cache_dir = os.path.join(temp_dir, ".cache")
        return IncrementalCompiler(cache_dir=cache_dir)

    def test_initialization(self, compiler):
        """Test compiler initialization"""
        assert compiler.cache == {}
        assert compiler.dependency_graph == {}

    def test_needs_recompilation_new_file(self, compiler, temp_dir):
        """Test that new file needs compilation"""
        source = os.path.join(temp_dir, "test.as4")
        with open(source, 'w') as f:
            f.write("var x = 5;")

        assert compiler.needs_recompilation(source) is True

    def test_cache_update(self, compiler, temp_dir):
        """Test updating cache after compilation"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        # Create files
        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        # Update cache
        compiler.update_cache(source, output, dependencies=[])

        # Should be in cache now
        assert source in compiler.cache
        entry = compiler.cache[source]
        assert entry.source_path == source
        assert entry.output_path == output
        assert len(entry.dependencies) == 0

    def test_no_recompilation_when_unchanged(self, compiler, temp_dir):
        """Test that unchanged file doesn't need recompilation"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        # Create files
        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        # First compilation
        compiler.update_cache(source, output)

        # Should not need recompilation
        assert compiler.needs_recompilation(source) is False

    def test_recompilation_when_source_changed(self, compiler, temp_dir):
        """Test that modified file needs recompilation"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        # Create and cache
        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        compiler.update_cache(source, output)

        # Wait a moment to ensure different timestamp
        time.sleep(0.01)

        # Modify source
        with open(source, 'w') as f:
            f.write("var x = 10;")  # Changed

        # Should need recompilation
        assert compiler.needs_recompilation(source) is True

    def test_recompilation_when_output_missing(self, compiler, temp_dir):
        """Test that missing output triggers recompilation"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        # Create files
        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        compiler.update_cache(source, output)

        # Remove output
        os.remove(output)

        # Should need recompilation
        assert compiler.needs_recompilation(source) is True

    def test_dependency_tracking(self, compiler, temp_dir):
        """Test dependency graph tracking"""
        main = os.path.join(temp_dir, "main.as4")
        util = os.path.join(temp_dir, "util.as4")
        main_out = os.path.join(temp_dir, "main.js")
        util_out = os.path.join(temp_dir, "util.js")

        # Create files
        with open(util, 'w') as f:
            f.write("function add(a, b) { return a + b; }")
        with open(main, 'w') as f:
            f.write('import {add} from "./util";\nvar result = add(1, 2);')

        # Create outputs
        with open(util_out, 'w') as f:
            f.write("function add(a, b) { return a + b; }")
        with open(main_out, 'w') as f:
            f.write("var result = add(1, 2);")

        # Update cache with dependency
        compiler.update_cache(util, util_out, dependencies=[])
        compiler.update_cache(main, main_out, dependencies=[util])

        # Check dependency graph
        assert util in compiler.dependency_graph
        assert main in compiler.dependency_graph[util]

    def test_recompilation_on_dependency_change(self, compiler, temp_dir):
        """Test that changing dependency triggers dependent recompilation"""
        main = os.path.join(temp_dir, "main.as4")
        util = os.path.join(temp_dir, "util.as4")
        main_out = os.path.join(temp_dir, "main.js")
        util_out = os.path.join(temp_dir, "util.js")

        # Create files
        with open(util, 'w') as f:
            f.write("function add(a, b) { return a + b; }")
        with open(main, 'w') as f:
            f.write("import util")
        with open(util_out, 'w') as f:
            f.write("")
        with open(main_out, 'w') as f:
            f.write("")

        # Cache both files
        compiler.update_cache(util, util_out, dependencies=[])
        compiler.update_cache(main, main_out, dependencies=[util])

        # Both should not need recompilation
        assert compiler.needs_recompilation(util) is False
        assert compiler.needs_recompilation(main) is False

        time.sleep(0.01)

        # Modify dependency
        with open(util, 'w') as f:
            f.write("function add(a, b) { return a + b + 1; }")  # Changed

        # Dependency should need recompilation
        assert compiler.needs_recompilation(util) is True

        # Main should also need recompilation because dependency changed
        assert compiler.needs_recompilation(main) is True

    def test_get_files_to_recompile(self, compiler, temp_dir):
        """Test getting list of files to recompile"""
        file1 = os.path.join(temp_dir, "file1.as4")
        file2 = os.path.join(temp_dir, "file2.as4")
        file3 = os.path.join(temp_dir, "file3.as4")

        # Create files
        for f in [file1, file2, file3]:
            with open(f, 'w') as fp:
                fp.write("var x = 1;")
            with open(f.replace('.as4', '.js'), 'w') as fp:
                fp.write("var x = 1;")

        # Cache all
        compiler.update_cache(file1, file1.replace('.as4', '.js'))
        compiler.update_cache(file2, file2.replace('.as4', '.js'), dependencies=[file1])
        compiler.update_cache(file3, file3.replace('.as4', '.js'))

        # Modify file1
        time.sleep(0.01)
        with open(file1, 'w') as f:
            f.write("var x = 2;")

        # Get files to recompile
        to_recompile = compiler.get_files_to_recompile([file1, file2, file3])

        # file1 changed, so file1 and file2 (depends on file1) should recompile
        # file3 unchanged and no dependencies
        assert file1 in to_recompile
        assert file2 in to_recompile
        assert file3 not in to_recompile

    def test_cache_persistence(self, temp_dir):
        """Test that cache persists across compiler instances"""
        cache_dir = os.path.join(temp_dir, ".cache")
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        # Create file
        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        # First compiler instance
        compiler1 = IncrementalCompiler(cache_dir=cache_dir)
        compiler1.update_cache(source, output)

        # Second compiler instance (should load cache)
        compiler2 = IncrementalCompiler(cache_dir=cache_dir)

        # Should have loaded cache
        assert source in compiler2.cache
        assert compiler2.needs_recompilation(source) is False

    def test_clear_cache(self, compiler, temp_dir):
        """Test clearing cache"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        compiler.update_cache(source, output)
        assert len(compiler.cache) > 0

        compiler.clear_cache()
        assert len(compiler.cache) == 0
        assert len(compiler.dependency_graph) == 0

    def test_invalidate_file(self, compiler, temp_dir):
        """Test invalidating specific file"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        compiler.update_cache(source, output)
        assert source in compiler.cache

        compiler.invalidate_file(source)
        assert source not in compiler.cache

    def test_prune_cache(self, compiler, temp_dir):
        """Test pruning deleted files from cache"""
        file1 = os.path.join(temp_dir, "file1.as4")
        file2 = os.path.join(temp_dir, "file2.as4")

        # Create files
        with open(file1, 'w') as f:
            f.write("var x = 1;")
        with open(file2, 'w') as f:
            f.write("var x = 2;")

        # Cache both
        compiler.update_cache(file1, file1.replace('.as4', '.js'))
        compiler.update_cache(file2, file2.replace('.as4', '.js'))

        assert len(compiler.cache) == 2

        # Delete file1
        os.remove(file1)

        # Prune cache
        removed = compiler.prune_cache()

        assert removed == 1
        assert len(compiler.cache) == 1
        assert file2 in compiler.cache
        assert file1 not in compiler.cache

    def test_cache_stats(self, compiler, temp_dir):
        """Test getting cache statistics"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        with open(source, 'w') as f:
            f.write("var x = 5;")
        with open(output, 'w') as f:
            f.write("var x = 5;")

        compiler.update_cache(source, output, dependencies=["dep1.as4", "dep2.as4"])

        stats = compiler.get_cache_stats()

        assert stats['total_files'] == 1
        assert stats['total_dependencies'] == 2  # source has 2 dependencies (dep1, dep2)
        assert stats['cache_size_bytes'] > 0

    def test_nested_dependencies(self, compiler, temp_dir):
        """Test nested dependency chain: A -> B -> C"""
        fileA = os.path.join(temp_dir, "a.as4")
        fileB = os.path.join(temp_dir, "b.as4")
        fileC = os.path.join(temp_dir, "c.as4")

        # Create files
        for f in [fileA, fileB, fileC]:
            with open(f, 'w') as fp:
                fp.write("var x = 1;")
            with open(f.replace('.as4', '.js'), 'w') as fp:
                fp.write("var x = 1;")

        # Cache with dependencies: A imports B, B imports C
        compiler.update_cache(fileC, fileC.replace('.as4', '.js'))
        compiler.update_cache(fileB, fileB.replace('.as4', '.js'), dependencies=[fileC])
        compiler.update_cache(fileA, fileA.replace('.as4', '.js'), dependencies=[fileB])

        # All should not need recompilation
        assert compiler.needs_recompilation(fileC) is False
        assert compiler.needs_recompilation(fileB) is False
        assert compiler.needs_recompilation(fileA) is False

        time.sleep(0.01)

        # Modify C (bottom of chain)
        with open(fileC, 'w') as f:
            f.write("var x = 2;")

        # All should need recompilation (C changed, B depends on C, A depends on B)
        assert compiler.needs_recompilation(fileC) is True
        assert compiler.needs_recompilation(fileB) is True
        assert compiler.needs_recompilation(fileA) is True
