from pydantic import BaseSettings


class Settings(BaseSettings):
    minio_url: str
    minio_access_key: str
    minio_secret_key: str
    image_bucket: str = "images"
    watermark_bucket: str = "watermarks"


settings = Settings(
    _env_file=".env.secrets",
    _env_file_encoding="utf-8"
)
