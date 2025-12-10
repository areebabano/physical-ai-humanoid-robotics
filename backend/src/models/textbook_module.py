from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
import uuid


class TextbookModule(BaseModel):
    """
    TextbookModule model representing an educational content unit covering specific robotics topics
    """
    id: str = str(uuid.uuid4())
    title: str
    description: str
    module_number: int  # required, unique
    weeks_duration: int  # required
    programming_language: str  # required
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    @validator('title')
    def validate_title_length(cls, v):
        if len(v) < 5 or len(v) > 100:
            raise ValueError('Title must be between 5 and 100 characters')
        return v

    @validator('weeks_duration')
    def validate_weeks_duration(cls, v):
        if v < 1 or v > 20:
            raise ValueError('Weeks duration must be between 1 and 20')
        return v

    @validator('programming_language')
    def validate_programming_language(cls, v):
        # Based on the spec, supported languages include Python, C#, JavaScript/TypeScript
        supported_languages = ['Python', 'C#', 'JavaScript', 'TypeScript']
        if v not in supported_languages:
            raise ValueError(f'Programming language must be one of {supported_languages}')
        return v