from minio import Minio
import logging
import io

from core import secrets


class MinioConnection:

    client = None

    def get_client(self):
        client = Minio(
            secrets.MINIO_URL,
            access_key=secrets.MINIO_ACCESS_KEY,
            secret_key=secrets.MINIO_SECRET_KEY,
            secure=False
        )
        logging.info("Created a new MinIO client!")
        self.client = client

    def send_image(self, image_name, image_bytes, bucket="test"):
        result = self.client.put_object(
            bucket,
            image_name,
            io.BytesIO(image_bytes),
            len(image_bytes),
            content_type="image/jpeg"
        )
        logging.info(
            "Created %s object; etag: %s, version-id: %s",
            result.object_name,
            result.etag,
            result.version_id
        )
