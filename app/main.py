from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import auth, admin

app = FastAPI(
    title="Balance App",
    description="Balance App Backend made with FastAPI",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)

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

