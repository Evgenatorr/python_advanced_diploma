from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional
from src import schemas


class UserBase(BaseModel):
    name: str = Field(max_length=50)


class UserCreate(UserBase):
    ...


class Follower(UserBase):
    id: int


class UserResponse(UserBase):
    id: int
    followers: Optional[list[Follower]]
    following: Optional[list[Follower]]
    # tweets: Optional[list[schemas.tweet.TweetResponse]]
    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(UserBase):
    followers: Optional[list[dict]]
    following: Optional[list[dict]]


class UserPatchRequest(UserBase):
    name: Optional[str]
    followers: Optional[list[dict]] = []
    following: Optional[list[dict]] = []


class APIUserResponse(BaseModel):
    result: Literal['true'] = 'true'
    user: UserResponse


class APIUserListResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: list[UserResponse]
