from __future__ import annotations

import asyncio
import json
import os
from asyncio import Task
from typing import Any, AsyncGenerator, Coroutine, Iterable

from httpx import AsyncClient

from app.core.config import settings
from app.sharding.constants import SHARD_MAP, TIMOUT_FOR_SHARD
from app.sharding.enums import ShardEnum


async def select_data_from_shard_file(*, shard_name: ShardEnum) -> list[dict]:
    """
    Получает данные из файла.
    """
    shard_file_path = os.path.join(
        settings.BASE_DIR, "app/sharding/files", f"{shard_name.value}.json"
    )
    with open(shard_file_path) as shard_file:
        data = json.load(shard_file)
        return data


async def select_data_from_shard(*, shard_name: ShardEnum) -> list[dict]:
    """
    Получает данные из шарда по http.
    """
    shard_url = SHARD_MAP[shard_name]
    async with AsyncClient() as client:
        response = await client.get(shard_url)
        result = response.json()
        return result


async def select_data_from_all_shards() -> list[dict]:
    """
    Получает данные из всех шардов по http.
    Игнорирует ошибки от шардов. Шарды могут отваливаться по таймауту.

    Может упасть целиком, если придут не правильные данные с какого то шарда.
    Можно решить проверкой контракта при получении данных с шарда.
    """
    selectors = [
        select_data_from_shard(shard_name=ShardEnum.first),
        select_data_from_shard(shard_name=ShardEnum.second),
        select_data_from_shard(shard_name=ShardEnum.third),
    ]
    results = await aggregate_all_data(selectors=selectors)
    return results


async def cancel_tasks(*, tasks: Iterable[Task]) -> None:
    for task in tasks:
        task.cancel()


async def fetch_results(
    *, selectors: list[Coroutine[Any, Any, list[dict]]], timeout: int
) -> AsyncGenerator[list[dict], None]:
    """
    Запускаем селекторы одновременно, получаем срез по таймауту.

    Можно было бы использовать wait_for с фильтрацией ошибок,
    но wait_for дожидается отмены таски => timeout не настоящий.
    await asyncio.gather(
        asyncio.wait_for(selectors_sleep(), timeout=2),
        asyncio.wait_for(selectors_error(), timeout=2),
        asyncio.wait_for(selectors_success(), timeout=2),
        return_exceptions=True
    )
    """
    done_tasks, pending_tasks = await asyncio.wait(selectors, timeout=timeout)

    for task in done_tasks:
        try:
            result = task.result()
        except Exception:
            pass
        else:
            yield result
        finally:
            #  отменяем таски, которые еще выполняются, ответа не дожидаемся, отмена не гарантируется
            asyncio.create_task(cancel_tasks(tasks=pending_tasks))


async def aggregate_all_data(
    selectors: list[Coroutine[Any, Any, list[dict]]], timeout: int = TIMOUT_FOR_SHARD
) -> list[dict]:
    """
    Запрашивает данные и агрегирует их.
    """
    fetched_result = fetch_results(selectors=selectors, timeout=timeout)

    results = []

    async for result in fetched_result:
        results.extend(result)

    results.sort(key=lambda item: int(item["id"]))
    return results
