from fastapi import Security, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.crud.api_key import api_key_crud
from src.database.session_manager import get_session
from config import settings
from src.schemas.user import UserResponse


async def get_user(
        api_key: str = Security(settings.API_KEY_HEADER),
        session: AsyncSession = Depends(get_session)
):
    api_key_db = await api_key_crud.get(api_key=api_key, session=session)

    if api_key_db:
        user = api_key_db.user
        response_model = UserResponse.model_validate(user)
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
