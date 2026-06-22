import pytest
from unittest.mock import patch, MagicMock

from app.services.ai_service import generate_tests, _extract_code_block


class TestAiService:

    def test_extract_code_block_with_markers(self):
        text = "```python\ndef test_foo():\n    pass\n```"
        result = _extract_code_block(text)
        assert result == "def test_foo():\n    pass"

    def test_extract_code_block_without_markers(self):
        text = "def test_foo():\n    pass"
        result = _extract_code_block(text)
        assert result == text

    def test_extract_code_block_empty(self):
        assert _extract_code_block("") == ""

    @patch("app.services.ai_service.httpx.Client")
    def test_generate_tests_success(self, mock_client_cls):
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "```python\ndef test_foo():\n    assert True\n```"}
        mock_instance.post.return_value = mock_response

        result = generate_tests("test prompt", "def foo(): pass")

        assert "def test_foo()" in result
        mock_instance.post.assert_called_once()

    @patch("app.services.ai_service.httpx.Client")
    def test_generate_tests_connection_error(self, mock_client_cls):
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        from httpx import ConnectError
        mock_instance.post.side_effect = ConnectError("Connection refused")

        with pytest.raises(ValueError, match="Ollama"):
            generate_tests("prompt", "code")
