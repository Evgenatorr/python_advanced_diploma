from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.crud import user_crud
from src.database.async_session import get_async_session
from src.database.models.user_model import User
from src.schemas import UserResponse
from logs_conf.log_utils import logger


async def check_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> UserResponse | HTTPException:
    """
    Функция проверки пользователя на существование
    и получение его подписок и подписчиков
    :param user_id: id пользователя
    :param session: асинхронная сессия базы данных
    :return: UserResponse | None
    """

    logger.debug('Получаем пользователя по id %s', user_id)
    user: User | None = await user_crud.get_with_lazy_load(
        session=session, user_id=user_id
    )

    if not user:
        logger.info('Пользователь с id %s не найден', user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    response_model = UserResponse.model_validate(user)

    return response_model
