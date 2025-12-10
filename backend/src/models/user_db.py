from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
from datetime import datetime

Base = declarative_base()


class User(Base):
    """
    User model representing a student or researcher accessing the textbook
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    software_background = Column(SQLEnum("beginner", "intermediate", "advanced", name="software_background_enum"), nullable=False, default="beginner")
    hardware_background = Column(SQLEnum("beginner", "intermediate", "advanced", name="hardware_background_enum"), nullable=False, default="beginner")
    preferred_language = Column(SQLEnum("en", "ur", name="language_enum"), nullable=False, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    personalization_settings = Column(JSON, nullable=False, default=dict)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"