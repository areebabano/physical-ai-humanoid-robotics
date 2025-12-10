"""
Authentication service for the Physical AI & Humanoid Robotics Textbook
Handles user registration, login, and authentication using Better-Auth
"""
from datetime import timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging

from backend.src.models.user import User
from backend.src.utils.security import SecurityUtils, validate_password_strength
from backend.src.database import get_db_session, AsyncSession


security = HTTPBearer()
security_utils = SecurityUtils()
logger = logging.getLogger(__name__)


class AuthService:
    """
    Authentication service class for handling user authentication operations
    """

    def __init__(self):
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    async def register_user(
        self,
        email: str,
        name: str,
        password: str,
        software_background: str = "beginner",
        hardware_background: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Register a new user with validation
        """
        # Validate password strength
        is_valid, message = validate_password_strength(password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )

        # Validate email format
        if not security_utils.validate_email_format(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Validate background levels
        valid_backgrounds = ["beginner", "intermediate", "advanced"]
        if software_background not in valid_backgrounds:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Software background must be beginner, intermediate, or advanced"
            )

        if hardware_background not in valid_backgrounds:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hardware background must be beginner, intermediate, or advanced"
            )

        # Create password hash
        password_hash = security_utils.get_password_hash(password)

        # Create user instance (in a real implementation, this would be saved to the database)
        user = User(
            email=email,
            name=name,
            software_background=software_background,
            hardware_background=hardware_background,
            personalization_settings={}
        )

        # In a real implementation, we would save the user to the database here
        # For now, we'll just return user data with the password hash
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "software_background": user.software_background,
            "hardware_background": user.hardware_background,
            "preferred_language": user.preferred_language,
            "created_at": user.created_at.isoformat(),
            "password_hash": password_hash  # In real implementation, this would be stored in DB
        }

        logger.info(f"User registered: {email}")
        return user_data

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user by email and password
        """
        # In a real implementation, we would query the database for the user
        # For this example, we'll simulate finding a user and checking the password
        # This is a simplified version - in production, always use database lookups

        # Simulated user lookup (in real implementation, query database)
        # This is just for demonstration - in real app, you'd query the actual database
        simulated_user = {
            "id": "test-user-id",
            "email": email,
            "name": "Test User",
            "software_background": "intermediate",
            "hardware_background": "beginner",
            "preferred_language": "en",
            "created_at": "2025-12-07T10:00:00Z",
            "password_hash": security_utils.get_password_hash(password)  # In real app, fetch from DB
        }

        # For demo purposes, we'll return the user if email format is valid
        # In real implementation, query database and verify password
        if security_utils.validate_email_format(email):
            # In a real implementation, you would:
            # 1. Query database for user by email
            # 2. If user exists, verify password using security_utils.verify_password
            # 3. Return user data if verification succeeds
            return simulated_user

        return None

    def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """
        Create an access token for the authenticated user
        """
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        token_data = {
            "sub": user_data["email"],
            "user_id": user_data["id"],
            "name": user_data["name"]
        }
        return security_utils.create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )

    def create_refresh_token(self, user_data: Dict[str, Any]) -> str:
        """
        Create a refresh token for the authenticated user
        """
        refresh_token_expires = timedelta(days=self.refresh_token_expire_days)
        token_data = {
            "sub": user_data["email"],
            "user_id": user_data["id"],
            "type": "refresh"
        }
        return security_utils.create_access_token(
            data=token_data,
            expires_delta=refresh_token_expires
        )

    async def get_current_user(
        self,
        token: HTTPAuthorizationCredentials = Depends(security)
    ) -> Dict[str, Any]:
        """
        Get the current authenticated user from the token
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = security_utils.verify_token(token.credentials)
        if payload is None:
            raise credentials_exception

        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")

        if email is None or user_id is None:
            raise credentials_exception

        # In a real implementation, fetch user from database
        # For demo purposes, return a simulated user
        return {
            "id": user_id,
            "email": email,
            "name": payload.get("name", "Unknown User")
        }

    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login a user and return tokens
        """
        user = await self.authenticate_user(email, password)

        if not user or not security_utils.verify_password(
            password,
            user.get("password_hash", "")
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "preferred_language": user["preferred_language"]
            }
        }

    async def update_user_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user preferences and personalization settings
        """
        # In a real implementation, update user in database
        # For demo purposes, return updated preferences
        updated_preferences = {
            "user_id": user_id,
            "updated_preferences": preferences,
            "updated_at": "2025-12-07T10:00:00Z"  # In real app, use current timestamp
        }

        logger.info(f"Updated preferences for user {user_id}")
        return updated_preferences


# Singleton instance of the auth service
auth_service = AuthService()


# Dependency to get the current user
async def get_current_user():
    """
    Dependency to get the current authenticated user
    """
    return await auth_service.get_current_user()


# Helper function to get auth service instance
def get_auth_service() -> AuthService:
    """
    Get the authentication service instance
    """
    return auth_service