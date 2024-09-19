from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.auth.secure_user import get_user
from src import schemas


router = APIRouter(tags=['GET'])


@router.get(
    "/api/tweets", response_model=schemas.tweet.APITweetListResponse, status_code=status.HTTP_200_OK
)
async def get_tweet(
        user: schemas.user.UserResponse = Depends(get_user),
) -> JSONResponse:
    tweets = user.tweets

    response_model = [
        schemas.tweet.TweetResponse.model_validate(jsonable_encoder(tweet)).model_dump() for tweet in tweets
    ]

    return JSONResponse(
        content={
            "result": "true",
            "tweets": response_model,
        },
        status_code=status.HTTP_200_OK,
    )
