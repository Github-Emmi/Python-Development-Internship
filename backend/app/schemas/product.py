from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.common import PyObjectId

class ProductBase(BaseModel):
    """Base schema for product data shared across create and update operations."""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str

class ProductCreate(ProductBase):
    """Schema for creating a new product, inherits from ProductBase."""
    pass

class ProductUpdate(BaseModel):
    """Schema for updating an existing product. All fields are optional."""
    name: Optional[str] = None      # New name for the product
    price: Optional[float] = None    # New price (must be positive if provided)
    category: Optional[str] = None  # New category for the product

class ProductResponse(ProductBase):
    """Schema for returning product data, includes the database ID."""
    id: PyObjectId = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True)