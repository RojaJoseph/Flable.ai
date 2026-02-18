"""
Authentication utilities - JWT, password hashing, user verification
Uses Argon2 for password hashing (pure Python, always works!)
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging

from database.connection import get_db
from database.models import User
from utils.config import settings

logger = logging.getLogger(__name__)

# Password hasher - Argon2 (pure Python, no compilation needed!)
ph = PasswordHasher()

# JWT Bearer token
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash a password using Argon2"""
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its Argon2 hash"""
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    # Ensure 'sub' is a string (JWT spec requires it)
    if 'sub' in to_encode and not isinstance(to_encode['sub'], str):
        to_encode['sub'] = str(to_encode['sub'])
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.debug(f"Created access token for user_id: {data.get('sub')}")
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    
    # Ensure 'sub' is a string (JWT spec requires it)
    if 'sub' in to_encode and not isinstance(to_encode['sub'], str):
        to_encode['sub'] = str(to_encode['sub'])
    
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.debug(f"Token decoded successfully. Payload: {payload}")
        return payload
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    
    # Check if credentials exist
    if credentials is None:
        logger.warning("No credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated - No credentials provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get token
    token = credentials.credentials
    logger.debug(f"Received token: {token[:20]}...")
    
    # Decode token
    try:
        payload = decode_token(token)
    except HTTPException as e:
        logger.error(f"Token decode failed: {e.detail}")
        raise
    
    # Get user ID from payload
    user_id = payload.get("sub")
    if user_id is None:
        logger.error("No 'sub' field in token payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - Invalid token payload"
        )
    
    # Convert to int if it's a string
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        logger.error(f"Invalid user_id format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - Invalid user ID"
        )
    
    logger.debug(f"Looking up user with ID: {user_id}")
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.error(f"User not found with ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Check if user is active
    if not user.is_active:
        logger.warning(f"Inactive user attempted access: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    logger.debug(f"User authenticated successfully: {user.email}")
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_role(required_role: str):
    """Dependency to check user role"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """Authenticate user with email and password"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Login attempt for non-existent user: {email}")
        return None
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Failed password verification for user: {email}")
        return None
    
    logger.info(f"User authenticated successfully: {email}")
    return user
