from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func

from src import crud, schemas
from src.auth.secure_user import get_user_by_secure_key
from src.database.async_session import get_async_session
from src.database import models
from logs_conf.log_utils import logger

router = APIRouter(tags=["GET"])


@router.get(
    "/api/tweets",
    response_model=schemas.tweet.APITweetListResponseSuccessful,
    status_code=status.HTTP_200_OK,
)
async def get_tweets(
        current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key),
        session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """
    Роутер для получения всех твитов пользователя вместе с твитами на кого подписан user
    :param current_user: пользователь прошедший аутентификацию
    :param session: асинхронная сессия базы данных
    :return: JSONResponse
    """

    user_in_db: models.user_model.User | None = await crud.user.user_crud.get(
        session=session, user_id=current_user.id
    )
    if user_in_db is None:
        logger.debug('Пользователь не найден')
        return JSONResponse(
            content={
                "result": "false",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Получаем список пользователей, на которых подписан текущий пользователь
    following_ids: list = [f.id for f in user_in_db.following]
    # Включаем твиты пользователя и тех, на кого он подписан
    all_user_ids: list[int] = [current_user.id] + following_ids

    tweets_with_likes = await crud.tweet.tweet_crud.get_tweets_with_tweets_you_follow(
        session=session, users_id=all_user_ids
    )
    if not tweets_with_likes:
        return JSONResponse(
            content={"result": "false"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Преобразуем результат в список для ответа
    response_model = [
        schemas.tweet.TweetResponse.model_validate(tweet).model_dump()
        for tweet in tweets_with_likes
    ]

    return JSONResponse(
        content={
            "result": "true",
            "tweets": response_model,
        },
        status_code=status.HTTP_200_OK,
    )
