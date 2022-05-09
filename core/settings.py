from pydantic import BaseSettings


class Settings(BaseSettings):
    openio_auth_url: str
    openio_user: str
    openio_secret_key: str
    image_container: str = "images"
    watermark_container: str = "watermarks"


settings = Settings(
    _env_file=".env.secrets",
    _env_file_encoding="utf-8"
)
