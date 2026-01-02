#!/usr/bin/env python3
import uvicorn
import os
from pathlib import Path
import sys

# Add backend folder to path
sys.path.append(str(Path(__file__).parent))

from src.main import app  # Import the FastAPI app

if __name__ == "__main__":
    print("Starting RAG Chatbot backend server...")
    # print("Make sure you have set up environment variables: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, SITEMAP_URL")

    # Use the port from environment/config, default to 8080 if not specified
    host = os.getenv("HOST", "127.0.0.1")  # Use 127.0.0.1 instead of 0.0.0.0 for local dev
    port = int(os.getenv("PORT", 8000))  # Use the configured port from .env

    print(f"Server will run on {host}:{port}")

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True
    )