"""
Main FastAPI application for the Physical AI & Humanoid Robotics Textbook
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
import os
import sys
from typing import AsyncGenerator

from backend.src.database import init_db, close_db
from backend.src.services.auth_service import get_current_user
from backend.src.api.textbook_router import router as textbook_router
from backend.src.api.chatbot_router import router as chatbot_router
from backend.src.api.auth_router import router as auth_router
from backend.src.api.translation_router import router as translation_router
from backend.src.api.personalization_router import router as personalization_router
from backend.src.api.exercise_router import router as exercise_router
from backend.src.utils.error_handler import ErrorHandlingMiddleware, http_exception_handler, validation_exception_handler, general_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for FastAPI
    """
    logger.info("Starting up the application...")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Initialize other services if needed
    # For example, initialize Qdrant connection, etc.

    yield

    # Cleanup
    await close_db()
    logger.info("Application shutdown complete")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="API for the Physical AI & Humanoid Robotics Textbook with RAG chatbot, personalization, and Urdu translation",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS middleware
# In production, specify exact origins instead of wildcard
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers for client access
    expose_headers=["Access-Control-Allow-Origin"]
)


# Add GZip compression middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # Compress responses larger than 1KB
)


# Add error handling middleware
app.add_middleware(
    ErrorHandlingMiddleware
)


# Add custom middleware for request logging
@app.middleware("http")
async def log_requests(request, call_next):
    """
    Middleware to log incoming requests
    """
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


# Add custom middleware for authentication (if needed globally)
@app.middleware("http")
async def add_current_user_to_request(request, call_next):
    """
    Middleware to add current user to request state if authenticated
    """
    # Extract token from headers if present
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix

        # Try to get current user (this will fail silently if token is invalid)
        try:
            # In a real implementation, we'd validate the token here
            # For now, we'll skip adding user to request state to avoid errors
            pass
        except:
            # If token validation fails, continue without current user
            pass

    response = await call_next(request)
    return response


# Include API routers
app.include_router(textbook_router, prefix="/api/textbook", tags=["textbook"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(translation_router, prefix="/api/translation", tags=["translation"])
app.include_router(personalization_router, prefix="/api/personalization", tags=["personalization"])
app.include_router(exercise_router, prefix="/api/exercise", tags=["exercise"])


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint to verify the API is running
    """
    return {
        "status": "healthy",
        "message": "Physical AI & Humanoid Robotics Textbook API is running"
    }


# Root endpoint
@app.get("/", tags=["root"])
async def read_root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to the Physical AI & Humanoid Robotics Textbook API",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc"
    }


# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Handle 404 errors
    """
    from backend.src.utils.error_handler import APIError
    return APIError.not_found()


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Handle 500 errors
    """
    logger.error(f"Internal server error: {exc}")
    from backend.src.utils.error_handler import APIError
    return APIError.internal_error()


# Include other middleware as needed
# For example, rate limiting, request validation, etc.