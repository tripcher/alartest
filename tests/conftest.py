from __future__ import annotations

import dataclasses
import uuid
from types import SimpleNamespace

import pytest
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy_utils import create_database, drop_database

from alembic.command import upgrade
from app.core.app import get_application
from app.core.config import settings
from app.core.db import close_db_connection, connect_to_db, make_alembic_config


@dataclasses.dataclass()
class TmpDatabaseUri:
    tmp_sqlalchemy_url: str
    tmp_databases_url: str


@pytest.fixture(autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture
def postgres() -> TmpDatabaseUri:
    """
    Создает временную БД для запуска теста.
    """
    tmp_name = "_".join([uuid.uuid4().hex, "pytest"])
    tmp_sqlalchemy_url = f"{settings.SQLALCHEMY_DATABASE_URI}_{tmp_name}"
    tmp_databases_url = f"{settings.DATABASE_URI}_{tmp_name}"
    create_database(tmp_sqlalchemy_url)

    try:
        yield TmpDatabaseUri(
            tmp_sqlalchemy_url=tmp_sqlalchemy_url, tmp_databases_url=tmp_databases_url
        )
    finally:
        drop_database(tmp_sqlalchemy_url)


@pytest.fixture
def alembic_config(postgres):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        pg_url=postgres.tmp_sqlalchemy_url,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config, postgres):
    """Накатывает миграции на временную БД."""
    upgrade(alembic_config, "head")
    return postgres


@pytest.fixture
async def app(migrated_postgres) -> FastAPI:
    app = get_application(db_uri=migrated_postgres.tmp_databases_url)
    await connect_to_db(app)
    yield app
    await close_db_connection(app)


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest.fixture
def async_client(app):
    return AsyncClient(app=app, base_url=settings.BASE_API_URL)
