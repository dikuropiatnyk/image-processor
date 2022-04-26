from fastapi import FastAPI

from api.routes import basics_router, images_router
from core import secrets
from providers import minio_client

app = FastAPI()

# Simple, testing GET endpoints
app.include_router(basics_router)

# Images processing
app.include_router(images_router)

# Provide secret data
secrets.download()

# Initialize providers
minio_client.get_client()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
