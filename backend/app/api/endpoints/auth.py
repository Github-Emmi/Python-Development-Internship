"""
Authentication Endpoints
Routes for user registration and login
"""
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Register a new user.
    
    Args:
        user_in: UserCreate schema containing email, password, and optional full_name
        db: MongoDB database connection
    
    Returns:
        UserResponse with created user details (excluding password)
    
    Raises:
        HTTPException: If email is already registered
    """
    existing_user = await db["users"].find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user_data = {
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "full_name": user_in.full_name,
        "is_active": True,
        "is_superuser": False
    }
    
    result = await db["users"].insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return user_data


@router.post("/login")
async def login(user_in: UserLogin, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Authenticate user and return JWT access token.
    
    Args:
        user_in: UserLogin schema containing email and password
        db: MongoDB database connection
    
    Returns:
        Dictionary with access_token, token_type, and user_id
    
    Raises:
        HTTPException: If email is not found or password is incorrect
    """
    user = await db["users"].find_one({"email": user_in.email})
    if not user or not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=str(user["_id"]))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user["_id"])
    }
