from fastapi import FastAPI

from api import router
from core import TimingMiddleware, configure_exception_handlers
from providers import verify_mongo

app = FastAPI()

# Routing
app.include_router(router)

# Provide middleware
app.add_middleware(TimingMiddleware)

# Verify MongoDB connection
app.add_event_handler("startup", verify_mongo)

# Provide exception handlers
configure_exception_handlers(app)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
