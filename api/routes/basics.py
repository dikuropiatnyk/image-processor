from fastapi import APIRouter, status
from typing import Optional

from starlette.responses import JSONResponse

from providers import mongo_client

router = APIRouter(tags=["Basics"])


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/up")
async def up(verbose: Optional[bool] = False):
    f_status, f_msg = status.HTTP_200_OK, "Healthy :-)"
    if verbose:
        await mongo_client.verify_connection()

    return JSONResponse(status_code=f_status, content={"condition": f_msg})
