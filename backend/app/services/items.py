import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis

from app.db.mongodb import get_database
from app.db.redis import get_redis
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter()

def get_product_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> ProductService:
    return ProductService(db)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    return await service.create_product(product)

@router.get("/", response_model=List[ProductResponse])
async def read_products(
    skip: int = 0,
    limit: int = 10,
    service: ProductService = Depends(get_product_service),
    redis_client: Redis = Depends(get_redis)
):
    # Cache Key
    cache_key = f"products:{skip}:{limit}"
    
    # Check Redis
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Fetch from DB
    products = await service.get_products(skip=skip, limit=limit)
    
    # Serialize for Redis (convert ObjectId to str for JSON serialization)
    # Note: Pydantic handles the response serialization, but for Redis we need raw JSON
    products_json = [
        {**p, "_id": str(p["_id"])} for p in products
    ]
    
    # Set Cache (TTL 300s)
    await redis_client.setex(cache_key, 300, json.dumps(products_json))
    
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Additional PUT/DELETE endpoints can be added similarly