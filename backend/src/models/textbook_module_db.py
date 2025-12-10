from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class TextbookModule(Base):
    """
    TextbookModule model representing a module in the textbook
    """
    __tablename__ = "textbook_modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    module_number = Column(Integer, nullable=False, unique=True, index=True)
    weeks_duration = Column(Integer, nullable=False)
    programming_language = Column(String(50), nullable=False, default="Python")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to chapters
    chapters = relationship("Chapter", back_populates="module", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TextbookModule(id={self.id}, title={self.title}, module_number={self.module_number})>"