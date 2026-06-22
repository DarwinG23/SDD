from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.services.file_storage import FileStorageService
from app.services.validation import ValidationService


class UploadController:
    def __init__(
        self,
        file_storage: FileStorageService,
        validation: ValidationService,
    ):
        self.file_storage = file_storage
        self.validation = validation
        self.router = APIRouter(prefix="/api/v1/upload", tags=["upload"])
        self.templates = Jinja2Templates(directory="app/templates")
        self._register_routes()

    def _register_routes(self):
        self.router.get("/page", include_in_schema=False)(self.upload_page)
        self.router.post("/source")(self.upload_source)
        self.router.delete("/source/{session_id}")(self.delete_upload)

    async def upload_page(self, request: Request):
        return self.templates.TemplateResponse("upload.html", {"request": request})

    async def upload_source(
        self,
        request: Request,
        file: UploadFile = File(...),
        project_name: str = Form(...),
        prompt: str = Form(...),
    ):
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = __import__("uuid").uuid4().hex

        file_content = await file.read()

        try:
            file_path = self.file_storage.store_file(
                session_id, file_content, file.filename or "source.py"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        validation_result = self.validation.validate_python_syntax(file_path)

        if not validation_result["valid"]:
            self.file_storage.cleanup_session(session_id)
            return JSONResponse(
                content={
                    "valid": False,
                    "uploadId": None,
                    "sessionId": session_id,
                    "errors": validation_result["errors"],
                },
                status_code=422,
                headers={"Set-Cookie": f"session_id={session_id}; Path=/; HttpOnly; SameSite=Lax"},
            )

        upload_id = file_path.stem

        return JSONResponse(
            content={
                "valid": True,
                "uploadId": upload_id,
                "sessionId": session_id,
                "projectName": project_name,
                "prompt": prompt,
            },
            headers={"Set-Cookie": f"session_id={session_id}; Path=/; HttpOnly; SameSite=Lax"},
        )

    async def delete_upload(self, session_id: str):
        self.file_storage.cleanup_session(session_id)
        return {"message": "Session cleaned up"}
