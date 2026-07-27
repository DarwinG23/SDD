from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.servicios.ai_service import AIServicio


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


@router.post("/generate-tests", response_model=GenerateResponse)
def generate_tests(req: GenerateRequest):
    try:
        test_code = ai_service.generate_tests(req.prompt, req.code)
        return GenerateResponse(success=True, test_code=test_code)
    except ValueError as e:
        return GenerateResponse(success=False, error=str(e))
    except Exception as e:
        return GenerateResponse(success=False, error=f"Error al generar pruebas: {str(e)}")


@router.post("/regenerate-tests", response_model=GenerateResponse)
def regenerate_tests(req: GenerateRequest):
    return generate_tests(req)
