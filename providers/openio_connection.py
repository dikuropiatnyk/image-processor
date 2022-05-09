import logging
import io
import aiohttp
from fastapi import HTTPException, status
from typing import Any, List
from functools import partial

from core import settings
from providers.handlers import (
    containers_check_handler,
    headers_handler,
    objects_list_handler,
)
from utils.helpers import refresh_token
from models import OpenioImage


async def request(
    method: str,
    url: str,
    headers: dict,
    exp_content_type: str,
    response_handler: callable,
    **kwargs
) -> Any:
    """
    General wrapper to execute request asynchronously and handle
    its response via a passed function

    :param method: HTTP request method
    :param url: full URL of future request
    :param headers: dictionary of headers
    :param exp_content_type: expected content type of the response
    :param response_handler: function to process response
    :return: whatever the response handler will return
    """
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs,
        ) as response:
            response.raise_for_status()
            if response.content_type != exp_content_type:
                logging.error(
                    "Response content type is unexpected! "
                    "URL: %s; Method: %s; Expected: %s; Received: %s",
                    url,
                    method,
                    exp_content_type,
                    response.content_type
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Image storage provided an unexpected response!"
                )

            return await response_handler(response)


class OpenIOConnection:
    storage_url = None
    _auth_header = {}

    AUTH_HEADERS = ("X-Storage-Url", "X-Auth-Token")
    IMAGE_HEADERS = ("ETag", "Last-Modified")

    async def create_connection(self):
        credentials = await request(
            method="GET",
            url=settings.openio_auth_url,
            headers={
                "X-Auth-User": settings.openio_user,
                "X-Auth-Key": settings.openio_secret_key,
            },
            exp_content_type="text/html",
            response_handler=partial(
                headers_handler,
                headers=self.AUTH_HEADERS
            ),
        )

        self.storage_url = credentials[0]
        self._auth_header = {
            "X-Auth-Token": credentials[1]
        }

        logging.info(
            "Connected to the OpenIO storage! URL: %s",
            self.storage_url
        )

    @refresh_token
    async def healthcheck(self) -> bool:
        logging.info("Starting containers availability check")
        containers_exist = await request(
            method="GET",
            url=f"{self.storage_url}?format=json",
            headers=self._auth_header,
            exp_content_type="application/json",
            response_handler=containers_check_handler,
        )

        if not containers_exist:
            logging.error("Not all containers are available!")

        return containers_exist

    @refresh_token
    async def send_image(
        self,
        image_name: str,
        image_bytes: bytes,
        container=settings.image_container
    ) -> List[str]:
        # Extend auth headers with image-specific ones
        headers = {
            "Content-Type": "image/jpeg",
            "Content-Length": str(len(image_bytes)),
        } | self._auth_header

        logging.info("Send image '%s'", image_name)

        result = await request(
            method="PUT",
            url=f"{self.storage_url}/{container}/{image_name}",
            headers=headers,
            exp_content_type="text/html",
            response_handler=partial(
                headers_handler,
                headers=self.IMAGE_HEADERS
            ),
            data=io.BytesIO(image_bytes),
        )

        logging.info(
            "Created %s object; etag: %s; date: %s",
            image_name,
            result[0].strip('"'),
            result[1],
        )
        return result

    @refresh_token
    async def get_images(self) -> List[OpenioImage]:
        logging.info(
            "Getting images list from `%s` container",
            settings.image_container
        )
        images = await request(
            method="GET",
            url=f"{self.storage_url}/{settings.image_container}?format=json",
            headers=self._auth_header,
            exp_content_type="application/json",
            response_handler=objects_list_handler,
        )
        logging.info("Total images count: %s", len(images))

        return images

