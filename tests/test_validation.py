import pytest
from app.services.validation import validate_python_syntax
import tempfile


class TestValidation:

    def test_valid_python(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("def foo():\n    return 42\n")
            f.flush()
            result = validate_python_syntax(f.name)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_invalid_python_syntax(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("def foo(:\n")
            f.flush()
            result = validate_python_syntax(f.name)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "invalid syntax" in result["errors"][0]["message"].lower()
