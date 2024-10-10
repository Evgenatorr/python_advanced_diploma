from typing import List

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.base_api_schema import APIBaseSuccessfulSchema


class ApiKeyCreateRequest(BaseModel):
    api_key: str = Field()
    user_id: int


class ApiKeyResponse(ApiKeyCreateRequest):
    id: int
    model_config = ConfigDict(from_attributes=True)


class APIApiKeyResponseSuccessful(APIBaseSuccessfulSchema):
    data: ApiKeyResponse


class APIApiKeyListResponseSuccessful(APIBaseSuccessfulSchema):
    data: List[ApiKeyResponse]
