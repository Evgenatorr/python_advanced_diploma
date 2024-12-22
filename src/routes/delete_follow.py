from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from logs_conf.log_utils import logger
from src.auth.secure_user import get_user_by_secure_key
from src.crud import user_crud
from src.database.async_session import get_async_session
from src.database.models.user_model import User
from src.schemas import UserResponse, APIBaseSuccessfulSchema

router: APIRouter = APIRouter(tags=["DELETE"])


@router.delete("/api/users/{user_id}/follow", status_code=status.HTTP_200_OK,
               response_model=APIBaseSuccessfulSchema)
async def subscription(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роут отписки от пользователя
    :param user_id: id пользователя
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """

    logger.debug('Пользователь с id %s отписывается', current_user.id)
    user_in_db: User | None = await user_crud.get_with_lazy_load(
        session=session, user_id=user_id
    )

    follower: User | None = await user_crud.get_with_lazy_load(
        session=session, user_id=current_user.id
    )

    if user_in_db and follower:
        user_in_db.followers.remove(follower)
        await session.commit()
        logger.info(
            'Пользователь с id %s '
            'отписался от пользователя с id %s', follower.id, user_in_db.id
        )
        return JSONResponse(
            content={
                "result": "true",
            },
            status_code=status.HTTP_200_OK,
        )

    logger.info('Пользователь не найден')
    return JSONResponse(
        content={
            "result": "false",
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )
