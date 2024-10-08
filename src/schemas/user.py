from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import AppenderQuery
from src.database.session_manager import db_manager
from src.schemas.tweet import TweetResponse
from src.schemas.base_api_schema import APIBaseSuccessfulSchema


class UserBase(BaseModel):
    name: str = Field(max_length=50)

    # @field_validator("*", mode='before')
    # def evaluate_lazy_columns(cls, v):
    #     if isinstance(v, AppenderQuery):
    #         async_session = db_manager.async_session()
    #         result = async_session.scalars(v)
    #         print(result)
    #         return result
    #     return v


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


class UserPatchRequest(UserBase):
    name: Optional[str]
    followers: Optional[list[dict]] = []
    following: Optional[list[dict]] = []


class APIUserResponseSuccessful(APIBaseSuccessfulSchema):
    user: UserResponse


class APIUserListResponseSuccessful(APIBaseSuccessfulSchema):
    data: list[UserResponse]
