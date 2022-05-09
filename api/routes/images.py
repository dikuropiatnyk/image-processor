import base64
import logging

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from typing import List

from models import EncodedImages, OpenioCreateResponse, OpenioImage
from providers import openio_client
from utils.helpers import map_images

router = APIRouter(prefix="/images")


@router.get("", response_model=Page[OpenioImage])
async def get_images():
    images = await openio_client.get_images()
    return paginate(images)


@router.post("/process", response_model=List[OpenioCreateResponse])
async def process_images(images: EncodedImages):
    response = []

    logging.info("Received %s images. Start processing...", len(images.Images))
    for image in images.Images:
        decoded_object = base64.decodebytes(str.encode(image.Encoded))
        result = await openio_client.send_image(image.Name, decoded_object)
        response.append(
            OpenioCreateResponse(
                object_name=image.Name,
                etag=result[0].strip('"'),
                last_modified=result[1],
            )
        )

    logging.info("Sending is done!")

    return response
