from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.secure_user import get_user_by_secure_key
from src import crud
from src.database.session_manager import get_async_session
from src import schemas

router = APIRouter(tags=['POST'])


@router.post(
    "/api/tweets", status_code=status.HTTP_201_CREATED
)
async def create_tweet(
        tweet_data: schemas.tweet.TweetCreateRequest, session: AsyncSession = Depends(get_async_session),
        current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key)
) -> JSONResponse:
    media_id = tweet_data.tweet_media_ids if tweet_data.tweet_media_ids else None

    media = await crud.media.media_crud.get(session=session, media_id=media_id)
    media_link = [media.file_link] if media else None

    data_dict = {
        'content': tweet_data.tweet_data,
        'attachments': media_link,
    }

    data = schemas.tweet.TweetBase(
        **data_dict
    )

    tweet = await crud.tweet.tweet_crud.post(session=session, tweet_data=data.model_dump(exclude_unset=True),
                                             author_id=current_user.id)
    if media:
        media.tweet_id = tweet.id
        await session.commit()

    return JSONResponse(
        content={
            "result": "true",
            "tweet_id": tweet.id,
        },
        status_code=status.HTTP_201_CREATED,
    )
