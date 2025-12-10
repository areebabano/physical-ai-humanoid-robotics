"""
Security utilities for the Physical AI & Humanoid Robotics Textbook
Contains encryption, authentication, and security-related helper functions
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
import os
import logging


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get secret key from environment
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class SecurityUtils:
    """
    Security utilities for password hashing, token generation, and data protection
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hash
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate a hash for a plain password
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token and return its payload
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None

    @staticmethod
    def generate_salt() -> str:
        """
        Generate a random salt for password hashing
        """
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_data(data: str, salt: Optional[str] = None) -> str:
        """
        Hash data with optional salt for additional security
        """
        if salt is None:
            salt = SecurityUtils.generate_salt()

        # Combine data and salt
        data_to_hash = f"{data}{salt}"

        # Create SHA-256 hash
        hashed = hashlib.sha256(data_to_hash.encode()).hexdigest()

        return f"{hashed}:{salt}"

    @staticmethod
    def verify_hashed_data(data: str, hashed_data: str) -> bool:
        """
        Verify if data matches the hashed value
        """
        try:
            hash_val, salt = hashed_data.split(":")
            return SecurityUtils.hash_data(data, salt).startswith(hash_val)
        except ValueError:
            return False

    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """
        Sanitize user input to prevent injection attacks
        """
        # Remove potentially dangerous characters/sequences
        sanitized = user_input.replace("<script", "").replace("javascript:", "")
        sanitized = sanitized.replace("vbscript:", "").replace("onerror", "")
        sanitized = sanitized.replace("onload", "").replace("onclick", "")

        return sanitized.strip()

    @staticmethod
    def generate_csrf_token() -> str:
        """
        Generate a CSRF token for protecting against cross-site request forgery
        """
        return secrets.token_urlsafe(32)

    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Basic email format validation
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def encrypt_data(data: str) -> str:
        """
        Basic encryption of sensitive data (in production, use proper encryption library like cryptography)
        This is a placeholder implementation - in production use Fernet or similar
        """
        # This is a simple XOR-based "encryption" for demonstration
        # In production, use a proper encryption library like cryptography
        key = SECRET_KEY[:16]  # Use first 16 chars of secret key
        encrypted_chars = []

        for i, char in enumerate(data):
            encrypted_char = chr(ord(char) ^ ord(key[i % len(key)]))
            encrypted_chars.append(encrypted_char)

        return "".join(encrypted_chars)

    @staticmethod
    def decrypt_data(encrypted_data: str) -> str:
        """
        Basic decryption of sensitive data (in production, use proper encryption library like cryptography)
        This is a placeholder implementation - in production use Fernet or similar
        """
        # Since XOR is symmetric, we can use the same function
        return SecurityUtils.encrypt_data(encrypted_data)  # XOR is symmetric


# Initialize security logger
logger = logging.getLogger(__name__)


def get_password_hash_sync(password: str) -> str:
    """
    Synchronous version of password hashing for use in non-async contexts
    """
    return SecurityUtils.get_password_hash(password)


def verify_password_sync(plain_password: str, hashed_password: str) -> bool:
    """
    Synchronous version of password verification for use in non-async contexts
    """
    return SecurityUtils.verify_password(plain_password, hashed_password)


# Security configuration constants
SECURITY_CONFIG = {
    "MIN_PASSWORD_LENGTH": 8,
    "MAX_PASSWORD_LENGTH": 128,
    "REQUIRE_UPPERCASE": True,
    "REQUIRE_LOWERCASE": True,
    "REQUIRE_DIGITS": True,
    "REQUIRE_SPECIAL_CHARS": True,
    "MAX_LOGIN_ATTEMPTS": 5,
    "LOCKOUT_DURATION_MINUTES": 15,
    "SESSION_TIMEOUT_MINUTES": 30
}


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength based on security requirements
    Returns (is_valid, message)
    """
    if len(password) < SECURITY_CONFIG["MIN_PASSWORD_LENGTH"]:
        return False, f"Password must be at least {SECURITY_CONFIG['MIN_PASSWORD_LENGTH']} characters long"

    if len(password) > SECURITY_CONFIG["MAX_PASSWORD_LENGTH"]:
        return False, f"Password must not exceed {SECURITY_CONFIG['MAX_PASSWORD_LENGTH']} characters"

    if SECURITY_CONFIG["REQUIRE_UPPERCASE"] and not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if SECURITY_CONFIG["REQUIRE_LOWERCASE"] and not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if SECURITY_CONFIG["REQUIRE_DIGITS"] and not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"

    if SECURITY_CONFIG["REQUIRE_SPECIAL_CHARS"]:
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False, f"Password must contain at least one special character: {special_chars}"

    return True, "Password meets strength requirements"


# Singleton instance for security utilities
security_utils = SecurityUtils()