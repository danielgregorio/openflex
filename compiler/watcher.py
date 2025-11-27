"""
OpenFlex Neo - File Watcher
Auto-recompile on file changes for rapid development
"""

import os
import time
import hashlib
from pathlib import Path
from typing import Dict, Callable, Set, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileState:
    """Track file state for change detection"""
    path: str
    mtime: float
    size: int
    hash: Optional[str] = None

    def has_changed(self, current_mtime: float, current_size: int) -> bool:
        """Check if file has changed"""
        return self.mtime != current_mtime or self.size != current_size


class FileWatcher:
    """Watch files for changes and trigger callbacks"""

    def __init__(self, poll_interval: float = 0.5):
        """
        Initialize file watcher

        Args:
            poll_interval: How often to check for changes (in seconds)
        """
        self.poll_interval = poll_interval
        self.watched_files: Dict[str, FileState] = {}
        self.callbacks: Dict[str, Callable] = {}
        self.is_running = False

    def watch(self, file_path: str, callback: Callable) -> None:
        """
        Watch a file for changes

        Args:
            file_path: Path to file to watch
            callback: Function to call when file changes
        """
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot watch non-existent file: {file_path}")

        # Get initial state
        stat = os.stat(file_path)
        self.watched_files[file_path] = FileState(
            path=file_path,
            mtime=stat.st_mtime,
            size=stat.st_size
        )

        self.callbacks[file_path] = callback

    def watch_directory(
        self,
        directory: str,
        pattern: str = "*.as4",
        callback: Callable = None,
        recursive: bool = True
    ) -> None:
        """
        Watch all files in a directory

        Args:
            directory: Directory to watch
            pattern: Glob pattern for files to watch
            callback: Callback for file changes
            recursive: Watch subdirectories
        """
        directory = os.path.abspath(directory)
        path = Path(directory)

        if recursive:
            files = path.rglob(pattern)
        else:
            files = path.glob(pattern)

        for file_path in files:
            if file_path.is_file():
                self.watch(str(file_path), callback)

    def check_changes(self) -> Set[str]:
        """
        Check all watched files for changes

        Returns:
            Set of file paths that have changed
        """
        changed_files = set()

        for file_path, file_state in self.watched_files.items():
            if not os.path.exists(file_path):
                # File was deleted
                continue

            stat = os.stat(file_path)
            if file_state.has_changed(stat.st_mtime, stat.st_size):
                # File has changed
                changed_files.add(file_path)

                # Update state
                self.watched_files[file_path] = FileState(
                    path=file_path,
                    mtime=stat.st_mtime,
                    size=stat.st_size
                )

        return changed_files

    def run(self, on_start: Optional[Callable] = None) -> None:
        """
        Start watching files

        Args:
            on_start: Optional callback to run when watcher starts
        """
        self.is_running = True

        if on_start:
            on_start()

        print(f"👀 Watching {len(self.watched_files)} file(s) for changes...")
        print("   Press Ctrl+C to stop")
        print()

        try:
            while self.is_running:
                changed_files = self.check_changes()

                for file_path in changed_files:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] 📝 Change detected: {file_path}")

                    callback = self.callbacks.get(file_path)
                    if callback:
                        try:
                            callback(file_path)
                        except Exception as e:
                            print(f"   ❌ Error: {e}")

                time.sleep(self.poll_interval)

        except KeyboardInterrupt:
            print()
            print("👋 Stopping file watcher...")
            self.is_running = False

    def stop(self) -> None:
        """Stop watching files"""
        self.is_running = False


def get_file_hash(file_path: str) -> str:
    """Get MD5 hash of file contents"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
