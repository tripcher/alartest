from __future__ import annotations

from app.common.dto import BaseDto


class Role(BaseDto):
    id: int
    title: str
