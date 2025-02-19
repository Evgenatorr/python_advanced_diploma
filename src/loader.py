import contextlib
from typing import AsyncIterator

from fastapi import FastAPI

from logs_conf.log_utils import logger, setup_logging
from logs_conf.logging_conf import LOGGING_CONFIG
from src.routes import (create_media, create_tweet, create_user, delete_follow,
                        delete_like, delete_tweet, follow, get_all_users,
                        get_tweets, get_user, get_user_by_id, like_tweet)
from src.utils.get_db_url import get_database_url

from .database.session_manager import db_manager

setup_logging(LOGGING_CONFIG)


@contextlib.asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    db_manager.init(get_database_url())
    logger.info('База инициализирована')
    yield
    await db_manager.close()


app: FastAPI = FastAPI(title="Clone twitter", lifespan=lifespan)

app.include_router(create_user.router)
app.include_router(create_tweet.router)
app.include_router(get_user.router)
app.include_router(get_user_by_id.router)
app.include_router(get_tweets.router)
app.include_router(like_tweet.router)
app.include_router(delete_like.router)
app.include_router(create_media.router)
app.include_router(delete_tweet.router)
app.include_router(follow.router)
app.include_router(delete_follow.router)
app.include_router(get_all_users.router)
