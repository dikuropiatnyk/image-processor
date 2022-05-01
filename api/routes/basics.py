from fastapi import APIRouter, status
from typing import Optional

from starlette.responses import JSONResponse

from providers.minio_connection import MinioConnection

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/up")
async def up(verbose: Optional[bool] = False):
    f_status, f_msg = status.HTTP_200_OK, "Healthy :-)"

    if verbose:
        minio_client = MinioConnection()
        if not minio_client.are_buckets_available():
            f_status, f_msg = (
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "Unhealthy :-(",
            )

    return JSONResponse(status_code=f_status, content={"condition": f_msg})
