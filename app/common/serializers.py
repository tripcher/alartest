from __future__ import annotations

from typing import Iterable, Mapping, Type, TypeVar

from app.common.dto import BaseDto

T = TypeVar("T", bound=BaseDto)


def serialize_from_db(*, row: Mapping, model: Type[T]) -> T:
    return model.parse_obj(row)


def serialize_rows_from_db(*, rows: Iterable[Mapping], model: Type[T]) -> list[T]:
    return [serialize_from_db(row=row, model=model) for row in rows]
