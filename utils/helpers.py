import asyncio
import time
import logging
from functools import wraps
from typing import Iterator, List
from minio.datatypes import Object

from models import MinioImage


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


def map_images(images_gen: Iterator[Object]) -> List[MinioImage]:
    return [
        MinioImage(
            id=image.etag,
            image_name=image.object_name,
            timestamp=image.last_modified,
            image_size=round(image.size / 1024, 2)
        )
        for image in images_gen
    ]
