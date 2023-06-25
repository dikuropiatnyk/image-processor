from datetime import datetime

from pydantic import BaseModel


class Pagination(BaseModel):
    total_count: int
    limit: int
    offset: int


class BaseOutputImage(BaseModel):
    id: str
    name: str
    created_at: datetime


class OutputProcessedImage(BaseOutputImage):
    """
    Processed image with a watermark in the storage
    """
    description: str


class OutputWatermark(BaseOutputImage):
    """
    A watermark image in the storage
    """
    is_default: bool = False


class ProcessedImages(BaseModel):
    images: list[OutputProcessedImage]
    paging: Pagination


class Watermarks(BaseModel):
    images: list[OutputWatermark]
    paging: Pagination
