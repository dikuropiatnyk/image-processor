import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from aiohttp.client_exceptions import ClientError


async def url_connection_exception_handler(request: Request, exc: ClientError):
    logging.error(
        f"Connection error! Details: {exc}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "The image storage didn't respond!"
        }
    )


def configure_exception_handlers(app: FastAPI):
    app.add_exception_handler(ClientError, url_connection_exception_handler)
