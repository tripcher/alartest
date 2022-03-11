from __future__ import annotations

import pytest

from app.users.dto import User
from app.users.selectors import find_user_by_username
from app.users.tables import users


@pytest.mark.anyio
async def test__find_user_by_username__empty(db):

    result = await find_user_by_username(db=db, username="test")

    assert result is None


@pytest.mark.anyio
async def test__find_user_by_username__check_fields(db):
    username = "test"
    query = users.insert().values(username=username, password="test")
    record_id = await db.execute(query)
    expected_result = User(id=record_id, username=username, password="test")
    query = users.insert().values(username="another_username", password="test")
    await db.execute(query)

    result = await find_user_by_username(db=db, username=username)

    assert result == expected_result


@pytest.mark.anyio
async def test__find_user_by_username__check_search(db):
    username = "test"
    query = users.insert().values(username="another_username", password="test")
    await db.execute(query)

    result = await find_user_by_username(db=db, username=username)

    assert result is None
