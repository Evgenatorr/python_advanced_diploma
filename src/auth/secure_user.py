from fastapi import Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from logs_conf.log_utils import logger
from src.crud import user_crud
from src.database import models
from src.database.async_session import get_async_session
from src.schemas import UserResponse


async def get_user_by_secure_key(
        api_key: str = Security(settings.API_KEY_HEADER),
        session: AsyncSession = Depends(get_async_session),
) -> UserResponse:
    """
    Функция проверяет api_key_header от пользователя
    :param api_key: ключ аутентификации пользователя
    :param session: асинхронная сессия базы данных
    :return: UserResponse | HTTPException
    """

    logger.debug('Авторизация пользователя с api_key: %s', api_key)
    user: models.user_model.User | None = await user_crud.get_by_api_key(
        session=session, api_key=api_key
    )
    if user:
        user_response = UserResponse.model_validate(user)
        logger.info('Пользователь(api_key: %s) с id %s '
                    'успешно прошел авторизацию', api_key, user_response.id)

        return user_response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key"
    )
