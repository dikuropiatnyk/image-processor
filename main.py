from fastapi import FastAPI

from api import router
from core import TimingMiddleware, configure_exception_handlers
from fastapi_pagination import add_pagination

app = FastAPI()

# Routing
app.include_router(router)

# Provide middleware
app.add_middleware(TimingMiddleware)

# Provide exception handlers
configure_exception_handlers(app)

# Add pagination for images getter
add_pagination(app)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
