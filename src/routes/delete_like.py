from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from logs_conf.log_utils import logger
from src.auth.secure_user import get_user_by_secure_key
from src.crud import like_crud
from src.database.async_session import get_async_session
from src.database.models.like_model import Like
from src.schemas import UserResponse, APIBaseSuccessfulSchema

router: APIRouter = APIRouter(tags=["DELETE"])


@router.delete("/api/tweets/{tweet_id}/likes", status_code=status.HTTP_200_OK,
               response_model=APIBaseSuccessfulSchema)
async def delete_like(
        tweet_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер удаления лайка из базы данных
    :param tweet_id: id твита
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """
    logger.debug('Пользователь с id %s удаляет лайк', current_user.id)
    like: Like | None = await like_crud.get_by_user_id_and_tweet_id(
        session=session,
        user_id=current_user.id,
        tweet_id=tweet_id,
    )

    if like:
        await like_crud.delete(session=session, obj_id=like.id)
        logger.info('Пользователь с id %s '
                    'успешно убрал лайк с твита с id %s', current_user.id, tweet_id)
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
