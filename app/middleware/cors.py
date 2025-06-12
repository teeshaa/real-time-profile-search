from fastapi.middleware.cors import CORSMiddleware


def setup_cors_middleware(app):
    """Add CORS middleware to the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
