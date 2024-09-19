from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.secure_user import get_user
from src.crud.tweet import tweet_crud
from src.database.session_manager import get_session
from src import schemas

router = APIRouter(tags=['POST'])


@router.post(
    "/api/tweets", status_code=status.HTTP_201_CREATED
)
async def create_tweet(
        tweet_data: schemas.tweet.TweetCreateRequest, session: AsyncSession = Depends(get_session),
        user: schemas.user.UserResponse = Depends(get_user)
) -> JSONResponse:
    tweet = await tweet_crud.post(session=session, tweet_data=tweet_data.model_dump(), author_id=user.id)
    print(tweet_data.tweet_media_ids)
    return JSONResponse(
        content={
            "result": "true",
            "tweet_id": tweet.id,
        },
        status_code=status.HTTP_201_CREATED,
    )
