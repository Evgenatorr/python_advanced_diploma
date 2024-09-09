from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.tweet import TweetCreateRequest, APITweetResponse
from src.database.session_manager import get_session

router = APIRouter()


@router.post("/api/tweets", response_model=APITweetResponse, status_code=status.HTTP_201_CREATED)
async def create_tweet(
        tweet_data: TweetCreateRequest, session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    ...
