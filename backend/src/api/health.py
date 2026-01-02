from fastapi import APIRouter
from datetime import datetime
from ..core.logging import logger


router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    logger.info("Health check endpoint called")
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@router.get("/")
async def root():
    """
    Root endpoint
    """
    logger.info("Root endpoint called")
    return {"message": "Physical AI & Humanoid Robotics RAG Chatbot API"}