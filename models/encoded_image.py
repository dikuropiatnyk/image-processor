import base64
import bson

from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Union


class EncodedImage(BaseModel):
    name: str
    raw_data: Union[str, bytes]
    description: str = ""
    created_at: datetime = None

    @validator("raw_data")
    def convert_image_to_bytes(cls, v):
        if not v:
            raise ValueError("Encoded image should be provided!")
        # For encoded images base64 should be applied
        if isinstance(v, str):
            return bson.Binary(base64.b64decode(v))
        elif isinstance(v, bytes):
            return bson.Binary(v)
        raise ValueError("Unknown type of raw_data")

    @validator("created_at", pre=True, always=True)
    def set_up_current_datetime(cls, v):
        return v or datetime.now()


class DefaultWatermark(BaseModel):
    id: str

    @validator("id")
    def check_if_object_id(cls, v):
        if not bson.ObjectId.is_valid(v):
            raise ValueError("Invalid Object ID!")
        return bson.ObjectId(v)


class EncodedImages(BaseModel):
    images: list[EncodedImage]
    watermark_id: str = None

    @validator("watermark_id")
    def check_if_custom_id_is_valid(cls, v):
        if v is not None and not bson.ObjectId.is_valid(v):
            raise ValueError("Invalid Object ID!")
        return v

