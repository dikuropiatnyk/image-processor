from fastapi import FastAPI

from api.routes import basics_router, images_router
from core import secrets, TimingMiddleware
from providers import minio_client

app = FastAPI()

# Routing
app.include_router(basics_router)
app.include_router(images_router)

# Provide middleware
app.add_middleware(TimingMiddleware)

# Provide secret data
secrets.download()

# Initialize providers
minio_client.get_client()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
