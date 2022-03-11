from __future__ import annotations

from unittest import mock

import pytest
from databases import Database

from app.auth.services import (fake_code_token_for_user, fake_decode_token,
                               fake_hash_password, get_current_user, check_permissions_on_resource_by_user)
from app.core.exceptions import AuthorizationError, PermissionDeniedError
from app.users.dto import User
from app.roles.enums import PermissionTypeEnum, ResourcesEnum


@pytest.mark.parametrize(
    ("password", "expected_result"),
    [
        ("", "fakehashed"),
        ("test", "fakehashedtest"),
        ("123", "fakehashed123"),
    ],
)
def test__fake_hash_password(password, expected_result):
    result = fake_hash_password(password=password)

    assert result == expected_result


@pytest.mark.parametrize(
    ("user", "expected_result"),
    [
        (User(id=1, username="", password="test"), "faketoken"),
        (User(id=1, username="test", password="test"), "faketokentest"),
        (User(id=1, username="123", password="test"), "faketoken123"),
    ],
)
def test__fake_code_token_for_user(user, expected_result):
    result = fake_code_token_for_user(user=user)

    assert result == expected_result


@pytest.mark.parametrize(
    ("token", "expected_result"),
    [
        ("faketoken", ""),
        ("faketokentest", "test"),
        ("faketoken123", "123"),
    ],
)
def test__fake_decode_token__success(token, expected_result):
    result = fake_decode_token(token=token)

    assert result == expected_result


@pytest.mark.parametrize("token", ["", "test", "faketoke1234", "tokentest"])
def test__fake_decode_token__error(token):
    with pytest.raises(AuthorizationError):
        fake_decode_token(token=token)


@pytest.mark.anyio
async def test__get_current_user__success(mocker):
    token = "faketokentest"
    username = "test"
    user = User(id=1, password="test", username=username)
    db = mock.MagicMock(spec=Database)
    mocked_fake_decode_token = mocker.patch(
        "app.auth.services.fake_decode_token", return_value=username
    )
    mocked_find_user_by_username = mocker.patch(
        "app.auth.services.find_user_by_username", return_value=user
    )

    result = await get_current_user(db=db, token=token)

    assert result == user
    mocked_fake_decode_token.assert_called_once_with(token=token)
    mocked_find_user_by_username.assert_called_once_with(db=db, username=username)


@pytest.mark.anyio
async def test__get_current_user__error(mocker):
    token = "faketokentest"
    username = "test"
    db = mock.MagicMock(spec=Database)
    mocked_fake_decode_token = mocker.patch(
        "app.auth.services.fake_decode_token", return_value=username
    )
    mocked_find_user_by_username = mocker.patch(
        "app.auth.services.find_user_by_username", return_value=None
    )

    with pytest.raises(AuthorizationError):
        await get_current_user(db=db, token=token)

    mocked_fake_decode_token.assert_called_once_with(token=token)
    mocked_find_user_by_username.assert_called_once_with(db=db, username=username)


@pytest.mark.parametrize(
    ("permissions", "resource", 'user_permissions', 'user_resource'),
    [
        ([PermissionTypeEnum.update], ResourcesEnum.users, [PermissionTypeEnum.update], ResourcesEnum.users),
        (
                [PermissionTypeEnum.update],
                ResourcesEnum.users,
                [PermissionTypeEnum.update, PermissionTypeEnum.delete, PermissionTypeEnum.view],
                ResourcesEnum.users
        ),
        (
                [PermissionTypeEnum.update, PermissionTypeEnum.delete, PermissionTypeEnum.view, PermissionTypeEnum.create],
                ResourcesEnum.users,
                [PermissionTypeEnum.update, PermissionTypeEnum.delete, PermissionTypeEnum.view, PermissionTypeEnum.create],
                ResourcesEnum.users
        )
    ],
)
@pytest.mark.anyio
async def test__check_permissions_on_resource_by_user__success(
        db,
        role_with_permissions_factory,
        permissions,
        resource,
        user_permissions,
        user_resource
):
    role = await role_with_permissions_factory(
        permission_types=user_permissions,
        resource=user_resource
    )
    user = User(
        id=1,
        username='test',
        password='test',
        role_id=role.id
    )

    result = await check_permissions_on_resource_by_user(
        db=db,
        user=user,
        permissions=permissions,
        resource=resource
    )

    assert result is None


@pytest.mark.parametrize(
    ("permissions", "resource", 'user_permissions', 'user_resource'),
    [
        ([PermissionTypeEnum.update], ResourcesEnum.users, [PermissionTypeEnum.update], ResourcesEnum.checks),
        (
                [PermissionTypeEnum.update, PermissionTypeEnum.delete, PermissionTypeEnum.view],
                ResourcesEnum.users,
                [PermissionTypeEnum.update],
                ResourcesEnum.users
        ),
        (
                [PermissionTypeEnum.view],
                ResourcesEnum.checks,
                [PermissionTypeEnum.update],
                ResourcesEnum.checks
        ),
    ],
)
@pytest.mark.anyio
async def test__check_permissions_on_resource_by_user__error(
        db,
        role_with_permissions_factory,
        permissions,
        resource,
        user_permissions,
        user_resource
):
    role = await role_with_permissions_factory(
        permission_types=user_permissions,
        resource=user_resource
    )
    user = User(
        id=1,
        username='test',
        password='test',
        role_id=role.id
    )
    with pytest.raises(PermissionDeniedError):
        await check_permissions_on_resource_by_user(
            db=db,
            user=user,
            permissions=permissions,
            resource=resource
        )
