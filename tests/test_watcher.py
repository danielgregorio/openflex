"""
Tests for file watcher
"""

import os
import pytest
import tempfile
import time
from pathlib import Path

from compiler.watcher import FileWatcher, FileState


class TestFileWatcher:
    """Tests for file watching functionality"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def watcher(self):
        """Create file watcher instance"""
        return FileWatcher(poll_interval=0.1)

    def test_file_state_change_detection(self):
        """Test FileState can detect changes"""
        state = FileState(path="test.as4", mtime=1000.0, size=100)

        # No change
        assert not state.has_changed(1000.0, 100)

        # Modified time changed
        assert state.has_changed(1001.0, 100)

        # Size changed
        assert state.has_changed(1000.0, 101)

        # Both changed
        assert state.has_changed(1001.0, 101)

    def test_watch_single_file(self, watcher, temp_dir):
        """Test watching a single file"""
        # Create test file
        test_file = os.path.join(temp_dir, "test.as4")
        with open(test_file, 'w') as f:
            f.write("var x = 10;")

        # Track callback invocations
        callbacks = []

        def callback(path):
            callbacks.append(path)

        # Watch file
        watcher.watch(test_file, callback)

        assert test_file in watcher.watched_files
        assert test_file in watcher.callbacks

    def test_watch_nonexistent_file(self, watcher):
        """Test watching non-existent file raises error"""
        with pytest.raises(FileNotFoundError):
            watcher.watch("/nonexistent/file.as4", lambda p: None)

    def test_detect_file_change(self, watcher, temp_dir):
        """Test detecting file changes"""
        # Create test file
        test_file = os.path.join(temp_dir, "test.as4")
        with open(test_file, 'w') as f:
            f.write("var x = 10;")

        watcher.watch(test_file, lambda p: None)

        # No changes initially
        changes = watcher.check_changes()
        assert len(changes) == 0

        # Modify file
        time.sleep(0.01)  # Ensure mtime changes
        with open(test_file, 'w') as f:
            f.write("var x = 20;")

        # Detect change
        changes = watcher.check_changes()
        assert test_file in changes

        # No further changes
        changes = watcher.check_changes()
        assert len(changes) == 0

    def test_watch_directory(self, watcher, temp_dir):
        """Test watching all files in a directory"""
        # Create multiple test files
        files = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"test{i}.as4")
            with open(file_path, 'w') as f:
                f.write(f"var x{i} = {i};")
            files.append(file_path)

        # Watch directory
        watcher.watch_directory(temp_dir, pattern="*.as4", callback=lambda p: None)

        # All files should be watched
        assert len(watcher.watched_files) == 3

        for file_path in files:
            assert file_path in watcher.watched_files

    def test_watch_directory_recursive(self, watcher, temp_dir):
        """Test watching directory recursively"""
        # Create subdirectory
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)

        # Create files in both directories
        main_file = os.path.join(temp_dir, "main.as4")
        sub_file = os.path.join(subdir, "sub.as4")

        with open(main_file, 'w') as f:
            f.write("var main = 1;")

        with open(sub_file, 'w') as f:
            f.write("var sub = 2;")

        # Watch recursively
        watcher.watch_directory(temp_dir, pattern="*.as4", callback=lambda p: None, recursive=True)

        # Both files should be watched
        assert len(watcher.watched_files) == 2
        assert main_file in watcher.watched_files
        assert sub_file in watcher.watched_files

    def test_watch_directory_non_recursive(self, watcher, temp_dir):
        """Test watching directory without recursion"""
        # Create subdirectory
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)

        # Create files in both directories
        main_file = os.path.join(temp_dir, "main.as4")
        sub_file = os.path.join(subdir, "sub.as4")

        with open(main_file, 'w') as f:
            f.write("var main = 1;")

        with open(sub_file, 'w') as f:
            f.write("var sub = 2;")

        # Watch non-recursively
        watcher.watch_directory(temp_dir, pattern="*.as4", callback=lambda p: None, recursive=False)

        # Only main file should be watched
        assert len(watcher.watched_files) == 1
        assert main_file in watcher.watched_files
        assert sub_file not in watcher.watched_files

    def test_multiple_file_changes(self, watcher, temp_dir):
        """Test detecting changes to multiple files"""
        # Create multiple files
        files = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"test{i}.as4")
            with open(file_path, 'w') as f:
                f.write(f"var x{i} = {i};")
            files.append(file_path)
            watcher.watch(file_path, lambda p: None)

        # Modify two files
        time.sleep(0.01)
        with open(files[0], 'w') as f:
            f.write("var x0 = 100;")

        with open(files[2], 'w') as f:
            f.write("var x2 = 200;")

        # Detect changes
        changes = watcher.check_changes()
        assert len(changes) == 2
        assert files[0] in changes
        assert files[2] in changes
        assert files[1] not in changes
