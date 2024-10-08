from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.secure_user import get_user_by_secure_key
from src import crud, schemas
from src.database.session_manager import get_async_session
from src.database.models.user_model import User

router: APIRouter = APIRouter(tags=['POST'])


@router.delete(
    "/api/users/{user_id}/follow", status_code=status.HTTP_200_OK
)
async def subscription(
        user_id: int, session: AsyncSession = Depends(get_async_session),
        current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key)
) -> JSONResponse:
    user_in_db: User = await crud.user.user_crud.get(session=session, user_id=user_id)
    current_user_in_db: User = await crud.user.user_crud.get(session=session, user_id=current_user.id)
    if user_in_db:
        current_user_in_db.following.remove(user_in_db)
        await session.refresh(current_user_in_db)
        await session.commit()

        return JSONResponse(
            content={
                "result": "true",
            },
            status_code=status.HTTP_200_OK,
        )
