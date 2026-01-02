import os
import sys
from pathlib import Path
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add backend to Python path
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

# Now run the application
if __name__ == "__main__":
    import uvicorn
    print("Starting RAG Chatbot backend server...")
    print("Make sure you have set up your environment variables:")
    print("- COHERE_API_KEY")
    print("- QDRANT_URL")
    print("- QDRANT_API_KEY")
    print("- SITEMAP_URL (for content ingestion)")
    # Use the port from environment/config, default to 8080 if not specified
    host = os.getenv("HOST", "0.0.0.0")  # Use 0.0.0.0 to allow external connections
    port = int(os.getenv("PORT", 8080))  # Use the configured port from .env

    print(f"Server will run on {host}:{port}")

    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=[str(project_root)]
    )