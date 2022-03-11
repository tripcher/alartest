from __future__ import annotations

from unittest import mock

import pytest
from databases import Database

from app.auth.services import (fake_code_token_for_user, fake_decode_token,
                               fake_hash_password, get_current_user)
from app.core.exceptions import AuthorizationError
from app.users.dto import User


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
