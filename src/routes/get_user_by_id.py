from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import APIUserResponse, UserResponse
from src.database.session_manager import get_async_session
from src.crud.user import user_crud

router = APIRouter(tags=['GET'])


async def check_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    user = await user_crud.get(session=session, user_id=user_id)
    following = await user_crud.get_list_following_by_user(session=session, user=user)
    followers = await user_crud.get_list_followers_by_user(session=session, user=user)
    response_model = UserResponse(
        followers=followers,
        following=following,
        name=user.name,
        id=user.id
    )
    return response_model


@router.get(
    "/api/users/{user_id}", response_model=APIUserResponse, status_code=status.HTTP_200_OK
)
async def user_info(
        user: UserResponse = Depends(check_user),
) -> JSONResponse:
    return JSONResponse(
        content={
            "result": "true",
            "user": user.model_dump(),
        },
        status_code=status.HTTP_200_OK,
    )
