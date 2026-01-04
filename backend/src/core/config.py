from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "Physical AI & Humanoid Robotics RAG Chatbot"
    API_VERSION: str = "1.0.0"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8080"))

    # Database Configuration
    DB_USER: str = os.getenv("DB_USER", "neondb_owner")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST", "ep-xxx.us-east-1.aws.neon.tech")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "neondb")

    # CORS Configuration
    # ALLOWED_ORIGINS: list = ["http://localhost:3000","http://localhost:3001"]  # In production, specify exact origins
    ALLOWED_ORIGINS: list = ["*","http://localhost:3000","http://localhost:3001", "https://physical-ai-humanoid-robotics-wheat-alpha.vercel.app/"]  # In production, specify exact origins


    # Cohere Configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "embed-english-v3.0")

    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "physical-ai-humanoid_robotics")
    INGESTION_COLLECTION_NAME: str = os.getenv("INGESTION_COLLECTION_NAME", "physical-ai-humanoid_robotics_book")

    # Google Gemini Configuration (for alternative embedding service)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL", "embedding-001")
    GEMINI_CHAT_MODEL: str = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.0-flash")

    # Sitemap Configuration
    SITEMAP_URL: str = os.getenv("SITEMAP_URL", "https://physical-ai-humanoid-robotics-khbj.vercel.app/sitemap.xml")

    # Model Configuration
    GENERATION_MODEL: str = os.getenv("GENERATION_MODEL", "command-r-plus")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "500"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.3"))

    # Retrieval Configuration
    RETRIEVAL_LIMIT: int = int(os.getenv("RETRIEVAL_LIMIT", "5"))

    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-in-production")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


# Create a single instance of settings
settings = Settings()


def validate_settings():
    """Validate that required environment variables are set"""
    if not settings.COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable is required")

    if not settings.QDRANT_URL or not settings.QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

    if not settings.DB_PASSWORD:
        raise ValueError("DB_PASSWORD environment variable is required for database connection")

    if settings.JWT_SECRET_KEY == "your-default-secret-key-change-in-production":
        print("WARNING: Using default JWT secret key. Please set JWT_SECRET_KEY in your .env file for production use.")