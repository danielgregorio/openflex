"""
Incremental Compilation System
Only recompiles files that have changed since last build
"""

import os
import json
import hashlib
from typing import Dict, List, Set, Optional
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class CacheEntry:
    """Cache entry for a compiled file"""
    source_path: str
    output_path: str
    source_hash: str
    dependencies: List[str]  # Files this file imports
    timestamp: float


class IncrementalCompiler:
    """
    Incremental compilation system that tracks file changes and dependencies
    """

    def __init__(self, cache_dir: str = ".openflex-cache"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "build-cache.json")
        self.cache: Dict[str, CacheEntry] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}  # file -> files that depend on it
        self._load_cache()

    def _load_cache(self) -> None:
        """Load compilation cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    for path, entry_dict in data.items():
                        self.cache[path] = CacheEntry(**entry_dict)
                        # Rebuild dependency graph
                        for dep in entry_dict['dependencies']:
                            if dep not in self.dependency_graph:
                                self.dependency_graph[dep] = set()
                            self.dependency_graph[dep].add(path)
            except (json.JSONDecodeError, KeyError):
                # Cache corrupted, start fresh
                self.cache = {}
                self.dependency_graph = {}

    def _save_cache(self) -> None:
        """Save compilation cache to disk"""
        os.makedirs(self.cache_dir, exist_ok=True)
        with open(self.cache_file, 'w') as f:
            cache_dict = {path: asdict(entry) for path, entry in self.cache.items()}
            json.dump(cache_dict, f, indent=2)

    def _compute_file_hash(self, file_path: str) -> str:
        """Compute SHA256 hash of file contents"""
        if not os.path.exists(file_path):
            return ""

        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    def _get_file_timestamp(self, file_path: str) -> float:
        """Get file modification timestamp"""
        if not os.path.exists(file_path):
            return 0.0
        return os.path.getmtime(file_path)

    def needs_recompilation(self, source_path: str) -> bool:
        """
        Check if a file needs to be recompiled

        Returns True if:
        - File is not in cache
        - Source file has been modified (hash changed)
        - Any dependency has been modified
        """
        # Normalize path
        source_path = os.path.abspath(source_path)

        # Not in cache - needs compilation
        if source_path not in self.cache:
            return True

        entry = self.cache[source_path]

        # Source file doesn't exist - skip
        if not os.path.exists(source_path):
            return False

        # Check if source has changed
        current_hash = self._compute_file_hash(source_path)
        if current_hash != entry.source_hash:
            return True

        # Check if any dependency has changed
        for dep in entry.dependencies:
            if self.needs_recompilation(dep):
                return True

        # Check if output file is missing
        if not os.path.exists(entry.output_path):
            return True

        return False

    def get_files_to_recompile(self, source_files: List[str]) -> List[str]:
        """
        Get list of files that need recompilation, including dependents

        Args:
            source_files: List of source files to check

        Returns:
            List of files that need to be recompiled
        """
        to_recompile = set()
        checked = set()

        def check_file(path: str):
            """Recursively check file and its dependents"""
            if path in checked:
                return
            checked.add(path)

            if self.needs_recompilation(path):
                to_recompile.add(path)

                # If this file changed, all files that depend on it need recompilation
                if path in self.dependency_graph:
                    for dependent in self.dependency_graph[path]:
                        check_file(dependent)

        # Check all source files
        for source in source_files:
            check_file(os.path.abspath(source))

        return list(to_recompile)

    def update_cache(
        self,
        source_path: str,
        output_path: str,
        dependencies: Optional[List[str]] = None
    ) -> None:
        """
        Update cache entry for a compiled file

        Args:
            source_path: Path to source file
            output_path: Path to output file
            dependencies: List of files this file depends on (imports)
        """
        source_path = os.path.abspath(source_path)
        output_path = os.path.abspath(output_path)
        dependencies = dependencies or []

        # Compute source hash
        source_hash = self._compute_file_hash(source_path)
        timestamp = self._get_file_timestamp(source_path)

        # Remove old dependency graph entries
        if source_path in self.cache:
            old_entry = self.cache[source_path]
            for dep in old_entry.dependencies:
                if dep in self.dependency_graph:
                    self.dependency_graph[dep].discard(source_path)

        # Create cache entry
        entry = CacheEntry(
            source_path=source_path,
            output_path=output_path,
            source_hash=source_hash,
            dependencies=dependencies,
            timestamp=timestamp
        )

        self.cache[source_path] = entry

        # Update dependency graph
        for dep in dependencies:
            if dep not in self.dependency_graph:
                self.dependency_graph[dep] = set()
            self.dependency_graph[dep].add(source_path)

        # Save cache
        self._save_cache()

    def clear_cache(self) -> None:
        """Clear all cache data"""
        self.cache = {}
        self.dependency_graph = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

    def get_cache_stats(self) -> Dict[str, any]:
        """Get cache statistics"""
        return {
            "total_files": len(self.cache),
            "total_dependencies": sum(len(deps) for deps in self.dependency_graph.values()),
            "cache_size_bytes": os.path.getsize(self.cache_file) if os.path.exists(self.cache_file) else 0
        }

    def invalidate_file(self, source_path: str) -> None:
        """
        Invalidate cache entry for a specific file
        This will force recompilation on next build
        """
        source_path = os.path.abspath(source_path)
        if source_path in self.cache:
            # Remove from cache
            entry = self.cache[source_path]

            # Remove from dependency graph
            for dep in entry.dependencies:
                if dep in self.dependency_graph:
                    self.dependency_graph[dep].discard(source_path)

            del self.cache[source_path]
            self._save_cache()

    def prune_cache(self) -> int:
        """
        Remove cache entries for files that no longer exist
        Returns number of entries removed
        """
        to_remove = []

        for source_path in self.cache:
            if not os.path.exists(source_path):
                to_remove.append(source_path)

        for source_path in to_remove:
            self.invalidate_file(source_path)

        return len(to_remove)
