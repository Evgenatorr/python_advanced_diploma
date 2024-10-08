from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.secure_user import get_user_by_secure_key
from src import crud, schemas
from src.database.session_manager import get_async_session
from src.database.models.tweet_model import Tweet

router: APIRouter = APIRouter(tags=['POST'])


@router.post(
    "/api/tweets/{tweet_id}/likes", status_code=status.HTTP_201_CREATED
)
async def like_tweet(
        tweet_id: int, session: AsyncSession = Depends(get_async_session),
        current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key)
) -> JSONResponse:
    tweet: Tweet = await crud.tweet.tweet_crud.get(session=session, tweet_id=tweet_id)

    if tweet:
        like_data: dict[str, str | int] = {
            'user_id': current_user.id,
            'name': current_user.name,
            'tweet_id': tweet_id
        }

        like = await crud.like.like_crud.post(session=session, like_data=like_data)

        return JSONResponse(
            content={
                "result": "true",
            },
            status_code=status.HTTP_201_CREATED,
        )
