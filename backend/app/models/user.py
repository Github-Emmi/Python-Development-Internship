from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.models.common import PyObjectId

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        populate_by_name = True