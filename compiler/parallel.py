"""
Parallel Compilation System
Compile multiple files concurrently using multiprocessing
"""

import os
import multiprocessing
from typing import List, Dict, Callable, Optional, Any
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import time


@dataclass
class CompilationTask:
    """Represents a single file compilation task"""
    source_file: str
    output_file: str
    options: Dict[str, Any]


@dataclass
class CompilationResult:
    """Result of a compilation task"""
    source_file: str
    output_file: str
    success: bool
    error: Optional[str] = None
    duration: float = 0.0


class ParallelCompiler:
    """
    Parallel compilation system using multiprocessing
    Compiles multiple files concurrently for faster builds
    """

    def __init__(self, max_workers: Optional[int] = None, use_threads: bool = False):
        """
        Initialize parallel compiler

        Args:
            max_workers: Maximum number of parallel workers (default: CPU count)
            use_threads: Use threads instead of processes (useful for I/O-bound tasks)
        """
        if max_workers is None:
            max_workers = multiprocessing.cpu_count()

        self.max_workers = max_workers
        self.use_threads = use_threads
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'total_duration': 0.0,
            'parallel_duration': 0.0
        }

    def compile_files(
        self,
        tasks: List[CompilationTask],
        compile_func: Callable[[CompilationTask], CompilationResult],
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[CompilationResult]:
        """
        Compile multiple files in parallel

        Args:
            tasks: List of compilation tasks
            compile_func: Function that compiles a single task
            progress_callback: Optional callback for progress updates (current, total)

        Returns:
            List of compilation results
        """
        if not tasks:
            return []

        results = []
        self.stats['total_files'] = len(tasks)
        start_time = time.time()

        # Choose executor based on mode
        executor_class = ThreadPoolExecutor if self.use_threads else ProcessPoolExecutor

        try:
            with executor_class(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_task = {
                    executor.submit(compile_func, task): task
                    for task in tasks
                }

                # Collect results as they complete
                completed = 0
                for future in as_completed(future_to_task):
                    task = future_to_task[future]
                    try:
                        result = future.result()
                        results.append(result)

                        if result.success:
                            self.stats['successful'] += 1
                        else:
                            self.stats['failed'] += 1

                        self.stats['total_duration'] += result.duration

                    except Exception as e:
                        # Handle compilation errors
                        result = CompilationResult(
                            source_file=task.source_file,
                            output_file=task.output_file,
                            success=False,
                            error=str(e)
                        )
                        results.append(result)
                        self.stats['failed'] += 1

                    # Update progress
                    completed += 1
                    if progress_callback:
                        progress_callback(completed, len(tasks))

        except KeyboardInterrupt:
            print("\nCompilation interrupted by user")
            raise

        self.stats['parallel_duration'] = time.time() - start_time

        return results

    def compile_files_in_batches(
        self,
        tasks: List[CompilationTask],
        compile_func: Callable[[CompilationTask], CompilationResult],
        batch_size: int = 10,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[CompilationResult]:
        """
        Compile files in batches to limit memory usage

        Args:
            tasks: List of compilation tasks
            compile_func: Function that compiles a single task
            batch_size: Number of files to compile per batch
            progress_callback: Optional callback for progress updates

        Returns:
            List of compilation results
        """
        results = []
        total_tasks = len(tasks)

        for i in range(0, total_tasks, batch_size):
            batch = tasks[i:i + batch_size]
            batch_results = self.compile_files(batch, compile_func, progress_callback)
            results.extend(batch_results)

        return results

    def get_stats(self) -> Dict[str, Any]:
        """
        Get compilation statistics

        Returns:
            Dictionary with compilation stats
        """
        stats = self.stats.copy()

        # Calculate speedup
        if stats['parallel_duration'] > 0:
            stats['speedup'] = stats['total_duration'] / stats['parallel_duration']
        else:
            stats['speedup'] = 1.0

        # Calculate average time per file
        if stats['total_files'] > 0:
            stats['avg_time_per_file'] = stats['total_duration'] / stats['total_files']
        else:
            stats['avg_time_per_file'] = 0.0

        return stats

    def reset_stats(self) -> None:
        """Reset compilation statistics"""
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'total_duration': 0.0,
            'parallel_duration': 0.0
        }


# Utility function for simple parallel compilation
def compile_files_parallel(
    source_files: List[str],
    output_dir: str,
    compile_func: Callable[[str, str], bool],
    max_workers: Optional[int] = None,
    verbose: bool = False,
    use_threads: bool = False
) -> bool:
    """
    Simplified parallel compilation helper

    Args:
        source_files: List of source file paths
        output_dir: Output directory for compiled files
        compile_func: Function(source_path, output_path) -> success
        max_workers: Maximum number of workers
        verbose: Print progress information
        use_threads: Use threads instead of processes

    Returns:
        True if all files compiled successfully
    """
    # Create tasks
    tasks = []
    for source in source_files:
        basename = os.path.basename(source)
        name = os.path.splitext(basename)[0]
        output = os.path.join(output_dir, f"{name}.js")
        tasks.append(CompilationTask(source, output, {}))

    # Wrapper for compile_func
    def compile_wrapper(task: CompilationTask) -> CompilationResult:
        start_time = time.time()
        try:
            success = compile_func(task.source_file, task.output_file)
            duration = time.time() - start_time
            return CompilationResult(
                source_file=task.source_file,
                output_file=task.output_file,
                success=success,
                duration=duration
            )
        except Exception as e:
            duration = time.time() - start_time
            return CompilationResult(
                source_file=task.source_file,
                output_file=task.output_file,
                success=False,
                error=str(e),
                duration=duration
            )

    # Progress callback
    def progress(current: int, total: int):
        if verbose:
            percent = (current / total) * 100
            print(f"\rCompiling: {current}/{total} ({percent:.1f}%)", end='', flush=True)

    # Compile
    compiler = ParallelCompiler(max_workers=max_workers, use_threads=use_threads)
    results = compiler.compile_files(tasks, compile_wrapper, progress if verbose else None)

    if verbose:
        print()  # New line after progress
        stats = compiler.get_stats()
        print(f"Compiled {stats['successful']}/{stats['total_files']} files successfully")
        print(f"Time: {stats['parallel_duration']:.2f}s (speedup: {stats['speedup']:.2f}x)")

    # Return True if all succeeded
    return all(r.success for r in results)
