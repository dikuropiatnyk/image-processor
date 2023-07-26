import logging

from fastapi import APIRouter, UploadFile, Form, Body, status
from starlette.responses import JSONResponse

from models import EncodedImage, UploadedImage
from providers import mongo_client
from utils.image_processing import (
    apply_watermark_on_image_and_upload,
    prepare_watermark,
)


router = APIRouter(prefix="/v2", tags=["User-Friendly Image Processing"])


@router.post("/watermarks/upload")
async def upload_watermark(
    watermark: UploadFile,
    description: str = Form(...),
):
    """
    Main difference between the previous version - using Form Data
    to upload file directly from user
    """
    processed_watermark = EncodedImage(
        name=watermark.filename,
        raw_data=await watermark.read(),
        description=description,
    )
    object_id = await mongo_client.upload_watermark(processed_watermark)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"result": f"Image was uploaded with id: {object_id}"}
    )


@router.post(
    "/images/process",
    response_model=UploadedImage,
)
async def process_images(
    image: UploadFile,
    description: str = Form(...),
    watermark_id: str = Form(default=None),
):
    logging.info("Trying to get a watermark...")
    if watermark_id:
        watermark = await mongo_client.get_watermark_by_id(watermark_id)
    else:
        watermark = await mongo_client.get_watermark_by_default()
    logging.info(f"Watermark {watermark.name} will be used")

    prepared_watermark = prepare_watermark(watermark)

    encoded_image = EncodedImage(
        name=image.filename,
        raw_data=await image.read(),
        description=description,
    )

    # Apply watermark on image
    uploaded_image = await apply_watermark_on_image_and_upload(
        encoded_image,
        prepared_watermark,
    )
    return uploaded_image
