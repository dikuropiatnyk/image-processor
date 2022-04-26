import base64

from fastapi import APIRouter

from models import EncodedImages
from providers import minio_client


router = APIRouter()


@router.post("/process")
async def process_images(images: EncodedImages):
    for image in images.Images:
        decoded_object = base64.decodebytes(str.encode(image.Encoded))
        minio_client.send_image(image.Name, decoded_object)

    return {"result": "Images were processed correctly!"}

