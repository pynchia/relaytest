from fastapi import APIRouter

from app.api.endpoints import earnings


api_router = APIRouter()
api_router.include_router(earnings.router, prefix="/earnings", tags=["earnings"])
