from fastapi.responses import Response

from models import DBImage


class ImageResponse(Response):
    """
    Inherits from the generic FastAPI response class, adds some
    typical headers and calls for the original init method
    """

    def __init__(self, image: DBImage, *args, **kwargs):
        super().__init__(
            content=image.raw_data,
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f'attachment; filename={image.name}',
                "Content-Length": str(len(image.raw_data)),
            },
            *args,
            **kwargs,
        )
