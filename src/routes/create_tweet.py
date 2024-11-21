from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.auth.secure_user import get_user_by_secure_key
from src.database import models
from src.database.async_session import get_async_session
from logs_conf.log_utils import logger

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

    async def get_media_if_exists(tweet_media_ids: list[int]) -> models.media_model.Media | None:
        """
        Вспомогательная локальная функция, которая возвращает объект media из базы данных,
        если пользователь добавил картинку
        :param tweet_media_ids: id картинки
        :return: Media
        """
        if not tweet_media_ids:
            return None

        return await crud.media.media_crud.get(
            session=session, id=tweet_data.tweet_media_ids
        )

    async def get_tweet_data(content: str, attachments: List[str]) -> schemas.tweet.TweetBase:
        """
        Вспомогательная локальная функция, которая возвращает корректные данные твита
        """
        valid_payload: dict[str, str | list[str] | None] = {
            "content": content,
            "attachments": attachments,
        }
        return schemas.tweet.TweetBase(**valid_payload)

    media: models.media_model.Media | None = await get_media_if_exists(
        tweet_media_ids=tweet_data.tweet_media_ids
    )
    media_link: List[str] | None = [media.file_link] if media else None

    valid_tweet_data: schemas.tweet.TweetBase = await get_tweet_data(
        content=tweet_data.tweet_data,
        attachments=media_link,
    )

    new_tweet: models.tweet_model.Tweet = await crud.tweet.tweet_crud.post_with_author_id(
        session=session,
        tweet_data=valid_tweet_data.model_dump(exclude_unset=True),
        author_id=current_user.id,
    )

    if media:
        media.tweet_id = new_tweet.id
        await session.commit()
    logger.debug('Твит создан')

    return JSONResponse(
        content={
            "result": "true",
            "tweet_id": new_tweet.id,
        },
        status_code=status.HTTP_201_CREATED,
    )
