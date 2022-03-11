from __future__ import annotations

from databases import Database
from fastapi import APIRouter, Depends

from app.auth.services import get_current_user
from app.core.db import get_database
from app.health_check.dto import HealthCheck
from app.health_check.selectors import all_checks

router = APIRouter()


@router.get("/checks", response_model=list[HealthCheck], status_code=200)
async def checks_list(db: Database = Depends(get_database)) -> list[HealthCheck]:
    return await all_checks(db=db)


@router.get(
    "/checks/auth",
    response_model=list[HealthCheck],
    status_code=200,
    dependencies=[Depends(get_current_user)],
)
async def checks_list_auth(db: Database = Depends(get_database)) -> list[HealthCheck]:
    return await all_checks(db=db)
