import pytest
import tempfile
from app.negocio.validation.validation_service import NegocioValidationService


@pytest.fixture
def validator():
    return NegocioValidationService()


class TestNegocioValidation:

    def test_valid_python_syntax(self, validator):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("def foo():\n    return 42\n")
            f.flush()
            result = validator.validate_python_syntax(f.name)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_invalid_python_syntax(self, validator):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("def foo(:\n")
            f.flush()
            result = validator.validate_python_syntax(f.name)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_valid_prompt_structure(self, validator):
        result = validator.validate_prompt_structure("context here code here tests here")
        assert result["valid"] is True

    def test_invalid_prompt_structure(self, validator):
        result = validator.validate_prompt_structure("just some text")
        assert result["valid"] is False
        assert len(result["errors"]) > 0
