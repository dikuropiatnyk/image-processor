from .mongo_connection import MongoDBConnection

mongo_client = MongoDBConnection()


async def verify_mongo():
    await mongo_client.verify_connection()
