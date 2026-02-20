from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.common import PyObjectId

class ProductService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["products"]

    async def create_product(self, product_in: ProductCreate) -> dict:
        product_data = product_in.model_dump()
        result = await self.collection.insert_one(product_data)
        product_data["_id"] = result.inserted_id
        return product_data

    async def get_products(self, skip: int = 0, limit: int = 10) -> List[dict]:
        cursor = self.collection.find().skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        return products

    async def get_product(self, product_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(product_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(product_id)})

    async def update_product(self, product_id: str, product_in: ProductUpdate) -> Optional[dict]:
        if not ObjectId.is_valid(product_id):
            return None
        
        update_data = product_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_product(product_id)
            
        await self.collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )
        return await self.get_product(product_id)

    async def delete_product(self, product_id: str) -> bool:
        if not ObjectId.is_valid(product_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0