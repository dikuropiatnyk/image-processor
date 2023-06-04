import base64

from models import EncodedImage, OpenioCreateResponse
from providers import openio_client


async def process_image(image: EncodedImage) -> OpenioCreateResponse:
    decoded_object = base64.decodebytes(str.encode(image.Encoded))
    result = await openio_client.send_image(image.Name, decoded_object)
    return OpenioCreateResponse(
        object_name=image.Name,
        etag=result[0].strip('"'),
        last_modified=result[1],
    )
