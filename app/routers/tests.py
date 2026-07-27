from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.servicios.test_runner import TestRunner
from app.services.file_storage import FileStorageService


class TestExecuteRequest(BaseModel):
    session_id: str
    source_code: str
    test_code: str


class TestResultResponse(BaseModel):
    success: bool
    passed: int = 0
    failed: int = 0
    stdout: str = ""
    stderr: str = ""
    exit_code: int = -1


router = APIRouter(prefix="/api/v1/tests", tags=["tests"])
test_runner = TestRunner()
file_storage = FileStorageService()
_execution_results: dict[str, dict] = {}


@router.post("/execute", response_model=TestResultResponse)
async def execute_tests(req: TestExecuteRequest):
    source_code = req.source_code
    if not source_code and req.session_id:
        file_path = file_storage.get_file_path(req.session_id)
        if file_path:
            source_code = file_path.read_text(encoding="utf-8")
    raw_result = await test_runner.execute_tests(source_code, req.test_code)
    parsed = test_runner.parse_test_result(raw_result)
    result_id = req.session_id
    _execution_results[result_id] = parsed
    return TestResultResponse(**parsed)


@router.get("/{test_id}/result", response_model=TestResultResponse)
def get_test_result(test_id: str):
    result = _execution_results.get(test_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Resultado de prueba no encontrado")
    return TestResultResponse(**result)
