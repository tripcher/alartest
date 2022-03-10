from __future__ import annotations

import sqlalchemy

from app.core.db import metadata

checks = sqlalchemy.Table(
    "checks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
)
