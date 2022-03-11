from __future__ import annotations

from databases import Database

from app.common.serializers import serialize_rows_from_db
from app.health_check.dto import HealthCheck
from app.health_check.tables import checks


async def all_checks(*, db: Database) -> list[HealthCheck]:
    query = checks.select()
    rows = await db.fetch_all(query)
    return serialize_rows_from_db(rows=rows, model=HealthCheck)
