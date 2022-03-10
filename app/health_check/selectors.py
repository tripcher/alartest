from __future__ import annotations

from app.common.serializers import serialize_rows_from_db
from app.core.db import database
from app.health_check.dto import HealthCheck
from app.health_check.tables import checks


async def all_checks() -> list[HealthCheck]:
    query = checks.select()
    rows = await database.fetch_all(query)
    return serialize_rows_from_db(rows=rows, model=HealthCheck)
