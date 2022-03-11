from __future__ import annotations

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter()


@router.get(
    "/users",
    response_class=HTMLResponse,
)
async def users_list(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users/list.html", context={"request": request})


@router.get(
    "/users/{user_id}",
    response_class=HTMLResponse,
)
async def users_list(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users/detail.html", context={"request": request})


@router.get(
    "/users/update/{user_id}",
    response_class=HTMLResponse,
)
async def users_update(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users/update.html", context={"request": request})
