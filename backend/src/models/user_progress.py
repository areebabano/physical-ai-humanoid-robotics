from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
import uuid


class UserProgress(BaseModel):
    """
    UserProgress model representing a user's progress through textbook content
    """
    id: str = str(uuid.uuid4())
    user_id: str  # foreign key to User
    chapter_id: str  # foreign key to Chapter
    completed: bool = False
    score: Optional[int] = None  # 0-100, nullable
    attempts: int = 0  # default: 0
    completed_at: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    @validator('score')
    def validate_score_range(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Score must be between 0 and 100')
        return v

    @validator('attempts')
    def validate_attempts_non_negative(cls, v):
        if v < 0:
            raise ValueError('Attempts must be non-negative')
        return v