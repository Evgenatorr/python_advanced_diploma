from fastapi import FastAPI
import contextlib
from fastapi.staticfiles import StaticFiles
from typing import AsyncIterator
from config import settings
from .database.session_manager import db_manager
from src.routes import (
    create_user, create_tweet, home_route,
    get_user, get_user_by_id, get_tweet,
    like_tweet, delete_like, load_media_for_tweet
)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init(settings.db.url_db_asyncpg)
    yield
    await db_manager.close()


app: FastAPI = FastAPI(
    title="Clone twitter",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory=settings.STATIC_PATH, html=True), name="static")

app.include_router(create_user.router)
app.include_router(create_tweet.router)
app.include_router(home_route.router)
app.include_router(get_user.router)
app.include_router(get_user_by_id.router)
app.include_router(get_tweet.router)
app.include_router(like_tweet.router)
app.include_router(delete_like.router)
app.include_router(load_media_for_tweet.router)
