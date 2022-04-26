from pydantic import BaseModel
from typing import List


class EncodedImage(BaseModel):
    Name: str
    Encoded: str


class EncodedImages(BaseModel):
    Images: List[EncodedImage]
