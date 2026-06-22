from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import upload
from app.services.file_storage import cleanup_old_sessions


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def periodic_cleanup():
        while True:
            cleanup_old_sessions(max_age_seconds=3600)
            await asyncio.sleep(1800)

    task = asyncio.create_task(periodic_cleanup())
    yield
    task.cancel()


app = FastAPI(title="SmartUnitTest", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(upload.router)
