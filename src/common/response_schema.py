from typing import Any
from typing import Optional

import ujson
from pydantic import BaseModel


class ResponseModel(BaseModel):
    status_code: Any
    message: Optional[str] = ''
    data: Optional[Any] = ''

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "message": "Success",
                "data": {"key": "value"},
            }
        }
