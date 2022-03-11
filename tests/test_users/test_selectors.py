from __future__ import annotations

import pytest

from app.users.dto import UserFullDetail
from app.users.selectors import find_user_by_username, all_users_for_list_display, find_user_detail_by_id


@pytest.mark.anyio
async def test__find_user_by_username__empty(db):

    result = await find_user_by_username(db=db, username="test")

    assert result is None


@pytest.mark.anyio
async def test__find_user_by_username__check_fields(db, user_factory):
    username = "test"
    expected_user = await user_factory(username=username, password="test")
    await user_factory(username="another_username", password="test")

    result = await find_user_by_username(db=db, username=username)

    assert result == expected_user


@pytest.mark.anyio
async def test__find_user_by_username__check_search(db, user_factory):
    username = "test"
    await user_factory(username="another_username", password="test")

    result = await find_user_by_username(db=db, username=username)

    assert result is None


@pytest.mark.anyio
async def test__all_users_for_list_display__empty(db):

    result = await all_users_for_list_display(db=db)

    assert result == []


@pytest.mark.parametrize("number_of_users", [0, 1, 3])
@pytest.mark.anyio
async def test__all_users_for_list_display__amount(db, user_factory, number_of_users):
    # лень делать нормальные фабрики с bulk
    for number in range(number_of_users):
        await user_factory(
            username=f'test_{number}'
        )

    result = await all_users_for_list_display(db=db)

    assert len(result) == number_of_users


@pytest.mark.anyio
async def test__find_user_detail_by_id__none(db):

    result = await find_user_detail_by_id(db=db, user_id=1)

    assert result is None


@pytest.mark.anyio
async def test__find_user_detail_by_id__not_none(db, user_factory):
    user = await user_factory(
        username=f'test'
    )

    result = await find_user_detail_by_id(db=db, user_id=user.id)

    assert result == UserFullDetail(
        id=user.id,
        username=user.username,
        role_id=None,
        role_title=None,
    )


@pytest.mark.anyio
async def test__find_user_detail_by_id__with_role(db, user_factory, role_factory):
    role = await role_factory(
        title='Test Role'
    )
    user = await user_factory(
        username=f'test',
        role_id=role.id
    )

    result = await find_user_detail_by_id(db=db, user_id=user.id)

    assert result == UserFullDetail(
        id=user.id,
        username=user.username,
        role_id=role.id,
        role_title=role.title,
    )
