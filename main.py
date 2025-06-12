from fastapi import FastAPI

from app.middleware.cors import setup_cors_middleware
from app.routers.profileFetching import router as profile_fetching_router

APP_PREFIX = "/api/v1"

app = FastAPI(
    title="Real-time Profile Search Service",
    description="AI-powered real-time profile search with content moderation and intelligent query processing",
    version="1.0.0",
    redoc_url=None,
    docs_url=None,
)

setup_cors_middleware(app)

app.include_router(profile_fetching_router, prefix=APP_PREFIX)
