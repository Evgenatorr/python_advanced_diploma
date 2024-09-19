from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional, List


class LikeTweet(BaseModel):
    name: str
    user_id: int
    tweet_id: Optional[int]


class TweetBase(BaseModel):
    content: str
    attachments: Optional[List[str]]


class TweetCreateRequest(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]]


class TweetCreateResponse(TweetCreateRequest):
    id: int
    likes: Optional[List]
    model_config = ConfigDict(from_attributes=True)


class TweetUpdateRequest(TweetBase):
    ...


class TweetResponse(TweetBase):
    id: int
    likes: Optional[list]
    model_config = ConfigDict(from_attributes=True)


class APITweetResponse(BaseModel):
    result: Literal['true'] = 'true'
    tweet: TweetResponse


class APITweetListResponse(BaseModel):
    result: Literal['true'] = 'true'
    tweets: List[TweetResponse]
