from pydantic import BaseModel


class DBImage(BaseModel):
    """
    Model for the image from the storage
    """
    name: str
    raw_data: bytes
