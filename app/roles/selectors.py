from __future__ import annotations

from databases import Database

from app.common.serializers import serialize_from_db
from app.core.exceptions import LogicError
from app.roles.dto import Role
from app.roles.enums import ResourcesEnum
from app.roles.tables import roles


async def get_role_by_id(*, db: Database, role_id: int) -> Role:
    query = roles.select().filter_by(id=role_id)
    row = await db.fetch_one(query)

    if not row:
        raise LogicError("Role not found")

    return serialize_from_db(row=row, model=Role)


async def permissions_on_resource_by_role(
    *, db: Database, role_id: int, resource: ResourcesEnum
) -> list[str]:
    query = """
        select p.type as permission from roles
        join permissions_in_roles pir on roles.id = pir.role_id
        join permissions p on p.id = pir.permission_id
        where roles.id = :role_id and p.resource = :resource;
        """

    role_permissions = await db.fetch_all(
        query=query,
        values={
            "role_id": role_id,
            "resource": resource.value,
        },
    )

    return [item["permission"] for item in role_permissions]
