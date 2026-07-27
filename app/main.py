from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.controllers.upload_controller import UploadController
from app.controllers.ai_controller import AIController
from app.services.file_storage import FileStorageService
from app.services.validation import ValidationService
from app.services.ai_service import AIService

from app.routers import validation as validation_router
from app.routers import ai as ai_router
from app.routers import tests as tests_router
from app.routers import evaluation as evaluation_router
from app.routers import reports as reports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    file_storage = FileStorageService()

    async def periodic_cleanup():
        while True:
            file_storage.cleanup_old_sessions(max_age_seconds=3600)
            await asyncio.sleep(1800)

    task = asyncio.create_task(periodic_cleanup())
    yield
    task.cancel()


app = FastAPI(title="SmartUnitTest", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

file_storage = FileStorageService()
validation = ValidationService()
ai_service = AIService()

upload_controller = UploadController(file_storage, validation)
ai_controller = AIController(file_storage, ai_service)

app.include_router(upload_controller.router)
app.include_router(ai_controller.router)

app.include_router(validation_router.router)
app.include_router(ai_router.router)
app.include_router(tests_router.router)
app.include_router(evaluation_router.router)
app.include_router(reports_router.router)
