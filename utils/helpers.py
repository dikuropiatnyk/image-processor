import asyncio
import time
import logging
from functools import wraps
from typing import Iterator, List, Dict
from aiohttp.client_exceptions import ClientResponseError
from fastapi import status

from models import OpenioImage


def _log_timing(func, start, finish):
    """
    General helper to calculate total execution time for a function
    :param func: function to track
    :param start: initial timestamp
    :param finish: final timestamp
    :return: None
    """

    total_time = round(finish - start, 3)
    log = logging.debug if total_time > 2 else logging.info

    log(f"Spent time on {func.__name__}: {total_time}s")


def async_log_timing(func):
    """
    Asynchronous decorator for time tracking
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        now = asyncio.get_event_loop().time
        start = now()
        result = await func(*args, **kwargs)
        _log_timing(func, start, now())

        return result

    return wrapper


def refresh_token(method):
    """
    Class decorator for OpenIO authorized requests
    Executes method and tries to refresh the auth token
    """
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        retries = 2
        while retries:
            try:
                result = await method(self, *args, **kwargs)
                return result
            except ClientResponseError as err:
                if err.status == status.HTTP_401_UNAUTHORIZED and retries > 1:
                    # Try to refresh token, if it's first such error
                    logging.warning("Auth token is outdated, try to refresh")
                    await asyncio.sleep(2)
                    await self.create_connection()
                    retries -= 1
                    continue
                raise err from None
    return wrapper


def log_timing(func):
    """
    Synchronous decorator for time tracking
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        _log_timing(func, start, time.time())

        return result

    return wrapper


def map_images(images_gen: Iterator[Dict]) -> List[OpenioImage]:
    return [
        OpenioImage(
            id=image["hash"],
            image_name=image["name"],
            timestamp=image["last_modified"],
            image_size=round(image["bytes"] / 1024, 2)
        )
        for image in images_gen
    ]
