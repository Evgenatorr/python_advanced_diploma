from typing import List, Sequence

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from logs_conf.log_utils import logger
from src.auth.secure_user import get_user_by_secure_key
from src.crud import media_crud, tweet_crud
from src.database.async_session import get_async_session
from src.database.models import media_model, tweet_model
from src.schemas import TweetCreate, TweetCreateRequest, UserResponse

router = APIRouter(tags=["POST"])


@router.post("/api/tweets", status_code=status.HTTP_201_CREATED,
             description='Роутер для создания нового твита')
async def create_tweet(
        tweet_data: TweetCreateRequest,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер для создания нового твита
    :param tweet_data: данные нового твита
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """
    logger.debug('Пользователь с id %s создаёт твит', current_user.id)

    medias: Sequence[media_model.Media] | None = await media_crud.get_list_by_media_ids(
        session=session,
        media_ids=tweet_data.tweet_media_ids
    )
    media_links: List[str] | None = [
        media.file_link for media in medias
    ] if medias else None

    create_tweet_data: TweetCreate = TweetCreate(
        content=tweet_data.tweet_data,
        attachments=media_links,
        author_id=current_user.id
    )

    new_tweet: tweet_model.Tweet = await tweet_crud.post(
        session=session,
        obj_in_data=create_tweet_data.model_dump(exclude_unset=True),
    )

    if medias:
        for media in medias:
            media.tweet_id = new_tweet.id
        await session.commit()
    logger.info(
        'Пользователь с id %s создал твит с id %s', current_user.id, new_tweet.id
    )
    return JSONResponse(
        content={
            "result": "true",
            "tweet_id": new_tweet.id,
        },
        status_code=status.HTTP_201_CREATED,
    )
