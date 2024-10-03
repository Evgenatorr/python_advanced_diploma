from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.user_model import User
from src.schemas.user import APIUserResponse, UserCreate, UserResponse
from src.database.session_manager import get_async_session
from src.auth.secure_user import get_user_by_secure_key

router = APIRouter(tags=['GET'])


@router.get(
    "/api/users/me", response_model=APIUserResponse, status_code=status.HTTP_200_OK
)
async def user_info(
        session: AsyncSession = Depends(get_async_session),
        current_user: UserResponse = Depends(get_user_by_secure_key)
) -> JSONResponse:
    # response_model = UserResponse.model_validate(user_response)

    return JSONResponse(
        content={
            "result": "true",
            "user": current_user.model_dump(),
        },
        status_code=status.HTTP_200_OK,
    )


# {
#         "result": "true",
#         "user": {
#             "id": 1,
#             "name": "name",
#             "followers": [], "following": []
#         }
#     }