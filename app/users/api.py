from __future__ import annotations

from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth.services import api_check_permissions_on_resource
from app.core.db import get_database
from app.roles.enums import PermissionTypeEnum, ResourcesEnum
from app.users.dto import CreateUserData, UpdateUserData, UserDetail, UserShort
from app.users.selectors import (all_users_for_list_display,
                                 find_user_detail_by_id)
from app.users.services import create_user, delete_user_by_id, update_user

router = APIRouter()


@router.get(
    "/users",
    response_model=list[UserShort],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            api_check_permissions_on_resource(
                permissions=[PermissionTypeEnum.view], resource=ResourcesEnum.users
            )
        )
    ],
)
async def users_list(db: Database = Depends(get_database)) -> list[UserShort]:
    return await all_users_for_list_display(db=db)


@router.get(
    "/users/{user_id}",
    response_model=UserDetail,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(
            api_check_permissions_on_resource(
                permissions=[PermissionTypeEnum.view], resource=ResourcesEnum.users
            )
        )
    ],
)
async def users_detail(
    user_id: int, db: Database = Depends(get_database)
) -> UserDetail:
    user = await find_user_detail_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return user


@router.post(
    "/users",
    response_model=UserDetail,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            api_check_permissions_on_resource(
                permissions=[PermissionTypeEnum.create], resource=ResourcesEnum.users
            )
        )
    ],
)
async def users_create(
    data: CreateUserData, db: Database = Depends(get_database)
) -> UserDetail:
    return await create_user(db=db, data=data)


@router.put(
    "/users/{user_id}",
    response_model=UserDetail,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            api_check_permissions_on_resource(
                permissions=[PermissionTypeEnum.update], resource=ResourcesEnum.users
            )
        )
    ],
)
async def users_update(
    user_id: int, data: UpdateUserData, db: Database = Depends(get_database)
) -> UserDetail:
    return await update_user(db=db, user_id=user_id, data=data)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            api_check_permissions_on_resource(
                permissions=[PermissionTypeEnum.delete], resource=ResourcesEnum.users
            )
        )
    ],
)
async def users_delete(user_id: int, db: Database = Depends(get_database)) -> None:
    await delete_user_by_id(db=db, user_id=user_id)
