import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_upload_valid_file(client):
    content = b"def foo(): return 42"
    files = {"file": ("test.py", content, "text/x-python")}
    data = {"project_name": "TestProj", "prompt": "context code tests"}
    response = await client.post("/api/v1/upload/source", files=files, data=data)
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["uploadId"] is not None
    assert body["projectName"] == "TestProj"


@pytest.mark.asyncio
async def test_upload_invalid_extension(client):
    files = {"file": ("test.txt", b"hello", "text/plain")}
    data = {"project_name": "P", "prompt": "context code tests"}
    response = await client.post("/api/v1/upload/source", files=files, data=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_syntax_error(client):
    content = b"def foo(:\n"
    files = {"file": ("broken.py", content, "text/x-python")}
    data = {"project_name": "P", "prompt": "context code tests"}
    response = await client.post("/api/v1/upload/source", files=files, data=data)
    assert response.status_code == 422
    body = response.json()
    assert body["valid"] is False
    assert len(body["errors"]) > 0


@pytest.mark.asyncio
async def test_cleanup_endpoint(client):
    session_id = "integration-cleanup-test"
    response = await client.delete(f"/api/v1/upload/source/{session_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Session cleaned up"
