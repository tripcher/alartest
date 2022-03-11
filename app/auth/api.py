from __future__ import annotations

from databases import Database
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dto import LoginData, LoginResponse
from app.auth.services import auth_login
from app.core.db import get_database

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Database = Depends(get_database),
) -> LoginResponse:
    login_data = LoginData(
        username=form_data.username,
        password=form_data.password,
    )
    token = await auth_login(db=db, login_data=login_data)
    return LoginResponse(access_token=token, token_type="bearer")
