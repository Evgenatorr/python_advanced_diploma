from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.secure_user import get_user_by_secure_key
from src import crud
from src.database.session_manager import get_async_session
from src import schemas

router = APIRouter(tags=['DELETE'])


@router.delete(
    "/api/tweets/{tweet_id}/likes", status_code=status.HTTP_200_OK
)
async def delete_like(
        tweet_id: int, session: AsyncSession = Depends(get_async_session),
        current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key)
) -> JSONResponse:
    like = await crud.like.like_crud.get_by_user_id_and_tweet_id(
        session=session,
        user_id=current_user.id,
        tweet_id=tweet_id,
    )

    if like:
        like = await crud.like.like_crud.delete(session=session, like_id=like.id)

        return JSONResponse(
            content={
                "result": "true",
            },
            status_code=status.HTTP_200_OK,
        )
