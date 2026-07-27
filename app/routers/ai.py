from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.servicios.ai_service import AIServicio
from app.services.file_storage import FileStorageService


class GenerateRequest(BaseModel):
    session_id: str
    prompt: str
    code: str


class GenerateResponse(BaseModel):
    success: bool
    test_code: str | None = None
    error: str | None = None


router = APIRouter(prefix="/api/v1/ai", tags=["ai"])
ai_service = AIServicio()
file_storage = FileStorageService()


@router.post("/generate-tests", response_model=GenerateResponse)
def generate_tests(req: GenerateRequest):
    try:
        source_code = req.code or _read_source_from_session(req.session_id)
        test_code = ai_service.generate_tests(req.prompt, source_code)
        return GenerateResponse(success=True, test_code=test_code)
    except ValueError as e:
        return GenerateResponse(success=False, error=str(e))
    except Exception as e:
        return GenerateResponse(success=False, error=f"Error al generar pruebas: {str(e)}")


@router.post("/regenerate-tests", response_model=GenerateResponse)
def regenerate_tests(req: GenerateRequest):
    return generate_tests(req)


def _read_source_from_session(session_id: str) -> str:
    file_path = file_storage.get_file_path(session_id)
    if not file_path:
        raise ValueError("Archivo fuente no encontrado. Debes subir un archivo primero.")
    return file_path.read_text(encoding="utf-8")
