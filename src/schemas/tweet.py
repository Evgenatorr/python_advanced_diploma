from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.base_api_schema import APIBaseSuccessfulSchema


class Author(BaseModel):
    name: str
    id: int
    model_config = ConfigDict(from_attributes=True)


class LikeTweet(BaseModel):
    name: str
    user_id: int
    tweet_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)


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
    likes: Optional[list[LikeTweet]]
    author: Author
    model_config = ConfigDict(from_attributes=True)


class APITweetResponseSuccessful(APIBaseSuccessfulSchema):
    tweet: TweetResponse


class APITweetListResponseSuccessful(APIBaseSuccessfulSchema):
    tweets: List[TweetResponse]
