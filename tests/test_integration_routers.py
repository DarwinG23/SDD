import tempfile
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_validation_code_endpoint_without_file(client):
    response = await client.post("/api/v1/validation/code", json={"file_path": "/nonexistent/test.py"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_validation_prompt_endpoint(client):
    response = await client.post("/api/v1/validation/prompt", json={"prompt": "context code tests", "template_name": "default"})
    assert response.status_code == 200
    body = response.json()
    assert "valid" in body


@pytest.mark.asyncio
async def test_ai_generate_tests_endpoint(client):
    response = await client.post("/api/v1/ai/generate-tests", json={
        "session_id": "test-session",
        "prompt": "test prompt",
        "code": "def foo(): pass",
    })
    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_tests_execute_endpoint(client):
    response = await client.post("/api/v1/tests/execute", json={
        "session_id": "test",
        "source_code": "def foo(): return 42",
        "test_code": "def test_foo(): pass",
    })
    assert response.status_code == 200
    body = response.json()
    assert "success" in body


@pytest.mark.asyncio
async def test_evaluation_run_endpoint_not_found(client):
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write("def foo(): return 42\n")
        f.flush()
        response = await client.post("/api/v1/evaluation/run", json={
            "source_path": f.name,
            "test_code": "def test_foo(): pass",
        })
    assert response.status_code in (200, 503)


@pytest.mark.asyncio
async def test_reports_generate_endpoint(client):
    response = await client.post("/api/v1/reports/generate", json={
        "evaluation_results": {"all_passed": True},
        "test_code": "def test(): pass",
    })
    assert response.status_code == 200
    body = response.json()
    assert "report_id" in body


@pytest.mark.asyncio
async def test_reports_download_not_found(client):
    response = await client.get("/api/v1/reports/nonexistent/download")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_evaluation_get_not_found(client):
    response = await client.get("/api/v1/evaluation/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_tests_result_not_found(client):
    response = await client.get("/api/v1/tests/nonexistent/result")
    assert response.status_code == 404
