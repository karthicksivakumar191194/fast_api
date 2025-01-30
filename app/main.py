from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.localization import DynamicLocalizationMiddleware
from app.api.routes import api_router
from app.settings import settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    # Create FastAPI App
    fast_api_app = FastAPI()

    # Include router with versioned prefix
    fast_api_app.include_router(api_router, prefix="")

    # Custom Middlewares
    fast_api_app.add_middleware(DynamicLocalizationMiddleware, default_language="en", supported_languages=["en", "es"])

    # Allow Cross-Origin Resource Sharing (CORS)
    fast_api_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fast_api_app


# Initialize the app
app = create_app()
