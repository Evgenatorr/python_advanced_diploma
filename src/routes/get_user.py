from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import APIUserResponse, UserCreate, UserResponse
from src.database.session_manager import get_session
from src.auth.secure_user import get_user

router = APIRouter(tags=['GET'])


@router.get(
    "/api/users/me", response_model=APIUserResponse, status_code=status.HTTP_200_OK
)
async def user_info(
        session: AsyncSession = Depends(get_session),
        user: UserResponse = Depends(get_user)
) -> JSONResponse:
    response_model = UserResponse.model_validate(user)

    return JSONResponse(
        content={
            "result": "true",
            "user": response_model.model_dump(),
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