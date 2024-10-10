from typing import Optional

from src.schemas.base_api_schema import APIBaseFailedSchema


class APIBaseSchema(APIBaseFailedSchema):
    error_type: Optional[str] = None
    error_message: Optional[str] = None
