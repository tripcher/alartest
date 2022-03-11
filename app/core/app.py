from __future__ import annotations

import os
from typing import Callable

from databases import Database
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.db import close_db_connection, connect_to_db
from app.core.exceptions import (AuthorizationError, LogicError,
                                 PermissionDeniedError)
from app.web import web_router


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app


async def authorization_error_handler(
    request: Request, exc: AuthorizationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid authentication credentials."},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def permission_error_handler(
    request: Request, exc: PermissionDeniedError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Permission denied."},
    )


async def logic_error_handler(request: Request, exc: LogicError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


def get_application(db_uri: str | None = settings.DATABASE_URI) -> FastAPI:
    if not db_uri:
        raise RuntimeError("Database uri not specified.")

    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    database = Database(db_uri, min_size=2, max_size=10)
    app.state._db = database

    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(settings.BASE_DIR, "static")),
        name="static",
    )

    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    app.add_exception_handler(AuthorizationError, authorization_error_handler)
    app.add_exception_handler(LogicError, logic_error_handler)
    app.add_exception_handler(PermissionDeniedError, permission_error_handler)

    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(web_router)

    return app
