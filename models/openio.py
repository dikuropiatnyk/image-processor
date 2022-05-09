from pydantic import BaseModel, validator
from datetime import datetime


class OpenioCreateResponse(BaseModel):
    object_name: str
    etag: str
    last_modified: datetime

    @validator("last_modified", pre=True)
    def parse_birthdate(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z")
        return value


class OpenioImage(BaseModel):
    id: str
    image_name: str
    timestamp: datetime
    image_size: float
