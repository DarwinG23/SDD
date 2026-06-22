import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_generate_tests_missing_session(client):
    response = await client.post("/api/v1/ai/generate-tests", json={
        "session_id": "nonexistent",
        "prompt": "test prompt",
    })
    assert response.status_code == 404


@pytest.mark.asyncio
@patch("app.services.ai_service.httpx.Client")
async def test_generate_tests_success(mock_client_cls, client):
    content = b"def foo(): return 42"
    files = {"file": ("test.py", content, "text/x-python")}
    data = {"project_name": "TestProj", "prompt": "Contexto:\ncontext\n\nCódigo:\ncode\n\nPruebas:\ntests"}
    upload_resp = await client.post("/api/v1/upload/source", files=files, data=data)
    assert upload_resp.status_code == 200
    session_id = upload_resp.json()["sessionId"]

    mock_instance = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "def test_foo():\n    assert True"}
    mock_instance.post.return_value = mock_response

    response = await client.post("/api/v1/ai/generate-tests", json={
        "session_id": session_id,
        "prompt": "Contexto:\nx\n\nCódigo:\ny\n\nPruebas:\nz",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "test_foo" in body["test_code"]
