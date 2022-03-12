from __future__ import annotations

from fastapi import APIRouter

from app.sharding.enums import ShardEnum
from app.sharding.selectors import (select_data_from_all_shards,
                                    select_data_from_shard_file)

router = APIRouter()


@router.get("/shards/{shard_name}", response_model=list[dict], status_code=200)
async def fetch_data_from_shard(shard_name: ShardEnum) -> list[dict]:
    return await select_data_from_shard_file(shard_name=shard_name)


@router.get("/shards", response_model=list[dict], status_code=200)
async def fetch_data_from_all_shards() -> list[dict]:
    return await select_data_from_all_shards()
