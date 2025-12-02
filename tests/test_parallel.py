"""
Tests for parallel compilation system
"""

import pytest
import os
import tempfile
import shutil
import time
from compiler.parallel import (
    ParallelCompiler,
    CompilationTask,
    CompilationResult,
    compile_files_parallel
)


class TestParallelCompiler:
    """Tests for parallel compilation"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp = tempfile.mkdtemp()
        yield temp
        # Cleanup
        shutil.rmtree(temp)

    @pytest.fixture
    def compiler(self):
        """Create parallel compiler (use threads for testing)"""
        return ParallelCompiler(max_workers=2, use_threads=True)

    def test_initialization(self, compiler):
        """Test compiler initialization"""
        assert compiler.max_workers == 2
        assert compiler.use_threads is True  # Tests use threads
        assert compiler.stats['total_files'] == 0

    def test_initialization_auto_workers(self):
        """Test auto-detection of worker count"""
        compiler = ParallelCompiler()
        import multiprocessing
        assert compiler.max_workers == multiprocessing.cpu_count()

    def test_empty_task_list(self, compiler):
        """Test compiling empty task list"""
        def dummy_compile(task):
            return CompilationResult(task.source_file, task.output_file, True)

        results = compiler.compile_files([], dummy_compile)
        assert len(results) == 0

    def test_single_file_compilation(self, compiler, temp_dir):
        """Test compiling a single file"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        with open(source, 'w') as f:
            f.write("var x = 5;")

        def compile_func(task: CompilationTask) -> CompilationResult:
            start = time.time()
            # Simulate compilation
            with open(task.output_file, 'w') as f:
                f.write("var x = 5;")
            duration = time.time() - start
            return CompilationResult(
                source_file=task.source_file,
                output_file=task.output_file,
                success=True,
                duration=duration
            )

        task = CompilationTask(source, output, {})
        results = compiler.compile_files([task], compile_func)

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].source_file == source
        assert os.path.exists(output)

    def test_multiple_file_compilation(self, compiler, temp_dir):
        """Test compiling multiple files in parallel"""
        tasks = []
        for i in range(5):
            source = os.path.join(temp_dir, f"file{i}.as4")
            output = os.path.join(temp_dir, f"file{i}.js")
            with open(source, 'w') as f:
                f.write(f"var x{i} = {i};")
            tasks.append(CompilationTask(source, output, {}))

        def compile_func(task: CompilationTask) -> CompilationResult:
            start = time.time()
            # Simulate compilation with small delay
            time.sleep(0.01)
            with open(task.output_file, 'w') as f:
                f.write("compiled")
            duration = time.time() - start
            return CompilationResult(
                source_file=task.source_file,
                output_file=task.output_file,
                success=True,
                duration=duration
            )

        results = compiler.compile_files(tasks, compile_func)

        assert len(results) == 5
        assert all(r.success for r in results)
        assert compiler.stats['successful'] == 5
        assert compiler.stats['failed'] == 0

    def test_compilation_error_handling(self, compiler, temp_dir):
        """Test handling of compilation errors"""
        source = os.path.join(temp_dir, "error.as4")
        output = os.path.join(temp_dir, "error.js")

        with open(source, 'w') as f:
            f.write("syntax error")

        def compile_func(task: CompilationTask) -> CompilationResult:
            # Simulate compilation error
            return CompilationResult(
                source_file=task.source_file,
                output_file=task.output_file,
                success=False,
                error="Syntax error on line 1"
            )

        task = CompilationTask(source, output, {})
        results = compiler.compile_files([task], compile_func)

        assert len(results) == 1
        assert results[0].success is False
        assert results[0].error == "Syntax error on line 1"
        assert compiler.stats['failed'] == 1

    def test_exception_handling(self, compiler, temp_dir):
        """Test handling of exceptions during compilation"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        def compile_func(task: CompilationTask) -> CompilationResult:
            raise RuntimeError("Unexpected error")

        task = CompilationTask(source, output, {})
        results = compiler.compile_files([task], compile_func)

        assert len(results) == 1
        assert results[0].success is False
        assert "Unexpected error" in results[0].error
        assert compiler.stats['failed'] == 1

    def test_progress_callback(self, compiler, temp_dir):
        """Test progress callback functionality"""
        tasks = []
        for i in range(3):
            source = os.path.join(temp_dir, f"file{i}.as4")
            output = os.path.join(temp_dir, f"file{i}.js")
            tasks.append(CompilationTask(source, output, {}))

        progress_calls = []

        def progress_callback(current: int, total: int):
            progress_calls.append((current, total))

        def compile_func(task: CompilationTask) -> CompilationResult:
            time.sleep(0.01)
            return CompilationResult(task.source_file, task.output_file, True)

        compiler.compile_files(tasks, compile_func, progress_callback)

        # Should have been called 3 times (once per file)
        assert len(progress_calls) == 3
        assert progress_calls[-1] == (3, 3)  # Last call should be (3, 3)

    def test_get_stats(self, compiler, temp_dir):
        """Test getting compilation statistics"""
        tasks = []
        for i in range(4):
            source = os.path.join(temp_dir, f"file{i}.as4")
            output = os.path.join(temp_dir, f"file{i}.js")
            tasks.append(CompilationTask(source, output, {}))

        def compile_func(task: CompilationTask) -> CompilationResult:
            start = time.time()
            time.sleep(0.01)  # Simulate work
            duration = time.time() - start
            # Fail every other file
            success = int(task.source_file[-5]) % 2 == 0
            return CompilationResult(
                source_file=task.source_file,
                output_file=task.output_file,
                success=success,
                duration=duration
            )

        compiler.compile_files(tasks, compile_func)
        stats = compiler.get_stats()

        assert stats['total_files'] == 4
        assert stats['successful'] == 2
        assert stats['failed'] == 2
        assert stats['parallel_duration'] > 0
        assert stats['total_duration'] > 0
        assert 'speedup' in stats
        assert 'avg_time_per_file' in stats

    def test_reset_stats(self, compiler, temp_dir):
        """Test resetting statistics"""
        source = os.path.join(temp_dir, "test.as4")
        output = os.path.join(temp_dir, "test.js")

        def compile_func(task: CompilationTask) -> CompilationResult:
            return CompilationResult(task.source_file, task.output_file, True)

        task = CompilationTask(source, output, {})
        compiler.compile_files([task], compile_func)

        assert compiler.stats['total_files'] == 1

        compiler.reset_stats()

        assert compiler.stats['total_files'] == 0
        assert compiler.stats['successful'] == 0
        assert compiler.stats['failed'] == 0

    def test_thread_mode(self):
        """Test using threads instead of processes"""
        compiler = ParallelCompiler(max_workers=2, use_threads=True)
        assert compiler.use_threads is True

    def test_batch_compilation(self, compiler, temp_dir):
        """Test compiling files in batches"""
        tasks = []
        for i in range(10):
            source = os.path.join(temp_dir, f"file{i}.as4")
            output = os.path.join(temp_dir, f"file{i}.js")
            tasks.append(CompilationTask(source, output, {}))

        def compile_func(task: CompilationTask) -> CompilationResult:
            return CompilationResult(task.source_file, task.output_file, True)

        # Compile in batches of 3
        results = compiler.compile_files_in_batches(tasks, compile_func, batch_size=3)

        assert len(results) == 10
        assert all(r.success for r in results)

    def test_speedup_calculation(self, compiler, temp_dir):
        """Test that parallel compilation achieves speedup"""
        tasks = []
        for i in range(4):
            source = os.path.join(temp_dir, f"file{i}.as4")
            output = os.path.join(temp_dir, f"file{i}.js")
            tasks.append(CompilationTask(source, output, {}))

        def compile_func(task: CompilationTask) -> CompilationResult:
            start = time.time()
            time.sleep(0.02)  # Simulate work
            duration = time.time() - start
            return CompilationResult(
                source_file=task.source_file,
                output_file=task.output_file,
                success=True,
                duration=duration
            )

        compiler.compile_files(tasks, compile_func)
        stats = compiler.get_stats()

        # With 2 workers and 4 tasks of 0.02s each, total should be ~0.08s
        # but parallel should be ~0.04s (2 batches of 2), so speedup ~2x
        # Allow for overhead
        assert stats['speedup'] > 1.0  # Should have some speedup


class TestCompileFilesParallel:
    """Tests for utility function"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)

    def test_simple_parallel_compilation(self, temp_dir):
        """Test simple parallel compilation helper"""
        # Create source files
        sources = []
        for i in range(3):
            source = os.path.join(temp_dir, f"test{i}.as4")
            with open(source, 'w') as f:
                f.write(f"var x = {i};")
            sources.append(source)

        output_dir = os.path.join(temp_dir, "out")
        os.makedirs(output_dir)

        def compile_func(source: str, output: str) -> bool:
            # Simple compilation: just copy content
            with open(source, 'r') as f:
                content = f.read()
            with open(output, 'w') as f:
                f.write(content)
            return True

        # Compile all files (use threads for testing with local functions)
        success = compile_files_parallel(sources, output_dir, compile_func, max_workers=2, verbose=False, use_threads=True)

        assert success is True
        assert os.path.exists(os.path.join(output_dir, "test0.js"))
        assert os.path.exists(os.path.join(output_dir, "test1.js"))
        assert os.path.exists(os.path.join(output_dir, "test2.js"))

    def test_parallel_with_failure(self, temp_dir):
        """Test parallel compilation with some failures"""
        sources = []
        for i in range(3):
            source = os.path.join(temp_dir, f"test{i}.as4")
            with open(source, 'w') as f:
                f.write(f"var x = {i};")
            sources.append(source)

        output_dir = os.path.join(temp_dir, "out")
        os.makedirs(output_dir)

        def compile_func(source: str, output: str) -> bool:
            # Fail for test1.as4
            if "test1" in source:
                return False
            with open(source, 'r') as f:
                content = f.read()
            with open(output, 'w') as f:
                f.write(content)
            return True

        success = compile_files_parallel(sources, output_dir, compile_func, use_threads=True)

        assert success is False  # Not all succeeded
