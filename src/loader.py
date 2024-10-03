from fastapi import FastAPI
import contextlib
from typing import AsyncIterator
from config import settings
from .database.session_manager import db_manager
from src.routes import (
    create_user, create_tweet,
    get_user, get_user_by_id, get_tweet,
    like_tweet, delete_like, load_media_for_tweet,
    delete_tweet, follow, delete_follow
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

app.include_router(create_user.router)
app.include_router(create_tweet.router)
app.include_router(get_user.router)
app.include_router(get_user_by_id.router)
app.include_router(get_tweet.router)
app.include_router(like_tweet.router)
app.include_router(delete_like.router)
app.include_router(load_media_for_tweet.router)
app.include_router(delete_tweet.router)
app.include_router(follow.router)
app.include_router(delete_follow.router)
