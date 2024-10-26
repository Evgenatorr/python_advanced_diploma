from fastapi import Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from src import crud
from src.database import models
from src.database.async_session import get_async_session
from src.schemas.user import UserResponse
from logs_conf.utils import logger


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

    api_key_db: models.api_key_model.ApiKey | None = (
        await crud.api_key.api_key_crud.get_by_apikey(session=session, api_key=api_key)
    )
    if api_key_db:
        user: models.user_model.User | None = await crud.user.user_crud.get(
            session=session, user_id=api_key_db.user_id
        )
        followers = [
            {"id": follower.id, "name": follower.name}
            for follower in user.followers
        ]
        following = [
            {"id": following.id, "name": following.name}
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
