from __future__ import annotations

from typing import Optional

from app.common.dto import BaseDto


class User(BaseDto):
    id: int
    username: str
    password: str
    role_id: Optional[int] = None


class UserDetail(BaseDto):
    id: int
    username: str
    role_id: Optional[int] = None


class UserFullDetail(BaseDto):
    id: int
    username: str
    role_id: Optional[int] = None
    role_title: Optional[str] = None


class UserShort(BaseDto):
    id: int
    username: str


class CreateUserData(BaseDto):
    username: str
    password: str
    role_id: Optional[int] = None


class UpdateUserData(BaseDto):
    username: str
    role_id: Optional[int] = None
