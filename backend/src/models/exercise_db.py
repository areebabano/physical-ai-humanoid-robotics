from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Exercise(Base):
    """
    Exercise model representing an exercise in a chapter
    """
    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False, index=True)
    type = Column(SQLEnum("coding", "mcq", "diagram", "written", name="exercise_type_enum"), nullable=False)
    question = Column(Text, nullable=False)
    solution = Column(Text, nullable=True)
    options = Column(Text, nullable=True)  # JSON string for multiple choice options
    difficulty = Column(SQLEnum("easy", "medium", "hard", name="difficulty_enum"), nullable=False, default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Exercise(id={self.id}, type={self.type}, chapter_id={self.chapter_id})>"