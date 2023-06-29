import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_NAME: str = "processor"
    IMAGE_CONTAINER: str = "images"
    WATERMARK_CONTAINER: str = "watermarks"
    WATERMARK_HEIGHT: int = 100
    WATERMARK_WIDTH: int = 100
    MONGO_USER: str = Field(env="MONGO_USER")
    MONGO_PWD: str = Field(env="MONGO_PWD")
    MONGO_URL: str = Field(env="MONGO_URL")


def get_settings():
    env = os.getenv("ENV")
    if env == "local":
        _settings = Settings(
            _env_file=".env.secrets",
            _env_file_encoding="utf-8"
        )
    elif env == "remote":
        _settings = Settings()
    else:
        raise RuntimeError(f'Insufficient environment parameter: "{env}"')

    return _settings


settings = get_settings()
