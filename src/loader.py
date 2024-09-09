from fastapi import FastAPI
import contextlib
from typing import AsyncIterator
from config import settings
from .database.session_manager import db_manager


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init(settings.database_url)
    yield
    await db_manager.close()


app: FastAPI = FastAPI(
    title="Clone twitter",
    lifespan=lifespan
)
