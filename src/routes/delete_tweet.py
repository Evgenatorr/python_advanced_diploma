from typing import List, cast

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from logs_conf.log_utils import logger
from src.auth.secure_user import get_user_by_secure_key
from src.crud import tweet_crud
from src.database.async_session import get_async_session
from src.database.models.tweet_model import Tweet
from src.schemas import UserResponse
from src.utils.remove_images import del_images

router: APIRouter = APIRouter(tags=["DELETE"])


@router.delete("/api/tweets/{tweet_id}", status_code=status.HTTP_200_OK)
async def delete_tweet(
    tweet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер удаления твита из базы данных
    :param tweet_id: id твита
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """
    logger.debug(
        'Пользователь с id %s удаляет твит',
        current_user.id
    )
    tweet: Tweet | None = await tweet_crud.get(
        session=session, obj_id=tweet_id
    )

    if tweet and tweet.author_id == current_user.id:
        await tweet_crud.delete(session=session, obj_id=tweet_id)
        logger.info(
            'Пользователь с id %s успешно удалил твит с id %s',
            current_user.id, tweet_id
        )
        if tweet.attachments:
            attachments = cast(List[str], tweet.attachments)
            await del_images(medias=attachments)

        return JSONResponse(
            content={
                "result": "true",
            },
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={
            "result": "false",
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )
