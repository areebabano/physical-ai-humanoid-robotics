"""
API router for textbook content endpoints
Implements the GET /api/textbook/modules and related endpoints for User Story 1
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_db_session
from backend.src.services.textbook_module_service import textbook_module_service
from backend.src.services.chapter_service import chapter_service
from backend.src.models.textbook_module_db import TextbookModule
from backend.src.models.chapter_db import Chapter
from backend.src.utils.logging_config import get_logger, log_api_request

router = APIRouter()
logger = get_logger(__name__)


@router.get("/modules",
            summary="Get all textbook modules",
            description="Retrieve a list of all textbook modules with basic information")
async def get_textbook_modules(
    db_session: AsyncSession = Depends(get_db_session)
) -> List[dict]:
    """
    Get all textbook modules
    """
    try:
        modules = await textbook_module_service.get_all_modules(db_session)

        # Convert modules to response format
        response_modules = []
        for module in modules:
            response_modules.append({
                "id": str(module.id),
                "title": module.title,
                "description": module.description,
                "module_number": module.module_number,
                "weeks_duration": module.weeks_duration,
                "programming_language": module.programming_language,
                "created_at": module.created_at.isoformat(),
                "updated_at": module.updated_at.isoformat() if module.updated_at else None
            })

        log_api_request(
            logger=logger,
            method="GET",
            path="/api/textbook/modules",
            status_code=200,
            response_time=0.0,  # This would be calculated in a real implementation
            user_id="anonymous"  # This would be the actual user ID
        )

        return response_modules

    except Exception as e:
        logger.error(f"Error retrieving textbook modules: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving textbook modules"
        )


@router.get("/modules/{module_id}",
            summary="Get a specific textbook module",
            description="Retrieve detailed information about a specific textbook module")
async def get_textbook_module(
    module_id: str,
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Get a specific textbook module by ID
    """
    try:
        # Validate UUID format
        try:
            uuid_obj = uuid.UUID(module_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid module ID format"
            )

        module_data = await textbook_module_service.get_module_with_chapters(db_session, uuid_obj)

        if not module_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Module not found"
            )

        log_api_request(
            logger=logger,
            method="GET",
            path=f"/api/textbook/modules/{module_id}",
            status_code=200,
            response_time=0.0,  # This would be calculated in a real implementation
            user_id="anonymous"  # This would be the actual user ID
        )

        return module_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving textbook module {module_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving textbook module"
        )


@router.get("/modules/{module_id}/chapters",
            summary="Get chapters for a specific module",
            description="Retrieve all chapters belonging to a specific textbook module")
async def get_module_chapters(
    module_id: str,
    db_session: AsyncSession = Depends(get_db_session)
) -> List[dict]:
    """
    Get all chapters for a specific module
    """
    try:
        # Validate UUID format
        try:
            uuid_obj = uuid.UUID(module_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid module ID format"
            )

        chapters = await textbook_module_service.get_module_with_chapters(db_session, uuid_obj)

        if not chapters:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Module not found"
            )

        # Return just the chapters from the response
        response_chapters = chapters.get("chapters", [])

        log_api_request(
            logger=logger,
            method="GET",
            path=f"/api/textbook/modules/{module_id}/chapters",
            status_code=200,
            response_time=0.0,  # This would be calculated in a real implementation
            user_id="anonymous"  # This would be the actual user ID
        )

        return response_chapters

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving chapters for module {module_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving chapters for module"
        )


@router.get("/chapters/{chapter_id}",
            summary="Get a specific chapter",
            description="Retrieve detailed information about a specific chapter including its content")
async def get_chapter(
    chapter_id: str,
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Get a specific chapter by ID
    """
    try:
        # Validate UUID format
        try:
            uuid_obj = uuid.UUID(chapter_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid chapter ID format"
            )

        chapter_data = await chapter_service.get_chapter_with_content(db_session, uuid_obj)

        if not chapter_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )

        log_api_request(
            logger=logger,
            method="GET",
            path=f"/api/textbook/chapters/{chapter_id}",
            status_code=200,
            response_time=0.0,  # This would be calculated in a real implementation
            user_id="anonymous"  # This would be the actual user ID
        )

        return chapter_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving chapter {chapter_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving chapter"
        )


@router.get("/chapters/slug/{slug}",
            summary="Get a chapter by slug",
            description="Retrieve a chapter by its URL-friendly slug")
async def get_chapter_by_slug(
    slug: str,
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Get a chapter by its slug
    """
    try:
        chapter = await chapter_service.get_chapter_by_slug(db_session, slug)

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )

        # Convert to response format
        chapter_data = {
            "id": str(chapter.id),
            "title": chapter.title,
            "content": chapter.content,
            "module_id": str(chapter.module_id),
            "chapter_number": chapter.chapter_number,
            "slug": chapter.slug,
            "learning_objectives": chapter.learning_objectives,
            "exercises": chapter.exercises,
            "created_at": chapter.created_at.isoformat(),
            "updated_at": chapter.updated_at.isoformat() if chapter.updated_at else None
        }

        log_api_request(
            logger=logger,
            method="GET",
            path=f"/api/textbook/chapters/slug/{slug}",
            status_code=200,
            response_time=0.0,  # This would be calculated in a real implementation
            user_id="anonymous"  # This would be the actual user ID
        )

        return chapter_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving chapter with slug {slug}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving chapter"
        )


# Additional endpoints for managing content could be added here in the future
# For example: POST, PUT, DELETE endpoints for admin users