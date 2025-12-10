import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# Import your SQLAlchemy models here
from backend.src.models.user_db import User as UserTable
from backend.src.models.textbook_module_db import TextbookModule as TextbookModuleTable
from backend.src.models.chapter_db import Chapter as ChapterTable
from backend.src.models.exercise_db import Exercise as ExerciseTable
from backend.src.models.user_progress_db import UserProgress as UserProgressTable
from backend.src.models.translation_db import Translation as TranslationTable
from backend.src.config import settings

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The MetaData object for autogenerate support
target_metadata = None

# Collect all table metadata from your models
def get_model_tables():
    """Get all model tables to include in migrations"""
    from sqlalchemy import MetaData
    metadata = MetaData()

    # Import all table objects
    tables = [
        UserTable.__table__,
        TextbookModuleTable.__table__,
        ChapterTable.__table__,
        ExerciseTable.__table__,
        UserProgressTable.__table__,
        TranslationTable.__table__,
    ]

    # Create a new metadata object and add all tables
    for table in tables:
        table.tometadata(metadata)

    return metadata

# Set target_metadata
target_metadata = get_model_tables()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Don't run migrations when just importing the file (for autogenerate)
    # This is only for when Alembic is actually running migrations
    if os.environ.get('RUNNING_MIGRATIONS'):
        asyncio.run(run_migrations_online())