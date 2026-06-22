from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.file_storage import FileStorageService
from app.services.ai_service import AIService


class GenerateRequest(BaseModel):
    session_id: str
    prompt: str


class GenerateResponse(BaseModel):
    success: bool
    test_code: str | None = None
    error: str | None = None


class AIController:
    def __init__(
        self,
        file_storage: FileStorageService,
        ai_service: AIService,
    ):
        self.file_storage = file_storage
        self.ai_service = ai_service
        self.router = APIRouter(prefix="/api/v1/ai", tags=["ai"])
        self._register_routes()

    def _register_routes(self):
        self.router.post("/generate-tests", response_model=GenerateResponse)(self.generate_tests_endpoint)

    async def generate_tests_endpoint(self, req: GenerateRequest):
        file_path = self.file_storage.get_file_path(req.session_id)
        if file_path is None:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")

        code = file_path.read_text(encoding="utf-8")

        try:
            test_code = self.ai_service.generate_tests(req.prompt, code)
            return GenerateResponse(success=True, test_code=test_code)
        except ValueError as e:
            return GenerateResponse(success=False, error=str(e))
        except Exception as e:
            return GenerateResponse(success=False, error=f"Error al generar pruebas: {str(e)}")
