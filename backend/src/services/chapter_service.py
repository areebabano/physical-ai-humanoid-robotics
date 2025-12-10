"""
Chapter service for the Physical AI & Humanoid Robotics Textbook
Handles chapter operations including creation, retrieval, and management
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.src.models.chapter_db import Chapter
from backend.src.models.textbook_module_db import TextbookModule
from backend.src.database import get_db_session
from backend.src.utils.logging_config import get_logger, log_user_action

logger = get_logger(__name__)


class ChapterService:
    """
    Service class for handling chapter operations
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    async def create_chapter(
        self,
        db_session: AsyncSession,
        title: str,
        content: str,
        module_id: uuid.UUID,
        chapter_number: int,
        slug: str,
        learning_objectives: Optional[str] = None,
        exercises: Optional[str] = None
    ) -> Chapter:
        """
        Create a new chapter
        """
        try:
            # Check if chapter with same slug already exists
            existing_chapter = await db_session.execute(
                select(Chapter).where(Chapter.slug == slug)
            )
            if existing_chapter.scalars().first():
                raise ValueError(f"Chapter with slug '{slug}' already exists")

            # Check if module exists
            module_result = await db_session.execute(
                select(TextbookModule).where(TextbookModule.id == module_id)
            )
            module = module_result.scalars().first()
            if not module:
                raise ValueError(f"Module with ID {module_id} does not exist")

            # Check if chapter number already exists in this module
            existing_chapter_number = await db_session.execute(
                select(Chapter)
                .where(Chapter.module_id == module_id)
                .where(Chapter.chapter_number == chapter_number)
            )
            if existing_chapter_number.scalars().first():
                raise ValueError(f"Chapter number {chapter_number} already exists in module {module_id}")

            chapter = Chapter(
                title=title,
                content=content,
                module_id=module_id,
                chapter_number=chapter_number,
                slug=slug,
                learning_objectives=learning_objectives,
                exercises=exercises
            )

            db_session.add(chapter)
            await db_session.commit()
            await db_session.refresh(chapter)

            self.logger.info(f"Created chapter: {chapter.title} (ID: {chapter.id})")
            log_user_action(
                logger=self.logger,
                user_id="system",  # This would be a real user ID in actual implementation
                action="create_chapter",
                details={"chapter_id": str(chapter.id), "chapter_title": chapter.title, "module_id": str(module_id)}
            )

            return chapter

        except Exception as e:
            self.logger.error(f"Error creating chapter: {str(e)}")
            await db_session.rollback()
            raise

    async def get_chapter_by_id(
        self,
        db_session: AsyncSession,
        chapter_id: uuid.UUID
    ) -> Optional[Chapter]:
        """
        Get a chapter by its ID
        """
        try:
            result = await db_session.execute(
                select(Chapter)
                .where(Chapter.id == chapter_id)
            )
            chapter = result.scalars().first()

            if chapter:
                self.logger.info(f"Retrieved chapter: {chapter.title} (ID: {chapter.id})")

            return chapter

        except Exception as e:
            self.logger.error(f"Error retrieving chapter {chapter_id}: {str(e)}")
            raise

    async def get_chapter_by_slug(
        self,
        db_session: AsyncSession,
        slug: str
    ) -> Optional[Chapter]:
        """
        Get a chapter by its slug
        """
        try:
            result = await db_session.execute(
                select(Chapter)
                .where(Chapter.slug == slug)
            )
            chapter = result.scalars().first()

            if chapter:
                self.logger.info(f"Retrieved chapter: {chapter.title} (Slug: {slug})")

            return chapter

        except Exception as e:
            self.logger.error(f"Error retrieving chapter with slug {slug}: {str(e)}")
            raise

    async def get_chapters_by_module(
        self,
        db_session: AsyncSession,
        module_id: uuid.UUID
    ) -> List[Chapter]:
        """
        Get all chapters for a specific module
        """
        try:
            result = await db_session.execute(
                select(Chapter)
                .where(Chapter.module_id == module_id)
                .order_by(Chapter.chapter_number)
            )
            chapters = result.scalars().all()

            self.logger.info(f"Retrieved {len(chapters)} chapters for module {module_id}")

            return chapters

        except Exception as e:
            self.logger.error(f"Error retrieving chapters for module {module_id}: {str(e)}")
            raise

    async def get_all_chapters(
        self,
        db_session: AsyncSession
    ) -> List[Chapter]:
        """
        Get all chapters
        """
        try:
            result = await db_session.execute(
                select(Chapter)
                .order_by(Chapter.module_id, Chapter.chapter_number)
            )
            chapters = result.scalars().all()

            self.logger.info(f"Retrieved {len(chapters)} chapters")

            return chapters

        except Exception as e:
            self.logger.error(f"Error retrieving all chapters: {str(e)}")
            raise

    async def update_chapter(
        self,
        db_session: AsyncSession,
        chapter_id: uuid.UUID,
        **kwargs
    ) -> Optional[Chapter]:
        """
        Update a chapter
        """
        try:
            result = await db_session.execute(
                select(Chapter)
                .where(Chapter.id == chapter_id)
            )
            chapter = result.scalars().first()

            if not chapter:
                return None

            # Update fields that are provided
            for field, value in kwargs.items():
                if hasattr(chapter, field) and field not in ['id', 'created_at', 'module_id']:
                    setattr(chapter, field, value)

            await db_session.commit()
            await db_session.refresh(chapter)

            self.logger.info(f"Updated chapter: {chapter.title} (ID: {chapter.id})")
            log_user_action(
                logger=self.logger,
                user_id="system",  # This would be a real user ID in actual implementation
                action="update_chapter",
                details={"chapter_id": str(chapter.id), "chapter_title": chapter.title}
            )

            return chapter

        except Exception as e:
            self.logger.error(f"Error updating chapter {chapter_id}: {str(e)}")
            await db_session.rollback()
            raise

    async def delete_chapter(
        self,
        db_session: AsyncSession,
        chapter_id: uuid.UUID
    ) -> bool:
        """
        Delete a chapter
        """
        try:
            result = await db_session.execute(
                select(Chapter)
                .where(Chapter.id == chapter_id)
            )
            chapter = result.scalars().first()

            if not chapter:
                return False

            await db_session.delete(chapter)
            await db_session.commit()

            self.logger.info(f"Deleted chapter: {chapter.title} (ID: {chapter.id})")
            log_user_action(
                logger=self.logger,
                user_id="system",  # This would be a real user ID in actual implementation
                action="delete_chapter",
                details={"chapter_id": str(chapter.id), "chapter_title": chapter.title}
            )

            return True

        except Exception as e:
            self.logger.error(f"Error deleting chapter {chapter_id}: {str(e)}")
            await db_session.rollback()
            raise

    async def get_chapter_with_content(
        self,
        db_session: AsyncSession,
        chapter_id: uuid.UUID
    ) -> Optional[Dict[str, Any]]:
        """
        Get a chapter with its full content and related information
        """
        try:
            result = await db_session.execute(
                select(Chapter)
                .options(selectinload(Chapter.module))
                .where(Chapter.id == chapter_id)
            )
            chapter = result.scalars().first()

            if chapter:
                # Convert to dict format for API response
                chapter_data = {
                    "id": str(chapter.id),
                    "title": chapter.title,
                    "content": chapter.content,  # This would typically be processed for security
                    "module_id": str(chapter.module_id),
                    "chapter_number": chapter.chapter_number,
                    "slug": chapter.slug,
                    "learning_objectives": chapter.learning_objectives,
                    "exercises": chapter.exercises,
                    "created_at": chapter.created_at.isoformat(),
                    "updated_at": chapter.updated_at.isoformat() if chapter.updated_at else None,
                    "module": {
                        "id": str(chapter.module.id),
                        "title": chapter.module.title,
                        "module_number": chapter.module.module_number,
                        "programming_language": chapter.module.programming_language
                    }
                }

                return chapter_data

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving chapter with content {chapter_id}: {str(e)}")
            raise


# Global instance of the service
chapter_service = ChapterService()