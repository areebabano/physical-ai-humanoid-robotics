from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class Chapter(Base):
    """
    Chapter model representing a chapter in a textbook module
    """
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  # This will store the chapter content in markdown format
    module_id = Column(UUID(as_uuid=True), ForeignKey("textbook_modules.id"), nullable=False, index=True)
    chapter_number = Column(Integer, nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)  # URL-friendly identifier
    learning_objectives = Column(Text, nullable=True)  # JSON string of learning objectives
    exercises = Column(Text, nullable=True)  # JSON string of exercise IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to module
    module = relationship("TextbookModule", back_populates="chapters")

    def __repr__(self):
        return f"<Chapter(id={self.id}, title={self.title}, chapter_number={self.chapter_number})>"