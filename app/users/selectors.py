from __future__ import annotations

from databases import Database

from app.common.serializers import serialize_from_db
from app.users.dto import User
from app.users.tables import users


async def find_user_by_username(*, db: Database, username: str) -> User | None:
    query = users.select().filter_by(username=username)
    row = await db.fetch_one(query)

    if row:
        return serialize_from_db(row=row, model=User)
