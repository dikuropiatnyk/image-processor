from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = "processor"
    IMAGE_CONTAINER: str = "images"
    WATERMARK_CONTAINER: str = "watermarks"
    MONGO_USER: str
    MONGO_PWD: str
    MONGO_URL: str
    WATERMARK_HEIGHT: int = 100
    WATERMARK_WIDTH: int = 100


settings = Settings(
    _env_file=".env.secrets",
    _env_file_encoding="utf-8"
)
