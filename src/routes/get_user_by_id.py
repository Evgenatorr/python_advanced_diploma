from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import user_crud
from src.database.async_session import get_async_session
from src.database.models.user_model import User
from src.schemas.user import APIUserResponseSuccessful, UserResponse, Follower

router = APIRouter(tags=["GET"])


async def check_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> UserResponse | None:
    """
    Функция получения пользователя, его подписки и подписчиков
    :param user_id: id пользователя
    :param session: асинхронная сессия базы данных
    :return: UserResponse | None
    """

    user: User | None = await user_crud.get(session=session, user_id=user_id)

    if user:
        followers = [{"id": follower.id, "name": follower.name} for follower in user.followers]
        following = [{"id": following.id, "name": following.name} for following in user.following]
        response_model = UserResponse(
            followers=followers, following=following, name=user.name, id=user.id
        )
        return response_model

    return None


@router.get(
    "/api/users/{user_id}",
    response_model=APIUserResponseSuccessful,
    status_code=status.HTTP_200_OK,
)
async def user_info(
    user: UserResponse = Depends(check_user),
) -> JSONResponse:
    """
    Роутер для получения пользователя по id
    :param user: пользователь
    :return: JSONResponse
    """

    return JSONResponse(
        content={
            "result": "true",
            "user": user.model_dump(),
        },
        status_code=status.HTTP_200_OK,
    )
