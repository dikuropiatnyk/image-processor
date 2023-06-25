import logging
import motor.motor_asyncio

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from motor.core import AgnosticCollection
from typing import Type, Optional

from core import settings
from models import DBImage, OutputProcessedImage, OutputWatermark


class MongoDBConnection:
    """
    Helper class to provide typical operations with MongoDB instance
    """

    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{settings.mongo_user}:"
            f"{settings.mongo_pwd}@{settings.mongo_url}",
            serverSelectionTimeoutMS=5000,
        )
        self._db = getattr(self._client, settings.db_name)
        self.images: AgnosticCollection = getattr(
            self._db,
            settings.image_container,
        )
        self.watermarks: AgnosticCollection = getattr(
            self._db,
            settings.watermark_container,
        )

    @classmethod
    async def upload_image_document(
        cls,
        image_document: dict,
        collection: AgnosticCollection,
    ):
        logging.info(f"Adding image to the {collection.name}")
        result = await collection.insert_one(image_document)
        logging.info(f"Added object with ID: {repr(result.inserted_id)}")
        return result.inserted_id

    @classmethod
    async def get_images(
        cls,
        collection: AgnosticCollection,
        limit: int,
        offset: int,
        response_class: Type,
        name: Optional[str],
    ) -> (int, list):
        """
        Validates the amount of available images, and applies the
        pagination parameters

        :param collection: desired collection object
        :param limit: amount of records per page
        :param offset: amount of records to skip before the retrieving
        :param response_class: response class to process results
        :param name: search pattern for the image name
        :return:
        """
        logging.info(f"Trying to get available images in {collection.name}")

        search_filter = {"name": {"$regex": f"{name}"}} if name else dict()
        total_count = await collection.count_documents(search_filter)
        # Prepare a cursor, which gets all appropriate documents,
        # but excluded a binary data from the response
        cursor = collection.find(search_filter, {"raw_data": 0})
        # Apply pagination
        cursor.skip(offset).limit(limit)

        results = []
        for result in await cursor.to_list(length=limit):
            # ID should be processed separately
            results.append(response_class(id=str(result.pop("_id")), **result))
        return total_count, results

    @classmethod
    async def get_specific_image_by_filters(
        cls,
        collection: AgnosticCollection,
        filters: dict,
    ) -> DBImage:
        """
        Returns first entry, which fulfills filters
        """
        logging.info(f"Trying to find an image by filter: {filters}")

        db_result = await collection.find_one(filters)
        if not db_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no such image!"
            )
        image = DBImage(**db_result)
        return image

    async def verify_connection(self):
        logging.info("Try to connect to the database...")
        await self._client.admin.command("ping")
        logging.info("Connection successful!")

    async def upload_processed_image(
        self,
        processed_image: dict,
    ):
        object_id = self.upload_image_document(
            image_document=processed_image,
            collection=self.images,
        )
        return object_id

    async def upload_watermark(
        self,
        watermark: dict,
    ):
        object_id = self.upload_image_document(
            image_document=watermark,
            collection=self.watermarks,
        )
        return object_id

    async def get_processed_images(
        self,
        limit: int = 0,
        offset: int = 0,
        name: Optional[str] = None,
    ) -> (int, list[OutputProcessedImage]):
        """
        Validates the amount of available images, and applies the
        pagination parameters
        """

        total_count, results = await self.get_images(
            collection=self.images,
            limit=limit,
            offset=offset,
            response_class=OutputProcessedImage,
            name=name,
        )

        return total_count, results

    async def get_processed_image_by_id(self, _id: str) -> DBImage:
        if not ObjectId.is_valid(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no such image!"
            )
        filters = {
            "_id": {
                "$eq": ObjectId(_id),
            }
        }
        return await self.get_specific_image_by_filters(
            collection=self.images,
            filters=filters,
        )

    async def get_processed_watermarks(
        self,
        limit: int = 0,
        offset: int = 0,
        name: Optional[str] = None,
    ) -> (int, list[OutputWatermark]):
        """
        Validates the amount of available images, and applies the
        pagination parameters
        """

        total_count, results = await self.get_images(
            collection=self.watermarks,
            limit=limit,
            offset=offset,
            response_class=OutputWatermark,
            name=name,
        )

        return total_count, results

    async def get_watermark_by_id(self, _id: str) -> DBImage:
        if not ObjectId.is_valid(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no such image!"
            )
        filters = {
            "_id": {
                "$eq": ObjectId(_id),
            }
        }
        return await self.get_specific_image_by_filters(
            collection=self.watermarks,
            filters=filters,
        )

    async def get_watermark_by_default(self) -> DBImage:
        filters = {
            "is_default": {
                "$eq": True,
            }
        }
        return await self.get_specific_image_by_filters(
            collection=self.watermarks,
            filters=filters,
        )
