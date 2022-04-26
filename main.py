from fastapi import FastAPI
from api.routes import router

app = FastAPI()

# Routers
app.include_router(router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
