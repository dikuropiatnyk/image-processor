from fastapi import APIRouter, status
from typing import Optional

from starlette.responses import JSONResponse

from providers import openio_client

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/up")
async def up(verbose: Optional[bool] = False):
    f_status, f_msg = status.HTTP_200_OK, "Healthy :-)"

    if verbose and not await openio_client.healthcheck():
        f_status, f_msg = (
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Unhealthy :-(",
        )

    return JSONResponse(status_code=f_status, content={"condition": f_msg})
