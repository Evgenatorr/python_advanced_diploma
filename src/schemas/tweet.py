from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional, List


class TweetCreateRequest(BaseModel):
    tweet_data: str = Field()
    tweet_media_ids: Optional[List[int]]


class TweetResponse(TweetCreateRequest):
    id: int
    likes: List
    model_config = ConfigDict(from_attributes=True)


class APITweetResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: TweetResponse


class APITweetListResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: List[TweetResponse]
