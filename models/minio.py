from pydantic import BaseModel
from datetime import datetime


class MinioCreateResponse(BaseModel):
    object_name: str
    etag: str


class MinioImage(BaseModel):
    id: str
    image_name: str
    timestamp: datetime
    image_size: float
