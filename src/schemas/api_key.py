from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional, List


class ApiKeyCreateRequest(BaseModel):
    api_key: str = Field()
    user_id: int


class ApiKeyResponse(ApiKeyCreateRequest):
    id: int
    model_config = ConfigDict(from_attributes=True)


class APIApiKeyResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: ApiKeyResponse


class APIApiKeyListResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: List[ApiKeyResponse]
