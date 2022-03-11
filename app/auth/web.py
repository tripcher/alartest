from __future__ import annotations

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth/login.html", context={"request": request})
