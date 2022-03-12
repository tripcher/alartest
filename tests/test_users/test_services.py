from __future__ import annotations

import pytest

from app.users.dto import CreateUserData, UpdateUserData, UserDetail
from app.users.services import create_user, delete_user_by_id, update_user
from app.users.tables import users


@pytest.mark.anyio
async def test__create_user__check_fields(db):
    data = CreateUserData(username="test_username", password="test_password")

    result = await create_user(db=db, data=data)
    user_in_db = await db.fetch_one(users.select().filter_by(id=result.id))

    assert isinstance(result, UserDetail)
    assert result.username == "test_username"
    assert result.role_id is None
    assert user_in_db["username"] == "test_username"
    assert user_in_db["password"] == "fakehashedtest_password"
    assert user_in_db["role_id"] is None


@pytest.mark.anyio
async def test__create_user__with_role(db, role_factory):
    role = await role_factory()
    data = CreateUserData(
        username="test_username", password="test_password", role_id=role.id
    )

    result = await create_user(db=db, data=data)
    user_in_db = await db.fetch_one(users.select().filter_by(id=result.id))

    assert isinstance(result, UserDetail)
    assert result.role_id == role.id
    assert user_in_db["role_id"] == role.id


@pytest.mark.anyio
async def test__update_user__check_fields(db, user_factory, role_factory):
    old_role = await role_factory()
    new_role = await role_factory()
    user = await user_factory(username="old_username", role_id=old_role.id)
    data = UpdateUserData(username="new_username", role_id=new_role.id)

    result = await update_user(db=db, user_id=user.id, data=data)
    user_in_db = await db.fetch_one(users.select().filter_by(id=user.id))

    assert isinstance(result, UserDetail)
    assert result.username == "new_username"
    assert result.role_id == new_role.id
    assert user_in_db["username"] == "new_username"
    assert user_in_db["role_id"] == new_role.id


@pytest.mark.anyio
async def test__delete_user_by_id(db, user_factory):
    user = await user_factory()

    result = await delete_user_by_id(db=db, user_id=user.id)
    user_in_db = await db.fetch_one(users.select().filter_by(id=user.id))

    assert result is None
    assert user_in_db is None
