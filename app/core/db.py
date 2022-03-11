from __future__ import annotations

import logging
import os
from types import SimpleNamespace

from databases import Database
from fastapi import FastAPI
from sqlalchemy import MetaData
from starlette.requests import Request

from alembic.config import Config

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

metadata = MetaData()


async def connect_to_db(app: FastAPI) -> None:
    logger.info("OPEN DB CONNECTION")

    try:
        await app.state._db.connect()
    except Exception as e:
        logger.error("--- DB CONNECTION ERROR ---")
        logger.error(e)
        logger.error("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("CLOSE DB CONNECTION")
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.error("--- DB DISCONNECT ERROR ---")
        logger.error(e)
        logger.error("--- DB DISCONNECT ERROR ---")


def get_database(request: Request) -> Database:
    return request.app.state._db


def make_alembic_config(cmd_opts: SimpleNamespace, base_path: str = BASE_DIR) -> Config:
    """
    Создает объект конфигурации alembic на основе аргументов,
    подменяет относительные пути на абсолютные.
    """
    print("base_path", base_path)
    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option("script_location")
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            "script_location", os.path.join(base_path, alembic_location)
        )
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    return config
