from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False, index=True)
    name: Optional[str] = Field(default=None)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# Pydantic models for API
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserInDB(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    created_at: str

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    created_at: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None