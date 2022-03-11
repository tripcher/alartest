from __future__ import annotations

from databases import Database

from app.common.serializers import serialize_from_db, serialize_rows_from_db
from app.users.dto import User, UserDetail, UserShort
from app.users.tables import users


async def find_user_by_username(*, db: Database, username: str) -> User | None:
    query = users.select().filter_by(username=username)
    row = await db.fetch_one(query)

    if row:
        return serialize_from_db(row=row, model=User)


async def all_users_for_list_display(*, db: Database) -> list[UserShort]:
    query = users.select()
    rows = await db.fetch_all(query)
    return serialize_rows_from_db(rows=rows, model=UserShort)


async def find_user_detail_by_id(*, db: Database, user_id: int) -> UserDetail | None:
    query = users.select().filter_by(id=user_id)
    row = await db.fetch_one(query)

    if row:
        return serialize_from_db(row=row, model=UserDetail)
