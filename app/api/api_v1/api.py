from __future__ import annotations

from fastapi import APIRouter

from app.auth.api import router as auth_router
from app.health_check.api import router as health_chek_router
from app.users.api import router as users_router

api_router = APIRouter()
api_router.include_router(health_chek_router, tags=["health_check"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(users_router, tags=["users"])
