from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.secure_user import get_user
from src import crud
from src.database.session_manager import get_session
from src import schemas

router = APIRouter(tags=['POST'])


@router.post(
    "/api/tweets/{tweet_id}/likes", status_code=status.HTTP_201_CREATED
)
async def like_tweet(
        tweet_id: int, session: AsyncSession = Depends(get_session),
        user: schemas.user.UserResponse = Depends(get_user)
) -> JSONResponse:
    tweet = await crud.tweet.tweet_crud.get(session=session, tweet_id=tweet_id)

    if tweet:
        like_data = {
            'user_id': user.id,
            'name': user.name,
            'tweet_id': tweet_id
        }

        like = await crud.like.like_crud.post(session=session, like_data=like_data)

        return JSONResponse(
            content={
                "result": "true",
            },
            status_code=status.HTTP_201_CREATED,
        )
