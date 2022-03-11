from __future__ import annotations

import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    BASE_API_URL: Optional[AnyHttpUrl] = None

    @validator("BASE_API_URL", pre=True)
    def assemble_base_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        return f'http://{values.get("SERVER_HOST", "")}:{values.get("SERVER_PORT", "")}{values.get("API_V1_STR", "")}'

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '['http://localhost', 'http://localhost:4200', 'http://localhost:3000', \
    # 'http://localhost:8080', 'http://local.dockertoolbox.tiangolo.com']'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "alartest"

    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "alartest"
    POSTGRES_PASSWORD: str = "alartest"
    POSTGRES_DB: str = "alartest"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_sql_alchemy_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f'/{values.get("POSTGRES_DB") or ""}',
        )

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f'/{values.get("POSTGRES_DB") or ""}',
        )

    FIRST_SUPERUSER: EmailStr = "alartest@example.ru"
    FIRST_SUPERUSER_PASSWORD: str = "alartest"
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
