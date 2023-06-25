import logging

from fastapi import APIRouter, Query

from core import ImageResponse
from models import Pagination, ProcessedImages, Watermarks
from providers import mongo_client


router = APIRouter(prefix="/mongo")


@router.get("/images", response_model=ProcessedImages)
async def get_images(
    limit: int = Query(default=1, ge=1, le=50),
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
    responses={
        200: {
            "content": {"image/jpeg": {}}
        }
    },
)
async def get_specific_image(image_id: str):
    image = await mongo_client.get_processed_image_by_id(_id=image_id)
    return ImageResponse(image)


@router.get("/watermarks", response_model=Watermarks)
async def get_watermarks(
    limit: int = Query(default=1, ge=1, le=50),
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
    responses={
        200: {
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
    responses={
        200: {
            "content": {"image/jpeg": {}}
        }
    },
)
async def get_specific_watermark(watermark_id: str):
    watermark = await mongo_client.get_watermark_by_id(_id=watermark_id)
    return ImageResponse(watermark)


