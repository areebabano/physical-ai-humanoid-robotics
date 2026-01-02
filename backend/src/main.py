# # from fastapi import FastAPI, WebSocket
# # from fastapi.middleware.cors import CORSMiddleware
# # from .api.chat import router as chat_router
# # from .api.health import router as health_router
# # from .websockets.ws_chat import websocket_endpoint
# # from .core.config import settings, validate_settings
# # from .core.logging import logger


# # # Validate settings before creating the app
# # validate_settings()

# # # Create FastAPI app instance
# # app = FastAPI(
# #     title=settings.API_TITLE,
# #     version=settings.API_VERSION
# # )

# # # Add CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=settings.ALLOWED_ORIGINS,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Register API routers
# # app.include_router(chat_router, prefix="/api/chatbot", tags=["chat"])
# # app.include_router(health_router, tags=["health"])

# # # Register WebSocket endpoint
# # @app.websocket("/ws")
# # async def ws_endpoint(websocket: WebSocket):
# #     await websocket_endpoint(websocket)

# # # Additional root endpoint
# # @app.get("/")
# # async def root():
# #     return {"message": "Physical AI & Humanoid Robotics RAG Chatbot API - Use /api/chatbot/chat for REST or /ws for WebSocket"}


# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(
# #         "src.main:app",
# #         host=settings.HOST,
# #         port=settings.PORT,
# #         reload=True  # Enable auto-reload for development
# #     )

# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from .api.chat import router as chat_router
# from .api.health import router as health_router
# from .websockets.ws_chat import websocket_endpoint
# from .core.config import settings, validate_settings
# from .core.logging import logger

# # Validate settings
# validate_settings()

# # Create FastAPI app
# app = FastAPI(
#     title=settings.API_TITLE,
#     version=settings.API_VERSION
# )

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Register routers
# app.include_router(chat_router, prefix="/api/chatbot", tags=["chat"])
# app.include_router(health_router, tags=["health"])

# # WebSocket
# @app.websocket("/ws")
# async def ws_endpoint(websocket: WebSocket):
#     await websocket_endpoint(websocket)

# # Root endpoint
# @app.get("/")
# async def root():
#     return {"message": "Physical AI & Humanoid Robotics RAG Chatbot API - Use /api/chatbot/chat for REST or /ws for WebSocket"}

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Import routers and websocket
from .api.chat import router as chat_router
from .api.health import router as health_router
from .api.auth import router as auth_router
from .websockets.ws_chat import websocket_endpoint

# Import settings and logging
from .core.config import settings, validate_settings
from .core.logging import logger

# Import database initialization
from .database.init_db import create_db_and_tables

# -----------------------------
# Validate environment variables
# -----------------------------
validate_settings()

# Create database tables
create_db_and_tables()

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION
)

# -----------------------------
# CORS middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register REST API routers
# -----------------------------
app.include_router(chat_router, prefix="/api/chatbot", tags=["chat"])
app.include_router(health_router, tags=["health"])
app.include_router(auth_router)  # Authentication routes

# -----------------------------
# WebSocket endpoint
# -----------------------------
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat
    """
    await websocket_endpoint(websocket)

# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/", name="root_endpoint")
async def root():
    return {
        "message": (
            "Physical AI & Humanoid Robotics RAG Chatbot API - "
            "Use /api/chatbot/chat for REST or /ws for WebSocket"
        )
    }
