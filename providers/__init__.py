from .openio_connection import OpenIOConnection
from .mongo_connection import MongoDBConnection

openio_client = OpenIOConnection()
mongo_client = MongoDBConnection()


async def verify_mongo():
    await mongo_client.verify_connection()

async def init_openio():
    await openio_client.create_connection()
