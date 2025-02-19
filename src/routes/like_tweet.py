from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from logs_conf.log_utils import logger
from src.auth.secure_user import get_user_by_secure_key
from src.crud import like_crud, tweet_crud
from src.database.async_session import get_async_session
from src.database.models import tweet_model, like_model
from src.schemas import UserResponse, APIBaseSuccessfulSchema

router: APIRouter = APIRouter(tags=["POST"])


@router.post("/api/tweets/{tweet_id}/likes", status_code=status.HTTP_201_CREATED,
             response_model=APIBaseSuccessfulSchema)
async def like_tweet(
        tweet_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер для добавления нового лайка от пользователя в базу данных
    :param tweet_id: id твита
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """

    logger.debug('Пользователь с id %s '
                 'ставит лайк', current_user.id)
    tweet: tweet_model.Tweet | None = await tweet_crud.get(
        session=session, obj_id=tweet_id
    )

    if not tweet:
        return JSONResponse(
            content={
                "result": "false",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    like: like_model.Like | None = await like_crud.get_by_user_id_and_tweet_id(
        session=session,
        user_id=current_user.id,
        tweet_id=tweet_id,
    )

    if like:
        return JSONResponse(
            content={
                "result": "false",
            },
            status_code=status.HTTP_409_CONFLICT,
        )

    like_data: dict[str, str | int] = {
        "user_id": current_user.id,
        "name": current_user.name,
        "tweet_id": tweet_id,
    }

    await like_crud.post(session=session, obj_in_data=like_data)
    logger.info('Пользователь с id %s '
                'успешно поставил лайк на твит с id %s', current_user.id, tweet_id)
    return JSONResponse(
        content={
            "result": "true",
        },
        status_code=status.HTTP_201_CREATED,
    )
