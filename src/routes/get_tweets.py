from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import user_crud, tweet_crud
from src.schemas import APITweetListResponseSuccessful, UserResponse, TweetResponse
from src.auth.secure_user import get_user_by_secure_key
from src.database.async_session import get_async_session
from src.database.models import user_model
from logs_conf.log_utils import logger


router = APIRouter(tags=["GET"])


@router.get(
    "/api/tweets",
    response_model=APITweetListResponseSuccessful,
    status_code=status.HTTP_200_OK,
)
async def get_tweets(
        current_user: UserResponse = Depends(get_user_by_secure_key),
        session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """
    Роутер для получения всех твитов пользователя вместе с твитами на кого подписан user
    :param current_user: пользователь прошедший аутентификацию
    :param session: асинхронная сессия базы данных
    :return: JSONResponse
    """
    logger.debug('Выводим все твиты')
    user_in_db: user_model.User | None = await user_crud.get_with_lazy_load(
        session=session, user_id=current_user.id
    )
    if user_in_db is None:
        logger.info('Пользователь не найден')
        return JSONResponse(
            content={
                "result": "false",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Получаем список с id пользователей, на которых подписан текущий пользователь
    following_ids: List[int] = [f.id for f in user_in_db.following]
    # Включаем твиты пользователя и тех, на кого он подписан
    all_user_ids: List[int] = [current_user.id] + following_ids

    tweets_with_likes = await tweet_crud.get_tweets_with_tweets_you_follow(
        session=session, users_id=all_user_ids
    )
    if not tweets_with_likes:
        return JSONResponse(
            content={"result": "false"},
        )

    response_model: APITweetListResponseSuccessful = APITweetListResponseSuccessful(
        tweets=[
            TweetResponse.model_validate(tweet)
            for tweet in tweets_with_likes
        ]
    )
    logger.info('Все твиты успешно получены')
    return JSONResponse(
        content=response_model.model_dump(),
        status_code=status.HTTP_200_OK,
    )
