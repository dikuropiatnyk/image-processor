from fastapi import FastAPI

from api import router
from core import TimingMiddleware, configure_exception_handlers
from fastapi_pagination import add_pagination
from providers import init_openio, verify_mongo

app = FastAPI()

# Routing
app.include_router(router)

# Provide middleware
app.add_middleware(TimingMiddleware)

# Initialize OpenIO connection
# app.add_event_handler("startup", init_openio)
app.add_event_handler("startup", verify_mongo)

# Provide exception handlers
configure_exception_handlers(app)

# Add pagination for images getter
add_pagination(app)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
