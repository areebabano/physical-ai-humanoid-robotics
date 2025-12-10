from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class UserProgress(Base):
    """
    UserProgress model tracking a user's progress through chapters and exercises
    """
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False, index=True)
    completed = Column(String, nullable=False, default="not_started")  # enum: not_started, in_progress, completed
    score = Column(Float, nullable=True)  # Score for exercises (0.0 to 100.0)
    attempts = Column(Integer, nullable=False, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserProgress(id={self.id}, user_id={self.user_id}, chapter_id={self.chapter_id}, completed={self.completed})>"