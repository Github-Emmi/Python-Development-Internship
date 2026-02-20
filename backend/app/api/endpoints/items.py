"""
Products/Items Endpoints
Routes for CRUD operations on products with Redis caching for GET requests
Role-based access control: DELETE and PUT require admin role
"""
import json
import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Query
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService
from app.db.mongodb import get_database
from app.db.redis import get_redis
from app.core.dependencies import require_admin, require_user
from motor.motor_asyncio import AsyncIOMotorDatabase
import redis.asyncio as redis

logger = logging.getLogger(__name__)

router = APIRouter()

CACHE_EXPIRATION = 300  # 5 minutes


async def get_product_service(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ProductService:
    """Dependency to get ProductService instance."""
    return ProductService(db)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    service: ProductService = Depends(get_product_service),
    redis_client: redis.Redis = Depends(get_redis),
    current_user: dict = Depends(require_user),
):
    """
    Create a new product.
    Requires authentication.
    
    Args:
        product_in: ProductCreate schema with name, price, category
        service: ProductService dependency
        redis_client: Redis connection for cache invalidation
        current_user: Current authenticated user
    
    Returns:
        ProductResponse with created product details and id
    """
    try:
        product = await service.create_product(product_in)
        
        # Invalidate the products list cache
        await redis_client.delete("products_list")
        logger.info(f"Product created by {current_user['email']}: {product['_id']}")
        
        return product
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )
    finally:
        await redis_client.close()


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
    redis_client: redis.Redis = Depends(get_redis),
    current_user: dict = Depends(require_user),
):
    """
    List all products with Redis caching.
    Requires authentication.
    
    First checks Redis cache. If not found, fetches from MongoDB and caches the result.
    
    Args:
        skip: Number of products to skip for pagination
        limit: Maximum number of products to return
        service: ProductService dependency
        redis_client: Redis connection for caching
        current_user: Current authenticated user
    
    Returns:
        List of ProductResponse objects
    """
    cache_key = f"products_list:skip:{skip}:limit:{limit}"
    
    try:
        # Try to get from cache
        cached_data = await redis_client.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for {cache_key}")
            products = json.loads(cached_data)
            return products
        
        # Cache miss - fetch from MongoDB
        logger.info(f"Cache miss for {cache_key} - fetching from MongoDB")
        products = await service.get_products(skip=skip, limit=limit)
        
        # Convert ObjectId to string for JSON serialization
        products_serialized = [
            {**p, "_id": str(p["_id"])} for p in products
        ]
        
        # Store in cache with expiration
        await redis_client.setex(
            cache_key,
            CACHE_EXPIRATION,
            json.dumps(products_serialized, default=str)
        )
        
        return products_serialized
    except Exception as e:
        logger.error(f"Error listing products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch products"
        )
    finally:
        await redis_client.close()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(require_user),
):
    """
    Get a specific product by ID.
    Requires authentication.
    
    Args:
        product_id: MongoDB ObjectId of the product
        service: ProductService dependency
        current_user: Current authenticated user
    
    Returns:
        ProductResponse with product details
    
    Raises:
        HTTPException: If product not found
    """
    try:
        product = await service.get_product(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch product"
        )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_in: ProductUpdate,
    service: ProductService = Depends(get_product_service),
    redis_client: redis.Redis = Depends(get_redis),
    current_user: dict = Depends(require_admin),
):
    """
    Update a product by ID.
    **Admin only**
    
    Args:
        product_id: MongoDB ObjectId of the product
        product_in: ProductUpdate schema with fields to update
        service: ProductService dependency
        redis_client: Redis connection for cache invalidation
        current_user: Current authenticated user (admin role required)
    
    Returns:
        Updated ProductResponse
    
    Raises:
        HTTPException: If product not found or user is not admin
    """
    try:
        product = await service.update_product(product_id, product_in)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
        # Invalidate related caches
        await redis_client.delete("products_list")
        logger.info(f"Product {product_id} updated by admin {current_user['email']}")
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )
    finally:
        await redis_client.close()


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    redis_client: redis.Redis = Depends(get_redis),
    current_user: dict = Depends(require_admin),
):
    """
    Delete a product by ID.
    **Admin only**
    
    Args:
        product_id: MongoDB ObjectId of the product
        service: ProductService dependency
        redis_client: Redis connection for cache invalidation
        current_user: Current authenticated user (admin role required)
    
    Raises:
        HTTPException: If product not found or user is not admin
    """
    try:
        success = await service.delete_product(product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
        # Invalidate related caches
        await redis_client.delete("products_list")
        logger.info(f"Product {product_id} deleted by admin {current_user['email']}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product"
        )
    finally:
        await redis_client.close()
