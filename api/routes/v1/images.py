import asyncio
import logging

from fastapi import APIRouter, Query, status
from starlette.responses import JSONResponse
from typing import List

from core import ImageResponse
from models import (
    DefaultWatermark,
    EncodedImage,
    EncodedImages,
    Pagination,
    ProcessedImages,
    Watermarks,
    UploadedImage,
)
from providers import mongo_client
from utils.image_processing import apply_watermark_on_image_and_upload, prepare_watermark


router = APIRouter(prefix="/v1", tags=["Image Processing"])


# RETRIEVE ENDPOINTS
@router.get("/images", response_model=ProcessedImages)
async def get_images(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    name: str = Query(default=None, min_length=3, max_length=25),
):
    total_count, images = await mongo_client.get_processed_images(
        limit=limit,
        offset=offset,
        name=name,
    )

    pagination = Pagination(
        total_count=total_count,
        limit=limit,
        offset=offset,
    )
    return ProcessedImages(images=images, paging=pagination)


@router.get(
    "/images/{image_id}",
    response_class=ImageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"image/jpeg": {}}
        }
    },
)
async def get_specific_image(image_id: str):
    image = await mongo_client.get_processed_image_by_id(_id=image_id)
    return ImageResponse(image)


@router.get("/watermarks", response_model=Watermarks)
async def get_watermarks(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    name: str = Query(default=None, min_length=3, max_length=25),
):
    total_count, images = await mongo_client.get_processed_watermarks(
        limit=limit,
        offset=offset,
        name=name
    )

    pagination = Pagination(
        total_count=total_count,
        limit=limit,
        offset=offset,
    )
    return Watermarks(images=images, paging=pagination)


@router.get(
    "/watermarks/default",
    response_class=ImageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"image/jpeg": {}}
        }
    },
)
async def get_default_watermark():
    watermark = await mongo_client.get_watermark_by_default()
    return ImageResponse(image=watermark)


@router.get(
    "/watermarks/{watermark_id}",
    response_class=ImageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"image/jpeg": {}}
        }
    },
)
async def get_specific_watermark(watermark_id: str):
    watermark = await mongo_client.get_watermark_by_id(_id=watermark_id)
    return ImageResponse(watermark)


# MODIFY ENDPOINTS
@router.put("/watermarks/default")
async def set_default_watermark(watermark: DefaultWatermark):
    await mongo_client.set_default_watermark(watermark.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Default watermark was set"
        }
    )


@router.post("/watermarks/upload")
async def upload_watermark(watermark: EncodedImage):
    object_id = await mongo_client.upload_watermark(watermark)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"result": f"Image was uploaded with id: {object_id}"}
    )


@router.post(
    "/images/process",
    response_model=List[UploadedImage],
)
async def process_images(data: EncodedImages):
    logging.info(f"Received {len(data.images)} images. Start processing...")

    logging.info("Trying to get a watermark...")
    if data.watermark_id:
        watermark = await mongo_client.get_watermark_by_id(data.watermark_id)
    else:
        watermark = await mongo_client.get_watermark_by_default()
    logging.info(f"Watermark {watermark.name} will be used")

    prepared_watermark = prepare_watermark(watermark)

    # Apply watermark on images in coroutines
    uploaded_images = await asyncio.gather(
        *[
            apply_watermark_on_image_and_upload(image, prepared_watermark)
            for image in data.images
        ]
    )
    return uploaded_images
