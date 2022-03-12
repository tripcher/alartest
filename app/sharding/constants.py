from __future__ import annotations

from app.core.config import settings
from app.sharding.enums import ShardEnum

SHARD_MAP = {
    ShardEnum.first: f"{settings.BASE_API_URL}/shards/{ShardEnum.first.value}",
    ShardEnum.second: f"{settings.BASE_API_URL}/shards/{ShardEnum.second.value}",
    ShardEnum.third: f"{settings.BASE_API_URL}/shards/{ShardEnum.third.value}",
}

TIMOUT_FOR_SHARD = 2
