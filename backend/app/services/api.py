from fastapi import APIRouter
from app.services import auth, items

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(items.router, prefix="/products", tags=["products"])