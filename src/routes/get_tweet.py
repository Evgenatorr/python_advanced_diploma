from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.auth.secure_user import get_user_by_secure_key
from src.database.async_session import get_async_session
from src.database.models.user_model import User

router = APIRouter(tags=["GET"])


@router.get(
    "/api/tweets",
    response_model=schemas.tweet.APITweetListResponseSuccessful,
    status_code=status.HTTP_200_OK,
)
async def get_tweet(
    current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key),
    session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """
    Роутер для получения всех твитов пользователя вместе с твитами на кого подписан user
    :param current_user: пользователь прошедший аутентификацию
    :param session: асинхронная сессия базы данных
    :return: JSONResponse
    """

    tweets = current_user.tweets
    user_in_db: User | None = await crud.user.user_crud.get(session=session, user_id=current_user.id)
    if user_in_db is None or tweets is None:
        return JSONResponse(
            content={
                "result": "false",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    following = await crud.user.user_crud.get_list_following_by_user(
        session=session, user=user_in_db
    )

    tweets_following_user = [
        await crud.tweet.tweet_crud.get_list_by_user_id(
            session=session, user_id=user.id
        )
        for user in following.all()
    ]

    if tweets_following_user:
        tweets_model_list = [
            schemas.tweet.TweetResponse.model_validate(tweet)
            for tweet in tweets_following_user[0]
        ]
        tweets.extend(tweets_model_list)

    response_model = [
        schemas.tweet.TweetResponse.model_validate(jsonable_encoder(tweet)).model_dump()
        for tweet in tweets
    ]

    return JSONResponse(
        content={
            "result": "true",
            "tweets": response_model,
        },
        status_code=status.HTTP_200_OK,
    )
