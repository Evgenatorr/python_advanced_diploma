from fastapi import Security, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ScalarResult
from src import crud
from src.database import models
from src.database.async_session import get_async_session
from config import settings
from src.schemas.user import UserResponse


async def get_user_by_secure_key(
        api_key: str = Security(settings.API_KEY_HEADER),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Функция проверяет api_key_header от пользователя
    :param api_key: ключ аутентификации пользователя
    :param session: асинхронная сессия базы данных
    :return: UserResponse | HTTPException
    """

    api_key_db: models.api_key_model.ApiKey = await crud.api_key.api_key_crud.get_by_apikey(session=session,
                                                                                            api_key=api_key)
    if api_key_db:
        user: models.user_model.User = api_key_db.user

        followers: ScalarResult = await crud.user.user_crud.get_list_followers_by_user(session=session, user=user)
        following: ScalarResult = await crud.user.user_crud.get_list_following_by_user(session=session, user=user)
        user_response: UserResponse = UserResponse(
            id=user.id,
            name=user.name,
            followers=followers,
            following=following,
            tweets=user.tweets,
            api_key=api_key_db
        )
        return user_response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
