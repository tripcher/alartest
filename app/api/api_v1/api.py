from __future__ import annotations

from fastapi import APIRouter

from app.health_check.api import router as health_chek_router

api_router = APIRouter()
api_router.include_router(health_chek_router, tags=["health_check"])
