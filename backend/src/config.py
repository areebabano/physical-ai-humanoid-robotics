"""
Environment configuration for different deployment environments
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings that can be configured through environment variables
    """
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./textbook.db")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Physical AI & Humanoid Robotics Textbook API")
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # CORS settings
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Performance settings
    MAX_CONTENT_SIZE: int = int(os.getenv("MAX_CONTENT_SIZE", "10485760"))  # 10MB
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

    # Security settings
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION_MINUTES: int = int(os.getenv("LOCKOUT_DURATION_MINUTES", "15"))

    # Content settings
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")
    SUPPORTED_LANGUAGES: list = os.getenv("SUPPORTED_LANGUAGES", "en,ur").split(",")

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Cache settings
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # 1 hour default
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "1000"))

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # in seconds

    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentSettings(Settings):
    """
    Development-specific settings
    """
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://dev_user:dev_password@localhost/textbook_dev")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")


class ProductionSettings(Settings):
    """
    Production-specific settings
    """
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")

    # In production, these must be set
    @classmethod
    def validate_production_settings(cls):
        required_vars = ["DATABASE_URL", "QDRANT_URL", "OPENAI_API_KEY", "SECRET_KEY"]
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                raise ValueError(f"Required environment variable {var} is not set in production")


class TestingSettings(Settings):
    """
    Testing-specific settings
    """
    DEBUG: bool = True
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://test_user:test_password@localhost/textbook_test")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://test_user:test_password@localhost/textbook_test")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6334")  # Different port for tests
    SECRET_KEY: str = "test-secret-key"


def get_settings() -> Settings:
    """
    Get the appropriate settings based on the environment
    """
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        settings = ProductionSettings()
        # Validate production settings
        ProductionSettings.validate_production_settings()
        return settings
    elif env == "testing":
        return TestingSettings()
    else:  # development
        return DevelopmentSettings()


# Global settings instance
settings = get_settings()


# Helper function to check if running in specific environment
def is_development() -> bool:
    return os.getenv("ENVIRONMENT", "development").lower() == "development"


def is_production() -> bool:
    return os.getenv("ENVIRONMENT", "development").lower() == "production"


def is_testing() -> bool:
    return os.getenv("ENVIRONMENT", "development").lower() == "testing"


# Environment-specific configurations
ENV_CONFIG = {
    "development": {
        "debug": True,
        "log_level": "DEBUG",
        "database_echo": True,  # Log SQL queries in development
    },
    "production": {
        "debug": False,
        "log_level": "WARNING",
        "database_echo": False,
    },
    "testing": {
        "debug": True,
        "log_level": "DEBUG",
        "database_echo": False,  # Usually we don't want to see SQL in tests
    }
}


def get_env_config() -> dict:
    """
    Get environment-specific configuration
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    return ENV_CONFIG.get(env, ENV_CONFIG["development"])


# API-specific configurations
API_CONFIG = {
    "title": settings.APP_NAME,
    "description": "API for the Physical AI & Humanoid Robotics Textbook with RAG chatbot, personalization, and Urdu translation",
    "version": settings.APP_VERSION,
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_url": "/openapi.json"
}