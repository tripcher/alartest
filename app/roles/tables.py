from __future__ import annotations

import sqlalchemy

from app.core.db import metadata
from app.roles.enums import PermissionTypeEnum, ResourcesEnum

roles = sqlalchemy.Table(
    "roles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("title", sqlalchemy.String),
)

permissions = sqlalchemy.Table(
    "permissions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("type", sqlalchemy.Enum(PermissionTypeEnum)),
    sqlalchemy.Column("resource", sqlalchemy.Enum(ResourcesEnum)),
)

permissions_in_roles = sqlalchemy.Table(
    "permissions_in_roles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("role_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id")),
    sqlalchemy.Column(
        "permission_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("permissions.id")
    ),
)
