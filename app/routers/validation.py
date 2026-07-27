from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from pathlib import Path

from app.negocio.validation.validation_service import NegocioValidationService


class CodeValidationRequest(BaseModel):
    file_path: str


class PromptValidationRequest(BaseModel):
    prompt: str
    template_name: str = "default"


router = APIRouter(prefix="/api/v1/validation", tags=["validation"])
validation_service = NegocioValidationService()


@router.post("/code")
def validate_code(req: CodeValidationRequest):
    if not Path(req.file_path).exists():
        raise HTTPException(status_code=404, detail="File not found")
    result = validation_service.validate_python_syntax(req.file_path)
    return result


@router.post("/prompt")
def validate_prompt(req: PromptValidationRequest):
    result = validation_service.validate_prompt_structure(req.prompt, req.template_name)
    return result
