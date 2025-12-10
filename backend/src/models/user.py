from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
import uuid


class User(BaseModel):
    """
    User model representing a student or researcher accessing the textbook
    """
    id: str = str(uuid.uuid4())
    email: EmailStr
    name: str
    software_background: str  # enum: beginner, intermediate, advanced
    hardware_background: str  # enum: beginner, intermediate, advanced
    preferred_language: str = "en"  # default: "en", options: ["en", "ur"]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    personalization_settings: Optional[dict] = {}

    @validator('software_background', 'hardware_background')
    def validate_background_level(cls, v):
        if v not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError('Background level must be beginner, intermediate, or advanced')
        return v

    @validator('preferred_language')
    def validate_preferred_language(cls, v):
        if v not in ['en', 'ur']:
            raise ValueError('Language must be en or ur')
        return v

    @validator('name')
    def validate_name_length(cls, v):
        if len(v) < 2 or len(v) > 50:
            raise ValueError('Name must be between 2 and 50 characters')
        return v