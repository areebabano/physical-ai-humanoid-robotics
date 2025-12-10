from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
import uuid


class Exercise(BaseModel):
    """
    Exercise model representing a learning activity within a chapter
    """
    id: str = str(uuid.uuid4())
    chapter_id: str  # foreign key to Chapter
    type: str  # enum: "coding", "mcq", "diagram", "essay"
    question: str
    solution: Optional[str] = None  # required for coding/essay
    options: Optional[List[str]] = []  # for MCQ type
    difficulty: str  # enum: "beginner", "intermediate", "advanced"
    created_at: datetime = datetime.utcnow()

    @validator('type')
    def validate_exercise_type(cls, v):
        valid_types = ['coding', 'mcq', 'diagram', 'essay']
        if v not in valid_types:
            raise ValueError(f'Exercise type must be one of {valid_types}')
        return v

    @validator('difficulty')
    def validate_difficulty(cls, v):
        valid_difficulties = ['beginner', 'intermediate', 'advanced']
        if v not in valid_difficulties:
            raise ValueError(f'Difficulty must be one of {valid_difficulties}')
        return v

    @validator('question')
    def validate_question_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Question must not be empty')
        return v

    @validator('solution')
    def validate_solution_for_coding_essay(cls, v, values):
        exercise_type = values.get('type')
        if exercise_type in ['coding', 'essay'] and (not v or len(v.strip()) == 0):
            raise ValueError('Solution is required for coding and essay exercises')
        return v

    @validator('options')
    def validate_options_for_mcq(cls, v, values):
        exercise_type = values.get('type')
        if exercise_type == 'mcq' and (not v or len(v) == 0):
            raise ValueError('Options are required for MCQ exercises')
        return v