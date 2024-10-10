from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.auth.secure_user import get_user_by_secure_key
from src.database.async_session import get_async_session
from src.database.models.tweet_model import Tweet

router: APIRouter = APIRouter(tags=["POST"])


@router.post("/api/tweets/{tweet_id}/likes", status_code=status.HTTP_201_CREATED)
async def like_tweet(
    tweet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер для добавления нового лайка от пользователя в базу данных
    :param tweet_id: id твита
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """

    tweet: Tweet | None = await crud.tweet.tweet_crud.get(session=session, tweet_id=tweet_id)

    if tweet:
        like_data: dict[str, str | int] = {
            "user_id": current_user.id,
            "name": current_user.name,
            "tweet_id": tweet_id,
        }

        await crud.like.like_crud.post(session=session, like_data=like_data)

        return JSONResponse(
            content={
                "result": "true",
            },
            status_code=status.HTTP_201_CREATED,
        )

    return JSONResponse(
        content={
            "result": "false",
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )
