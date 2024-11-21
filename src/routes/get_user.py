from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.secure_user import get_user_by_secure_key
from src.schemas.user import APIUserResponseSuccessful, UserResponse

router = APIRouter(tags=["GET"])


@router.get(
    "/api/users/me",
    response_model=APIUserResponseSuccessful,
    status_code=status.HTTP_200_OK,
)
async def user_info(
    current_user: UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер для получения информации о пользователе
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """
    return JSONResponse(
        content={
            "result": "true",
            "user": current_user.model_dump(),
        },
        status_code=status.HTTP_200_OK,
    )
