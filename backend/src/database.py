"""
Database connection and initialization module for the Physical AI & Humanoid Robotics Textbook
"""
import os
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/textbook_db")

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session maker
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for dependency injection
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


# Import all models at module level to ensure they are registered with Base
from .models.user_db import User
from .models.textbook_module_db import TextbookModule
from .models.chapter_db import Chapter
from .models.exercise_db import Exercise
from .models.user_progress_db import UserProgress
from .models.translation_db import Translation
from .models.user_db import Base


async def init_db():
    """
    Initialize the database by creating all tables
    """
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close the database engine
    """
    await engine.dispose()