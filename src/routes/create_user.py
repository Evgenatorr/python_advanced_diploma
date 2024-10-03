import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import APIUserResponse, UserCreate, UserResponse
from src.database.session_manager import get_async_session
from src import crud

router = APIRouter(tags=['POST'])


@router.post(
    "/api/users", status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_data: UserCreate = Depends(), session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    user = await crud.user.user_crud.post(session=session, user_data=user_data.model_dump())
    api_key = str(uuid.uuid4())
    # api_key = 'test'
    api_data = {
        'api_key': api_key,
        'user_id': user.id
    }
    api_key = await crud.api_key.api_key_crud.post(session=session, api_key_data=api_data)
    await session.refresh(user)

    return JSONResponse(
        content={'status': 'true'}
    )
