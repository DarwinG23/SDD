from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import file_storage
from app.services.ai_service import generate_tests

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


class GenerateRequest(BaseModel):
    session_id: str
    prompt: str


class GenerateResponse(BaseModel):
    success: bool
    test_code: str | None = None
    error: str | None = None


@router.post("/generate-tests", response_model=GenerateResponse)
async def generate_tests_endpoint(req: GenerateRequest):
    file_path = file_storage.get_file_path(req.session_id)
    if file_path is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    code = file_path.read_text(encoding="utf-8")

    try:
        test_code = generate_tests(req.prompt, code)
        return GenerateResponse(success=True, test_code=test_code)
    except ValueError as e:
        return GenerateResponse(success=False, error=str(e))
    except Exception as e:
        return GenerateResponse(success=False, error=f"Error al generar pruebas: {str(e)}")
