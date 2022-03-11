from __future__ import annotations

from databases import Database
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.dto import LoginData
from app.core.db import get_database
from app.core.exceptions import AuthorizationError
from app.users.dto import User
from app.users.selectors import find_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def fake_hash_password(*, password: str) -> str:
    return "fakehashed" + password


def fake_code_token_for_user(*, user: User) -> str:
    return "faketoken" + user.username


def fake_decode_token(*, token: str) -> str:
    decoded_username = token.replace("faketoken", "")

    if decoded_username == token:
        raise AuthorizationError()

    return decoded_username


async def auth_login(*, db: Database, login_data: LoginData) -> str:
    user = await find_user_by_username(db=db, username=login_data.username)

    if not user:
        raise AuthorizationError()

    hashed_password = fake_hash_password(password=login_data.password)

    if hashed_password != user.password:
        raise AuthorizationError()

    token = fake_code_token_for_user(user=user)
    return token


async def get_current_user(
    db: Database = Depends(get_database), token: str = Depends(oauth2_scheme)
) -> User:
    username = fake_decode_token(token=token)
    user = await find_user_by_username(db=db, username=username)

    if not user:
        raise AuthorizationError()

    return user
