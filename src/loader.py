import contextlib
from typing import AsyncIterator

from fastapi import FastAPI

from config import settings
from src.routes import (create_tweet, create_user, delete_follow, delete_like,
                        delete_tweet, follow, get_tweet, get_user,
                        get_user_by_id, like_tweet, load_media_for_tweet)

from .database.session_manager import db_manager


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init(settings.db.url_db_asyncpg)
    yield
    await db_manager.close()


app: FastAPI = FastAPI(title="Clone twitter", lifespan=lifespan)

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
