from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.auth.secure_user import get_user_by_secure_key
from src.database import models
from src.database.async_session import get_async_session
from logs_conf.utils import logger

router = APIRouter(tags=["POST"])


@router.post("/api/tweets", status_code=status.HTTP_201_CREATED,
             description='Роутер для создания нового твита')
async def create_tweet(
    tweet_data: schemas.tweet.TweetCreateRequest,
    session: AsyncSession = Depends(get_async_session),
    current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер для создания нового твита
    :param tweet_data: данные нового твита
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """

    media: models.media_model.Media | None = await crud.media.media_crud.get(
        session=session, media_id=tweet_data.tweet_media_ids
    ) if tweet_data.tweet_media_ids else None

    media_link: List[str] | None = [media.file_link] if media else None

    data_dict: dict[str, str | list[str] | None] = {
        "content": tweet_data.tweet_data,
        "attachments": media_link,
    }

    data: schemas.tweet.TweetBase = schemas.tweet.TweetBase(**data_dict)

    tweet: models.tweet_model.Tweet = await crud.tweet.tweet_crud.post(
        session=session,
        tweet_data=data.model_dump(exclude_unset=True),
        author_id=current_user.id,
    )
    if media:
        media.tweet_id = tweet.id
        await session.commit()
    logger.debug('Твит создан')
    return JSONResponse(
        content={
            "result": "true",
            "tweet_id": tweet.id,
        },
        status_code=status.HTTP_201_CREATED,
    )
