from __future__ import annotations

from databases import Database

from app.common.serializers import serialize_from_db
from app.core.exceptions import LogicError
from app.roles.dto import Role
from app.roles.tables import roles


async def get_role_by_id(*, db: Database, role_id: int) -> Role:
    query = roles.select().filter_by(id=role_id)
    row = await db.fetch_one(query)

    if not row:
        raise LogicError("Role not found")

    return serialize_from_db(row=row, model=Role)
