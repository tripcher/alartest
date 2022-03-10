from __future__ import annotations

from app.common.dto import BaseDto


class HealthCheck(BaseDto):
    id: int
    title: str
