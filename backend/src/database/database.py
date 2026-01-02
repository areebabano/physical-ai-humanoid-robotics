from sqlmodel import create_engine, Session
from ..core.config import settings
import os

# For PostgreSQL with Neon
if os.getenv("TESTING"):
    # Use SQLite for testing
    DATABASE_URL = "sqlite:///./test.db"
else:
    # Use PostgreSQL for production
    DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    # Add connect_args for SQLite if needed
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)


def get_db():
    with Session(engine) as session:
        yield session