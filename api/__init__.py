from fastapi import APIRouter

from .routes import basics_router, images_router

router = APIRouter()

router.include_router(basics_router)
router.include_router(images_router)
