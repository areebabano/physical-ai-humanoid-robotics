from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from typing import Optional
from ..database.database import get_db
from ..models.user import User, UserCreate, UserLogin, Token, UserPublic
from ..services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

security = HTTPBearer()


@router.post("/register", response_model=UserPublic)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = create_user(db, user)
        # Convert SQLModel object to Pydantic model for response
        return UserPublic(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            created_at=db_user.created_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: UserPublic = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserPublic)
async def update_user_profile(
    user_update: dict,
    current_user: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    statement = select(User).where(User.id == current_user.id)
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update allowed fields
    if "name" in user_update:
        db_user.name = user_update["name"]

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Convert SQLModel object to Pydantic model for response
    return UserPublic(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        is_active=db_user.is_active,
        is_verified=db_user.is_verified,
        created_at=db_user.created_at.isoformat()
    )