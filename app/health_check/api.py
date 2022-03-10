from __future__ import annotations

from fastapi import APIRouter

from app.health_check.dto import HealthCheck
from app.health_check.selectors import all_checks

router = APIRouter()


@router.get("/checks", response_model=list[HealthCheck], status_code=200)
async def health_check() -> list[HealthCheck]:
    return await all_checks()
