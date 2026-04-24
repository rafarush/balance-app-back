from fastapi import FastAPI

app = FastAPI(
    title="Balance App",
    description="Balance App Backend made with FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "app_name": "balance-app-back",
        "status": "healthy",
        "documentation": {
            "swagger_url": "/docs",
            "redoc_url": "/redoc",
        },
    }

