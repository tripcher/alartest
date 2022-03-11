from __future__ import annotations

from app.common.dto import BaseDto


class User(BaseDto):
    id: int
    username: str
    password: str
