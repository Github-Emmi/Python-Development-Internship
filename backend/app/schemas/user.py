from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.common import PyObjectId

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool