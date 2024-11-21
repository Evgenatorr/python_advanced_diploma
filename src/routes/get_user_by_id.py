from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.routes.dependencies.search_user_by_id import check_user
from src.schemas.user import APIUserResponseSuccessful, UserResponse

router = APIRouter(tags=["GET"])


@router.get(
    "/api/users/{user_id}",
    response_model=APIUserResponseSuccessful,
    status_code=status.HTTP_200_OK,
    description='Роутер для получения пользователя по id'
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
