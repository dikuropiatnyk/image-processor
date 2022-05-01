import base64
import logging

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from typing import List

from models import EncodedImages, MinioCreateResponse, MinioImage
from providers import MinioConnection
from utils.helpers import map_images

router = APIRouter(prefix="/images")


@router.get("", response_model=Page[MinioImage])
async def get_images(minio_client: MinioConnection = Depends()):
    # Get images generator
    images_gen = minio_client.get_images()

    images = map_images(images_gen)
    logging.info(f"Total images count: {len(images)}")
    return paginate(images)


@router.post("/process", response_model=List[MinioCreateResponse])
async def process_images(
    images: EncodedImages,
    minio_client: MinioConnection = Depends(),
 ):
    response = []

    logging.info("Received %s images. Start processing...", len(images.Images))
    for image in images.Images:
        decoded_object = base64.decodebytes(str.encode(image.Encoded))
        result = minio_client.send_image(image.Name, decoded_object)
        response.append(
            MinioCreateResponse(
                object_name=result.object_name,
                etag=result.etag
            )
        )

    logging.info("Sending is done!")

    return response
