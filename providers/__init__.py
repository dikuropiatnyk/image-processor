from .openio_connection import OpenIOConnection

openio_client = OpenIOConnection()


async def init_openio():
    await openio_client.create_connection()
