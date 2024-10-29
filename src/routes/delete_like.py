from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.auth.secure_user import get_user_by_secure_key
from src.database.async_session import get_async_session
from src.database.models.like_model import Like
from logs_conf.log_utils import logger

router: APIRouter = APIRouter(tags=["DELETE"])


@router.delete("/api/tweets/{tweet_id}/likes", status_code=status.HTTP_200_OK)
async def delete_like(
    tweet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер удаления лайка из базы данных
    :param tweet_id: id твита
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """

    like: Like | None = await crud.like.like_crud.get_by_user_id_and_tweet_id(
        session=session,
        user_id=current_user.id,
        tweet_id=tweet_id,
    )

    if like:
        await crud.like.like_crud.delete(session=session, id=like.id)
        logger.debug(f'Пользователь с id {current_user.id} '
                     f'успешно убрал лайк с твита с id {tweet_id}')
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
