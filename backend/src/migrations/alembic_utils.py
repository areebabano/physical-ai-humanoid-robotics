"""
Utility functions for Alembic database migrations
"""
import asyncio
import os
from alembic.config import Config
from alembic import command
from pathlib import Path

def get_alembic_config() -> Config:
    """
    Get Alembic configuration
    """
    # Add the project root to Python path for imports
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

    alembic_dir = Path(__file__).parent
    alembic_ini_path = alembic_dir / "alembic.ini"

    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", str(alembic_dir))
    alembic_cfg.set_main_option("config_file", str(alembic_ini_path))

    # Override database URL from environment
    from backend.src.config import settings
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    return alembic_cfg


def run_migrations_current() -> None:
    """
    Run migrations to current state
    """
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")


def create_migration(message: str) -> None:
    """
    Create a new migration with the given message
    """
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, autogenerate=True, message=message)


def downgrade_migration(revision: str = "base") -> None:
    """
    Downgrade to a specific revision (default: base)
    """
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, revision)


def show_current_revision() -> None:
    """
    Show current revision
    """
    alembic_cfg = get_alembic_config()
    command.current(alembic_cfg)


def show_migration_history() -> None:
    """
    Show migration history
    """
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)


async def setup_database() -> None:
    """
    Set up the database with initial migrations
    """
    print("Setting up database with initial migrations...")
    run_migrations_current()
    print("Database setup complete!")


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "upgrade":
            run_migrations_current()
        elif cmd == "create":
            if len(sys.argv) > 2:
                create_migration(sys.argv[2])
            else:
                print("Usage: python alembic_utils.py create <migration_message>")
        elif cmd == "downgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "base"
            downgrade_migration(revision)
        elif cmd == "current":
            show_current_revision()
        elif cmd == "history":
            show_migration_history()
        elif cmd == "setup":
            asyncio.run(setup_database())
        else:
            print("Available commands: upgrade, create <message>, downgrade [revision], current, history, setup")
    else:
        print("Usage: python alembic_utils.py <command> [args]")
        print("Available commands: upgrade, create <message>, downgrade [revision], current, history, setup")