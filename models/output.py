from datetime import datetime

from pydantic import BaseModel


class Pagination(BaseModel):
    total_count: int
    limit: int
    offset: int


class OutputImage(BaseModel):
    id: str
    name: str
    created_at: datetime
    description: str = ""


class OutputWatermark(OutputImage):
    """
    A watermark image in the storage
    """
    is_default: bool = False


class ProcessedImages(BaseModel):
    images: list[OutputImage]
    paging: Pagination


class Watermarks(BaseModel):
    images: list[OutputWatermark]
    paging: Pagination
