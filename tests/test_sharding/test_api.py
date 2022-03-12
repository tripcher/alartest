from __future__ import annotations

import pytest

from app.sharding.enums import ShardEnum


@pytest.mark.parametrize("shard_name", ShardEnum)
@pytest.mark.anyio
async def test__fetch_data_from_shard__smoke(async_client, shard_name):
    async with async_client as ac:
        response = await ac.get(f"/shards/{shard_name.value}")
    assert response.status_code == 200


@pytest.mark.anyio
async def test__fetch_data_from_all_shards__smoke(async_client):
    """
    Не хорошо так делать, так как тест ходит в сеть.
    Но тест написан ради теста + запросы идут на тот же сервис.
    """
    async with async_client as ac:
        response = await ac.get("/shards")
    assert response.status_code == 200
