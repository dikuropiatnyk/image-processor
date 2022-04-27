import asyncio
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.middleware.base import RequestResponseEndpoint


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware to track total time of the request execution
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ):
        now = asyncio.get_event_loop().time
        start = now()
        response = await call_next(request)
        total_time = round(now() - start, 3)
        logging.info(f"Spent time on `{request.url.path}`: {total_time}s")
        return response
