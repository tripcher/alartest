from __future__ import annotations

from databases import Database
from fastapi import APIRouter, Depends

from app.auth.services import api_check_permissions_on_resource
from app.core.db import get_database
from app.health_check.dto import HealthCheck
from app.health_check.selectors import all_checks
from app.roles.enums import PermissionTypeEnum, ResourcesEnum

router = APIRouter()


@router.get("/checks", response_model=list[HealthCheck], status_code=200)
async def checks_list(db: Database = Depends(get_database)) -> list[HealthCheck]:
    return await all_checks(db=db)


@router.get(
    "/checks/auth",
    response_model=list[HealthCheck],
    status_code=200,
    dependencies=[
        Depends(
            api_check_permissions_on_resource(
                permissions=[PermissionTypeEnum.view], resource=ResourcesEnum.checks
            )
        )
    ],
)
async def checks_list_auth(db: Database = Depends(get_database)) -> list[HealthCheck]:
    return await all_checks(db=db)
