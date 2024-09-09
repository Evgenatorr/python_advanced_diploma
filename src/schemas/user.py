from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class UserCreateRequest(BaseModel):
    name: str = Field(max_length=50)


class UserResponse(BaseModel):
    id: int
    name: str
    followers: list
    following: list

    model_config = ConfigDict(from_attributes=True)


class APIUserResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: UserResponse


class APIUserListResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: list[UserResponse]
