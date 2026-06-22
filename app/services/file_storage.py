import os
import uuid
import shutil
from pathlib import Path

UPLOAD_BASE_DIR = Path("/tmp/smartunittest/uploads")

ALLOWED_EXTENSIONS = {".py"}
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024


def _sanitize_filename(original_filename: str) -> str:
    ext = Path(original_filename).suffix.lower()
    return f"{uuid.uuid4().hex}{ext}"


def _session_dir(session_id: str) -> Path:
    return UPLOAD_BASE_DIR / session_id


def store_file(session_id: str, file_content: bytes, original_filename: str) -> Path:
    ext = Path(original_filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension '{ext}' not allowed. Only .py files are accepted.")

    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError("File exceeds the 2 GB limit.")

    session_path = _session_dir(session_id)
    session_path.mkdir(parents=True, exist_ok=True)

    safe_name = _sanitize_filename(original_filename)
    file_path = session_path / safe_name

    file_path.write_bytes(file_content)

    return file_path


def get_file_path(session_id: str) -> Path | None:
    session_path = _session_dir(session_id)
    if not session_path.exists():
        return None
    files = list(session_path.iterdir())
    if not files:
        return None
    return files[0]


def cleanup_session(session_id: str) -> None:
    session_path = _session_dir(session_id)
    if session_path.exists():
        shutil.rmtree(session_path)


def cleanup_old_sessions(max_age_seconds: int = 3600) -> int:
    now = __import__("time").time()
    removed = 0
    if not UPLOAD_BASE_DIR.exists():
        return 0
    for entry in UPLOAD_BASE_DIR.iterdir():
        if entry.is_dir():
            mtime = entry.stat().st_mtime
            if now - mtime > max_age_seconds:
                shutil.rmtree(entry)
                removed += 1
    return removed
