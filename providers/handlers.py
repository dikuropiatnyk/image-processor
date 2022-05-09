import logging
from typing import Tuple, List, Dict
from aiohttp import ClientResponse
from fastapi import HTTPException, status

from core import settings
from models import OpenioImage
from utils.helpers import map_images


async def containers_check_handler(response: ClientResponse) -> bool:
    """
    Checks if all the needed containers are available in the storage
    """
    expected_containers = (
        settings.image_container,
        settings.watermark_container,
    )

    # There can be only unique container names,
    # so the filtration subset length should be identical
    all_containers = await response.json()
    found_containers = list(
        filter(
            lambda c: c["name"] in expected_containers,
            all_containers
        )
    )

    return len(expected_containers) == len(found_containers)


async def headers_handler(
    response: ClientResponse,
    headers: Tuple,
) -> List[str]:
    """
    General handler for empty content requests, which store needed data
    within headers

    :return: list of values for found headers
    """
    result = []
    await response.text()

    for exp_header in headers:
        if header_value := response.headers.get(exp_header, ""):
            result.append(header_value)
        else:
            logging.error("Missing required header `%s`", exp_header)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Image storage interaction error!"
            )

    return result


async def objects_list_handler(response: ClientResponse) -> List[OpenioImage]:
    images_data = await response.json()
    images = map_images(images_data)
    return images

