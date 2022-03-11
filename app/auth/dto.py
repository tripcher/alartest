from __future__ import annotations

from app.common.dto import BaseDto


class LoginData(BaseDto):
    username: str
    password: str


class LoginResponse(BaseDto):
    access_token: str
    token_type: str
