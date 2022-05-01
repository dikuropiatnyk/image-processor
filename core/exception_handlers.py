import logging
from minio.error import MinioException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from urllib3.exceptions import PoolError


async def minio_exception_handler(request: Request, exc: MinioException):
    logging.error(f"MinIO communication error! Details: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal image storage error!"
        }
    )


async def url_connection_exception_handler(request: Request, exc: PoolError):
    logging.error(
        f"Error with a Connections Pool! Details: {exc}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "The image storage didn't respond!"
        }
    )


def configure_exception_handlers(app: FastAPI):
    app.add_exception_handler(MinioException, minio_exception_handler)
    app.add_exception_handler(PoolError, url_connection_exception_handler)
