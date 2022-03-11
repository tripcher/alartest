from __future__ import annotations

from databases import Database

from app.users.dto import CreateUserData, UserDetail, UpdateUserData
from app.users.tables import users
from app.auth.services import fake_hash_password


async def create_user(*, db: Database, data: CreateUserData) -> UserDetail:
    hashed_password = fake_hash_password(password=data.password)
    query = users.insert().values(
        username=data.username,
        password=hashed_password
    )

    user_id = await db.execute(query)

    return UserDetail(
        id=user_id,
        username=data.username,
        role_id=data.role_id
    )


async def update_user(*, db: Database, user_id: int, data: UpdateUserData) -> UserDetail:
    hashed_password = fake_hash_password(password=data.password)
    query = users.update().filter_by(id=user_id).values(
        username=data.username,
        password=hashed_password
    )

    await db.execute(query)

    return UserDetail(
        id=user_id,
        username=data.username,
        role_id=data.role_id
    )


async def delete_user_by_id(*, db: Database, user_id: int) -> None:
    query = users.delete().filter_by(id=user_id)
    await db.execute(query)
