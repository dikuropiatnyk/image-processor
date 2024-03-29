import cv2
import numpy as np
import bson

from typing import Optional, Union

from core import settings
from models import DBImage, EncodedImage, UploadedImage
from providers import mongo_client


def convert_binary_image_to_cv2(
    img_bytes: Union[bytes, bson.Binary]
) -> np.ndarray:
    """
    Binary data should be converted to flat numpy array first,
    and then populated to the cv2 image decoding function
    """
    flat_values = np.asarray(bytearray(img_bytes))
    processed_image = cv2.imdecode(flat_values, cv2.IMREAD_COLOR)
    return processed_image


def convert_cv2_image_to_binary(img_array: np.ndarray) -> bytes:
    return cv2.imencode('.jpg', img_array)[1].tobytes()


def prepare_watermark(db_watermark: DBImage) -> np.ndarray:
    """
    Converts watermark and resized it to the desired shape
    """
    converted_watermark = convert_binary_image_to_cv2(db_watermark.raw_data)
    watermark_resized = cv2.resize(
        converted_watermark,
        (
            settings.WATERMARK_HEIGHT,
            settings.WATERMARK_WIDTH,
        )
    )
    return watermark_resized


async def apply_watermark_on_image_and_upload(
    image: EncodedImage,
    prepared_watermark: np.ndarray,
) -> Optional[UploadedImage]:
    # Raw Data will already be binary because of the validator
    converted_image = convert_binary_image_to_cv2(image.raw_data)
    # Get size of image, but it usually should be fixed
    # (720, 1080)
    h_image, w_image, _ = converted_image.shape

    # Create left top corner of the region to put a watermark
    x = w_image - settings.WATERMARK_WIDTH
    y = h_image - settings.WATERMARK_HEIGHT

    # Region of interest
    roi = converted_image[y:h_image, x:w_image]
    # Add watermark on the region of original image with
    # half-transparent merging
    result = cv2.addWeighted(roi, 1, prepared_watermark, 0.5, 0)
    converted_image[y:h_image, x:w_image] = result
    binary_image = convert_cv2_image_to_binary(converted_image)
    image.raw_data = binary_image

    object_id = await mongo_client.upload_processed_image(image.dict())
    if object_id:
        return UploadedImage(id=str(object_id), name=image.name)
