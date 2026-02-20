"""
V1 API Router Aggregator
Combines all versioned endpoints into a single router
"""
from fastapi import APIRouter
from app.api.endpoints import auth, items

api_router = APIRouter()

# Include auth routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

# Include product routes
api_router.include_router(
    items.router,
    prefix="/products",
    tags=["Products"],
)
