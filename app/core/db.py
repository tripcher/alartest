from __future__ import annotations

import databases
import sqlalchemy

from app.core.config import settings

database = databases.Database(settings.DATABASE_URI)

engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)

metadata = sqlalchemy.MetaData()
