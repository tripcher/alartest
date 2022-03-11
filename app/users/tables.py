from __future__ import annotations

import sqlalchemy

from app.core.db import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("role_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'), nullable=True),
)
