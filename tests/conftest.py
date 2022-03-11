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
from app.health_check.tables import checks
from app.roles.dto import Role

from app.roles.enums import PermissionTypeEnum, ResourcesEnum
from app.roles.tables import roles, permissions, permissions_in_roles
from app.users.dto import User
from app.users.tables import users


@dataclasses.dataclass()
class TmpDatabaseUri:
    tmp_sqlalchemy_url: str
    tmp_databases_url: str


@pytest.fixture(autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def clean_db(db):
    await db.execute(permissions_in_roles.delete())
    await db.execute(permissions.delete())
    await db.execute(users.delete())
    await db.execute(roles.delete())
    await db.execute(checks.delete())


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


# фабрики на минималках

@pytest.fixture
def user_factory(db):
    async def _user_factory(username: str = 'test', password: str = 'test', role_id: int | None = None):
        query = users.insert().values(username=username, password=password, role_id=role_id)
        record_id = await db.execute(query)
        return User(id=record_id, username=username, password=password, role_id=role_id)
    return _user_factory


@pytest.fixture
def role_factory(db):
    async def _role_factory(title: str = 'test'):
        query = roles.insert().values(title=title)
        record_id = await db.execute(query)
        return Role(id=record_id, title=title)
    return _role_factory


@pytest.fixture
def role_with_permissions_factory(db):
    async def _role_with_permissions(
            permission_types: list[PermissionTypeEnum], resource: ResourcesEnum
    ) -> Role:
        query = roles.insert().values(
            title='Test'
        )
        role_id = await db.execute(query)
        raw_role = await db.fetch_one(roles.select().filter_by(id=role_id))

        await db.execute_many(
            query=permissions.insert(),
            values=[{'type': type.value, 'resource': resource.value} for type in permission_types]
        )
        db_permissions = await db.fetch_all(query=permissions.select())

        await db.execute_many(
            query=permissions_in_roles.insert(),
            values=[{'permission_id': permission['id'], 'role_id': role_id} for permission in db_permissions]
        )

        return Role(**raw_role)

    return _role_with_permissions
