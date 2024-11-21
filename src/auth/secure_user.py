from fastapi import Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from src import crud
from src.database import models
from src.database.async_session import get_async_session
from src.schemas.user import UserResponse
from logs_conf.log_utils import logger
from src.utils.followers_to_dict import entity_to_dict


async def get_user_by_secure_key(
        api_key: str = Security(settings.API_KEY_HEADER),
        session: AsyncSession = Depends(get_async_session),
):
    """
    Функция проверяет api_key_header от пользователя
    :param api_key: ключ аутентификации пользователя
    :param session: асинхронная сессия базы данных
    :return: UserResponse | HTTPException
    """

    user: models.user_model.User | None = await crud.user.user_crud.get_by_api_key(
        session=session, api_key=api_key
    )
    if user:
        followers = [
            entity_to_dict(follower)
            for follower in user.followers
        ]
        following = [
            entity_to_dict(following)
            for following in user.following
        ]

        user_response: UserResponse = UserResponse(
            id=user.id,
            name=user.name,
            followers=followers,
            following=following,
            tweets=user.tweets,
        )
        logger.debug(f'Пользователь с id {user_response.id} '
                     f'успешно прошел аутентификацию')
        return user_response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key"
    )
