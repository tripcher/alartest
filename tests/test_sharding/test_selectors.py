from __future__ import annotations

import asyncio

import pytest

from app.sharding.selectors import aggregate_all_data


async def selectors_sleep() -> list[dict]:
    await asyncio.sleep(0.5)
    print("selectors_sleep")
    await asyncio.sleep(3)
    return [{"id": 1, "title": "title 1"}]


async def selectors_error() -> list[dict]:
    await asyncio.sleep(0.3)
    print("selectors_error")
    raise RuntimeError("Selector")


async def selectors_success_1() -> list[dict]:
    print("selectors_success")
    return [
        {"id": 8, "title": "title 8"},
        {"id": 4, "title": "title 4"},
        {"id": 10, "title": "title 10"},
    ]


async def selectors_success_2() -> list[dict]:
    print("selectors_success")
    await asyncio.sleep(0.4)
    return [
        {"id": 40, "title": "title 40"},
        {"id": 90, "title": "title 90"},
        {"id": 50, "title": "title 50"},
    ]


@pytest.mark.anyio
async def test__aggregate_all_data(async_client):
    selectors = [
        selectors_sleep(),
        selectors_error(),
        selectors_success_1(),
        selectors_success_2(),
    ]

    result = await aggregate_all_data(selectors=selectors)

    assert result == [
        {"id": 4, "title": "title 4"},
        {"id": 8, "title": "title 8"},
        {"id": 10, "title": "title 10"},
        {"id": 40, "title": "title 40"},
        {"id": 50, "title": "title 50"},
        {"id": 90, "title": "title 90"},
    ]
