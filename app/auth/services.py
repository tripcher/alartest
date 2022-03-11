from __future__ import annotations

from databases import Database
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.dto import LoginData
from app.core.db import get_database
from app.core.exceptions import AuthorizationError, PermissionDeniedError
from app.roles.selectors import permissions_on_resource_by_role
from app.users.dto import User
from app.users.selectors import find_user_by_username
from app.roles.enums import ResourcesEnum, PermissionTypeEnum

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


async def check_permissions_on_resource_by_user(
    *, db: Database, user: User, permissions: list[PermissionTypeEnum], resource: ResourcesEnum
) -> None:
    role_id = user.role_id

    if not role_id:
        raise PermissionDeniedError()

    user_permissions = await permissions_on_resource_by_role(
        db=db,
        role_id=role_id,
        resource=resource
    )

    required_permissions = [item.value for item in permissions]

    if not set(required_permissions).issubset(set(user_permissions)):
        raise PermissionDeniedError()


async def get_current_user(
    db: Database = Depends(get_database), token: str = Depends(oauth2_scheme)
) -> User:
    username = fake_decode_token(token=token)
    user = await find_user_by_username(db=db, username=username)

    if not user:
        raise AuthorizationError()

    return user


def api_check_permissions_on_resource(*, permissions: list[PermissionTypeEnum], resource: ResourcesEnum):
    async def _api_check_permissions_on_resource(
            current_user: User = Depends(get_current_user), db: Database = Depends(get_database)
    ):
        await check_permissions_on_resource_by_user(
            db=db,
            user=current_user,
            permissions=permissions,
            resource=resource
        )
        return current_user
    return _api_check_permissions_on_resource
