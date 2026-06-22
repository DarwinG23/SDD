import pytest
from unittest.mock import patch, MagicMock

from app.services.ai_service import AIService


@pytest.fixture
def ai_service():
    return AIService()


class TestAiService:

    def test_extract_code_block_with_markers(self, ai_service):
        text = "```python\ndef test_foo():\n    pass\n```"
        result = ai_service._extract_code_block(text)
        assert result == "def test_foo():\n    pass"

    def test_extract_code_block_without_markers(self, ai_service):
        text = "def test_foo():\n    pass"
        result = ai_service._extract_code_block(text)
        assert result == text

    def test_extract_code_block_empty(self, ai_service):
        assert ai_service._extract_code_block("") == ""

    @patch("app.services.ai_service.httpx.Client")
    def test_generate_tests_success(self, mock_client_cls, ai_service):
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "```python\ndef test_foo():\n    assert True\n```"}
        mock_instance.post.return_value = mock_response

        result = ai_service.generate_tests("test prompt", "def foo(): pass")

        assert "def test_foo()" in result
        mock_instance.post.assert_called_once()

    @patch("app.services.ai_service.httpx.Client")
    def test_generate_tests_connection_error(self, mock_client_cls, ai_service):
        mock_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_instance
        from httpx import ConnectError
        mock_instance.post.side_effect = ConnectError("Connection refused")

        with pytest.raises(ValueError, match="Ollama"):
            ai_service.generate_tests("prompt", "code")
