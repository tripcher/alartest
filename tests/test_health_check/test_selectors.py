from __future__ import annotations

import pytest

from app.health_check.dto import HealthCheck
from app.health_check.selectors import all_checks
from app.health_check.tables import checks


@pytest.mark.anyio
async def test__all_checks__empty(db):

    result = await all_checks(db=db)

    assert result == []


@pytest.mark.anyio
async def test__all_checks__check_fields(db):
    query = checks.insert().values(title="Test")
    record_id = await db.execute(query)
    expected_result = [HealthCheck(id=record_id, title="Test")]

    result = await all_checks(db=db)

    assert result == expected_result
