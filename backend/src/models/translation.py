from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
import uuid


class Translation(BaseModel):
    """
    Translation model representing language-specific version of textbook content
    """
    id: str = str(uuid.uuid4())
    original_content_id: str  # references either Chapter or Exercise
    content_type: str  # enum: "chapter", "exercise"
    language_code: str  # required, e.g., "ur", "en"
    translated_content: str  # required
    approved: bool = False  # default: false
    created_at: datetime = datetime.utcnow()

    @validator('content_type')
    def validate_content_type(cls, v):
        valid_types = ['chapter', 'exercise']
        if v not in valid_types:
            raise ValueError(f'Content type must be one of {valid_types}')
        return v

    @validator('language_code')
    def validate_language_code(cls, v):
        # Support English and Urdu as per requirements
        valid_codes = ['en', 'ur']
        if v not in valid_codes:
            raise ValueError(f'Language code must be one of {valid_codes}')
        return v

    @validator('translated_content')
    def validate_translated_content_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Translated content must not be empty')
        return v