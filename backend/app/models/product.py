"""
Product Model for MongoDB
Represents how products are stored in the database
"""
from pydantic import BaseModel, Field
from typing import Optional
from app.models.common import PyObjectId


class ProductModel(BaseModel):
    """MongoDB Product model with BSON ObjectId mapping."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    price: float
    category: str

    class Config:
        populate_by_name = True
