import logging
import time
import asyncio

from fastapi import APIRouter, status
from typing import Optional

from starlette.responses import JSONResponse

from providers import openio_client

router = APIRouter()


async def item_task(item_num: int, sleep: int):
    logging.info(f"Asynchronously slept for "
                 f"{sleep} seconds for item№{item_num + 1}")
    await asyncio.sleep(sleep)


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/test")
async def test():
    return {
        "storage": openio_client.storage_url,
    }


@router.get("/sync")
def sync_tester(items: int, sleep: int):
    for _ in range(items):
        time.sleep(sleep)
        logging.info(f"Slept for {sleep} seconds")

    return {"status": "Great!"}


@router.get("/async")
async def async_tester(items: int, sleep: int):
    await asyncio.gather(*[item_task(i, sleep) for i in range(items)])

    return {"status": "Great!"}


@router.get("/up")
async def up(verbose: Optional[bool] = False):
    f_status, f_msg = status.HTTP_200_OK, "Healthy :-)"

    if verbose and not await openio_client.healthcheck():
        f_status, f_msg = (
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Unhealthy :-(",
        )

    return JSONResponse(status_code=f_status, content={"condition": f_msg})
