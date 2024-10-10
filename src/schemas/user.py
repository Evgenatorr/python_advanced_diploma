from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.base_api_schema import APIBaseSuccessfulSchema
from src.schemas.tweet import TweetResponse


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


class APIUserResponseSuccessful(APIBaseSuccessfulSchema):
    user: UserResponse


class APIUserListResponseSuccessful(APIBaseSuccessfulSchema):
    data: list[UserResponse]
