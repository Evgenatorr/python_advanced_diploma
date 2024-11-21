from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.crud.user import user_crud
from src.database.async_session import get_async_session
from src.database.models.user_model import User
from src.schemas.user import UserResponse
from src.utils.followers_to_dict import entity_to_dict


async def check_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> UserResponse | HTTPException:
    """
    Функция проверки пользователя на существование, и получение его подписок и подписчиков
    :param user_id: id пользователя
    :param session: асинхронная сессия базы данных
    :return: UserResponse | None
    """

    user: User | None = await user_crud.get_with_lazy_load(session=session, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    followers = [
        entity_to_dict(follower)
        for follower in user.followers
    ]
    following = [
        entity_to_dict(following)
        for following in user.following
    ]

    response_model = UserResponse(
        followers=followers, following=following, name=user.name, id=user.id
    )
    return response_model
