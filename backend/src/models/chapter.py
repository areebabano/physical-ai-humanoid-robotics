from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
import uuid


class Chapter(BaseModel):
    """
    Chapter model representing an individual content section within a module
    """
    id: str = str(uuid.uuid4())
    title: str
    content: str
    module_id: str  # foreign key to TextbookModule
    chapter_number: int  # required within module
    slug: str  # unique, auto-generated from title
    learning_objectives: Optional[List[str]] = []
    exercises: Optional[dict] = {}  # exercise data
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    @validator('title')
    def validate_title_length(cls, v):
        if len(v) < 5 or len(v) > 100:
            raise ValueError('Title must be between 5 and 100 characters')
        return v

    @validator('content')
    def validate_content_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Content must not be empty')
        return v

    @validator('chapter_number')
    def validate_chapter_number_positive(cls, v):
        if v < 1:
            raise ValueError('Chapter number must be positive')
        return v