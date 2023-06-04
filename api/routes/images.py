import logging
import asyncio

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from typing import List

from models import EncodedImages, OpenioCreateResponse, OpenioImage
from providers import openio_client
from api.tasks.image import process_image

router = APIRouter(prefix="/images")


@router.get("", response_model=Page[OpenioImage])
async def get_images():
    images = await openio_client.get_images()
    return paginate(images)


@router.post("/process", response_model=List[OpenioCreateResponse])
async def process_images(images: EncodedImages):
    logging.info("Received %s images. Start processing...", len(images.Images))
    response = await asyncio.gather(
        *[process_image(image) for image in images.Images]
    )
    logging.info("Sending is done!")

    return response
