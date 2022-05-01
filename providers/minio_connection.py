import logging
import io

from minio import Minio
from minio.helpers import ObjectWriteResult
from minio.datatypes import Object
from typing import Iterator

from core import settings


class MinioConnection:

    client = None

    def __init__(self):
        client = Minio(
            settings.minio_url,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False
        )
        logging.info("Created a new MinIO client!")
        self.client = client

    def send_image(
        self,
        image_name,
        image_bytes,
        bucket=settings.image_bucket
    ) -> ObjectWriteResult:
        logging.info("Send image '%s'", image_name)
        result = self.client.put_object(
            bucket,
            image_name,
            io.BytesIO(image_bytes),
            len(image_bytes),
            content_type="image/jpeg"
        )
        logging.info(
            "Created %s object; etag: %s",
            result.object_name,
            result.etag
        )
        return result

    def are_buckets_available(self) -> bool:
        for bucket in (settings.image_bucket, settings.watermark_bucket):
            if not self.client.bucket_exists(bucket):
                logging.error(f"Bucket {bucket} doesn't exist!")
                return False
        return True

    def get_images(
        self,
        bucket: str = settings.image_bucket
    ) -> Iterator[Object]:
        logging.info(f"Getting images list from `{bucket}` bucket")
        return self.client.list_objects(bucket)
