from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import APIUserResponse, UserCreate, UserResponse
from src.database.session_manager import get_session
from src.crud.user import user_crud

router = APIRouter(tags=['GET'])


@router.get(
    "/api/users/{user_id}", response_model=APIUserResponse, status_code=status.HTTP_200_OK
)
async def user_info(
        user_id: int,
        session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    user = await user_crud.get(session=session, user_id=user_id)
    response_model = UserResponse.model_validate(user)
    return JSONResponse(
        content={
            "result": "true",
            "user": response_model.model_dump(),
        },
        status_code=status.HTTP_200_OK,
    )