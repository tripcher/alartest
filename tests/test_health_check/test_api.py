from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test__checks_list__smoke(async_client):
    async with async_client as ac:
        response = await ac.get("/checks")
    assert response.status_code == 200
