from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Translation(Base):
    """
    Translation model for storing translated content
    """
    __tablename__ = "translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_content_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Could reference chapters, exercises, etc.
    content_type = Column(SQLEnum("chapter", "exercise", "module", "other", name="content_type_enum"), nullable=False)
    language_code = Column(String(10), nullable=False, index=True)  # e.g., "en", "ur"
    translated_content = Column(Text, nullable=False)
    approved = Column(String, nullable=False, default="pending")  # enum: pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Translation(id={self.id}, content_type={self.content_type}, language_code={self.language_code})>"