import base64
import logging
from fastapi import APIRouter

from models import EncodedImages


router = APIRouter(tags=['Image-Processor'])


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.post("/process")
async def process_images(images: EncodedImages):
    for image in images.Images:
        with open(f"images/{image.Name}", "wb") as fh:
            fh.write(base64.decodebytes(str.encode(image.Encoded)))

    return {"result": "Images were processed correctly!"}

