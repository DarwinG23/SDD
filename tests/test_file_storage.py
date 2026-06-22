import pytest
import tempfile
import os
from pathlib import Path

from app.services.file_storage import (
    store_file,
    get_file_path,
    cleanup_session,
    cleanup_old_sessions,
)


class TestFileStorage:

    def test_store_valid_py_file(self):
        session_id = "test-session-1"
        content = b"print('hello')"
        path = store_file(session_id, content, "script.py")
        assert path.exists()
        assert path.suffix == ".py"
        assert path.read_bytes() == content
        cleanup_session(session_id)

    def test_rejects_non_py_extension(self):
        with pytest.raises(ValueError, match="not allowed"):
            store_file("s", b"x", "file.txt")

    def test_rejects_excessive_size(self):
        big = b"x" * (2 * 1024 * 1024 * 1024 + 1)
        with pytest.raises(ValueError, match="2 GB"):
            store_file("s", big, "code.py")

    def test_sanitized_filename(self):
        session_id = "test-sanitize"
        path = store_file(session_id, b"x", "../malicious.py")
        assert ".." not in path.name
        assert path.suffix == ".py"
        assert len(path.stem) == 32
        cleanup_session(session_id)

    def test_get_file_path_returns_none_for_unknown(self):
        assert get_file_path("nonexistent") is None

    def test_cleanup_session_removes_directory(self):
        session_id = "test-cleanup"
        store_file(session_id, b"x", "f.py")
        session_path = Path("/tmp/smartunittest/uploads") / session_id
        assert session_path.exists()
        cleanup_session(session_id)
        assert not session_path.exists()

    def test_cleanup_old_sessions(self):
        session_id = "test-old"
        store_file(session_id, b"x", "f.py")
        session_path = Path("/tmp/smartunittest/uploads") / session_id
        old_time = __import__("time").time() - 7200
        os.utime(session_path, (old_time, old_time))
        count = cleanup_old_sessions(max_age_seconds=3600)
        assert count >= 1
        assert not session_path.exists()
