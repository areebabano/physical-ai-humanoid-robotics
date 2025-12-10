"""
TextbookModule service for the Physical AI & Humanoid Robotics Textbook
Handles module operations including creation, retrieval, and management
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.src.models.textbook_module_db import TextbookModule
from backend.src.models.chapter_db import Chapter
from backend.src.database import get_db_session
from backend.src.utils.logging_config import get_logger, log_user_action

logger = get_logger(__name__)


class TextbookModuleService:
    """
    Service class for handling textbook module operations
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    async def create_module(
        self,
        db_session: AsyncSession,
        title: str,
        description: Optional[str],
        module_number: int,
        weeks_duration: int,
        programming_language: str = "Python"
    ) -> TextbookModule:
        """
        Create a new textbook module
        """
        try:
            # Check if module number already exists
            existing_module = await db_session.execute(
                select(TextbookModule).where(TextbookModule.module_number == module_number)
            )
            if existing_module.scalars().first():
                raise ValueError(f"Module with number {module_number} already exists")

            module = TextbookModule(
                title=title,
                description=description,
                module_number=module_number,
                weeks_duration=weeks_duration,
                programming_language=programming_language
            )

            db_session.add(module)
            await db_session.commit()
            await db_session.refresh(module)

            self.logger.info(f"Created textbook module: {module.title} (ID: {module.id})")
            log_user_action(
                logger=self.logger,
                user_id="system",  # This would be a real user ID in actual implementation
                action="create_module",
                details={"module_id": str(module.id), "module_title": module.title}
            )

            return module

        except Exception as e:
            self.logger.error(f"Error creating textbook module: {str(e)}")
            await db_session.rollback()
            raise

    async def get_module_by_id(
        self,
        db_session: AsyncSession,
        module_id: uuid.UUID
    ) -> Optional[TextbookModule]:
        """
        Get a textbook module by its ID
        """
        try:
            result = await db_session.execute(
                select(TextbookModule)
                .where(TextbookModule.id == module_id)
            )
            module = result.scalars().first()

            if module:
                self.logger.info(f"Retrieved textbook module: {module.title} (ID: {module.id})")

            return module

        except Exception as e:
            self.logger.error(f"Error retrieving textbook module {module_id}: {str(e)}")
            raise

    async def get_module_by_number(
        self,
        db_session: AsyncSession,
        module_number: int
    ) -> Optional[TextbookModule]:
        """
        Get a textbook module by its module number
        """
        try:
            result = await db_session.execute(
                select(TextbookModule)
                .where(TextbookModule.module_number == module_number)
            )
            module = result.scalars().first()

            if module:
                self.logger.info(f"Retrieved textbook module: {module.title} (Number: {module.module_number})")

            return module

        except Exception as e:
            self.logger.error(f"Error retrieving textbook module with number {module_number}: {str(e)}")
            raise

    async def get_all_modules(
        self,
        db_session: AsyncSession
    ) -> List[TextbookModule]:
        """
        Get all textbook modules
        """
        try:
            result = await db_session.execute(
                select(TextbookModule)
                .order_by(TextbookModule.module_number)
            )
            modules = result.scalars().all()

            self.logger.info(f"Retrieved {len(modules)} textbook modules")

            return modules

        except Exception as e:
            self.logger.error(f"Error retrieving textbook modules: {str(e)}")
            raise

    async def update_module(
        self,
        db_session: AsyncSession,
        module_id: uuid.UUID,
        **kwargs
    ) -> Optional[TextbookModule]:
        """
        Update a textbook module
        """
        try:
            result = await db_session.execute(
                select(TextbookModule)
                .where(TextbookModule.id == module_id)
            )
            module = result.scalars().first()

            if not module:
                return None

            # Update fields that are provided
            for field, value in kwargs.items():
                if hasattr(module, field) and field not in ['id', 'created_at']:
                    setattr(module, field, value)

            await db_session.commit()
            await db_session.refresh(module)

            self.logger.info(f"Updated textbook module: {module.title} (ID: {module.id})")
            log_user_action(
                logger=self.logger,
                user_id="system",  # This would be a real user ID in actual implementation
                action="update_module",
                details={"module_id": str(module.id), "module_title": module.title}
            )

            return module

        except Exception as e:
            self.logger.error(f"Error updating textbook module {module_id}: {str(e)}")
            await db_session.rollback()
            raise

    async def delete_module(
        self,
        db_session: AsyncSession,
        module_id: uuid.UUID
    ) -> bool:
        """
        Delete a textbook module
        """
        try:
            result = await db_session.execute(
                select(TextbookModule)
                .where(TextbookModule.id == module_id)
            )
            module = result.scalars().first()

            if not module:
                return False

            await db_session.delete(module)
            await db_session.commit()

            self.logger.info(f"Deleted textbook module: {module.title} (ID: {module.id})")
            log_user_action(
                logger=self.logger,
                user_id="system",  # This would be a real user ID in actual implementation
                action="delete_module",
                details={"module_id": str(module.id), "module_title": module.title}
            )

            return True

        except Exception as e:
            self.logger.error(f"Error deleting textbook module {module_id}: {str(e)}")
            await db_session.rollback()
            raise

    async def get_module_with_chapters(
        self,
        db_session: AsyncSession,
        module_id: uuid.UUID
    ) -> Optional[Dict[str, Any]]:
        """
        Get a textbook module with its associated chapters
        """
        try:
            result = await db_session.execute(
                select(TextbookModule)
                .options(selectinload(TextbookModule.chapters))
                .where(TextbookModule.id == module_id)
            )
            module = result.scalars().first()

            if module:
                # Convert to dict format for API response
                module_data = {
                    "id": str(module.id),
                    "title": module.title,
                    "description": module.description,
                    "module_number": module.module_number,
                    "weeks_duration": module.weeks_duration,
                    "programming_language": module.programming_language,
                    "created_at": module.created_at.isoformat(),
                    "updated_at": module.updated_at.isoformat() if module.updated_at else None,
                    "chapters": []
                }

                # Add chapters to the response
                for chapter in module.chapters:
                    chapter_data = {
                        "id": str(chapter.id),
                        "title": chapter.title,
                        "chapter_number": chapter.chapter_number,
                        "slug": chapter.slug,
                        "learning_objectives": chapter.learning_objectives,
                        "created_at": chapter.created_at.isoformat(),
                        "updated_at": chapter.updated_at.isoformat() if chapter.updated_at else None
                    }
                    module_data["chapters"].append(chapter_data)

                return module_data

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving textbook module with chapters {module_id}: {str(e)}")
            raise


# Global instance of the service
textbook_module_service = TextbookModuleService()