"""
Role-based access control dependencies
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import jwt, JWTError
from app.core.config import settings
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: JWT token from Authorization header
        db: MongoDB database connection
    
    Returns:
        User document from database
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    try:
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token"
        )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def require_admin(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency to require admin role
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        User if admin, raises HTTPException otherwise
    
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.get("role") != "admin" and not current_user.get("is_superuser"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can perform this action"
        )
    return current_user


async def require_user(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency to require authenticated user (any role)
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        User regardless of role
    """
    return current_user
