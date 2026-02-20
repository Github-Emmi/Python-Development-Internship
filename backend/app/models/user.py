from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.models.common import PyObjectId

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    role: str = Field(default="user")  # "user" or "admin"
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True