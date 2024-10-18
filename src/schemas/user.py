from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.base_api_schema import APIBaseSuccessfulSchema
from src.schemas.tweet import TweetResponse


class UserBase(BaseModel):
    name: str = Field(max_length=50)


class UserCreate(UserBase):
    ...


class Follower(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    id: int
    tweets: Optional[list[TweetResponse]] = []
    followers: Optional[list[Follower]]
    following: Optional[list[Follower]]
    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(UserBase):
    followers: Optional[list[dict]]
    following: Optional[list[dict]]


class APIUserResponseSuccessful(APIBaseSuccessfulSchema):
    user: UserResponse
