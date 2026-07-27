import pytest
from app.servicios.test_runner import TestRunner


@pytest.fixture
def runner():
    return TestRunner()


@pytest.mark.asyncio
async def test_parse_test_result_success(runner):
    raw = {
        "success": True,
        "stdout": "collected 1 item\n\nPASSED\n",
        "stderr": "",
        "exit_code": 0,
    }
    result = runner.parse_test_result(raw)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_parse_test_result_failure(runner):
    raw = {
        "success": False,
        "stdout": "FAILED test.py::test_foo\n",
        "stderr": "",
        "exit_code": 1,
    }
    result = runner.parse_test_result(raw)
    assert result["success"] is False
