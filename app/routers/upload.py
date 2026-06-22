from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.services import file_storage
from app.services.validation import validate_python_syntax

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/page", include_in_schema=False)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/source")
async def upload_source(
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
        file_path = file_storage.store_file(session_id, file_content, file.filename or "source.py")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    validation_result = validate_python_syntax(file_path)

    if not validation_result["valid"]:
        file_storage.cleanup_session(session_id)
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


@router.delete("/source/{session_id}")
async def delete_upload(session_id: str):
    file_storage.cleanup_session(session_id)
    return {"message": "Session cleaned up"}
