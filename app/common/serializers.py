from __future__ import annotations

from typing import Any, Iterable, Type, TypeVar

from app.common.dto import BaseDto

T = TypeVar("T", bound=BaseDto)


def serialize_from_db(*, row: dict[str, Any], model: Type[T]) -> T:
    return model.parse_obj(row)


def serialize_rows_from_db(
    *, rows: Iterable[dict[str, Any]], model: Type[T]
) -> list[T]:
    return [serialize_from_db(row=row, model=model) for row in rows]
