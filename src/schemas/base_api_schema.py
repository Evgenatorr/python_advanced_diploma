from typing import Literal

from pydantic import BaseModel


class APIBaseSuccessfulSchema(BaseModel):
    result: Literal["true"] = "true"


class APIBaseFailedSchema(BaseModel):
    result: Literal["false"] = "false"
