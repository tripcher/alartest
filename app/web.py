from __future__ import annotations

from fastapi import APIRouter

from app.auth.web import router as auth_router
from app.users.web import router as users_router

web_router = APIRouter()
web_router.include_router(auth_router, tags=["web_auth"])
web_router.include_router(users_router, tags=["web_users"])
