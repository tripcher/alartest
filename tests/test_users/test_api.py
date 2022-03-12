from __future__ import annotations

import pytest

from app.roles.enums import PermissionTypeEnum, ResourcesEnum


@pytest.mark.anyio
async def test__users_list__smoke_with_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[PermissionTypeEnum.view],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.get("/users")
    assert response.status_code == 200


@pytest.mark.anyio
async def test__users_list__smoke_with_another_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[
            PermissionTypeEnum.update,
            PermissionTypeEnum.create,
            PermissionTypeEnum.delete,
        ],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.get("/users")
    assert response.status_code == 403


@pytest.mark.anyio
async def test__users_list__smoke_not_auth(async_client):
    async with async_client as ac:
        response = await ac.get("/users")
    assert response.status_code == 401


@pytest.mark.anyio
async def test__users_detail__smoke_with_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[PermissionTypeEnum.view],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.get(f"/users/{user.id}")
    assert response.status_code == 200


@pytest.mark.anyio
async def test__users_detail__smoke_with_another_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[
            PermissionTypeEnum.update,
            PermissionTypeEnum.create,
            PermissionTypeEnum.delete,
        ],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.get(f"/users/{user.id}")
    assert response.status_code == 403


@pytest.mark.anyio
async def test__users_detail__smoke_not_auth(async_client):
    async with async_client as ac:
        response = await ac.get("/users/100")
    assert response.status_code == 401


@pytest.mark.anyio
async def test__users_create__smoke_with_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[PermissionTypeEnum.create],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.post("/users")
    assert response.status_code == 422  # validation error


@pytest.mark.anyio
async def test__users_create__smoke_with_another_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[
            PermissionTypeEnum.view,
            PermissionTypeEnum.update,
            PermissionTypeEnum.delete,
        ],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.post("/users")
    assert response.status_code == 403


@pytest.mark.anyio
async def test__users_create__smoke_not_auth(async_client):
    async with async_client as ac:
        response = await ac.post("/users")
    assert response.status_code == 401


@pytest.mark.anyio
async def test__users_update__smoke_with_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[PermissionTypeEnum.update],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.put(f"/users/{user.id}")
    assert response.status_code == 422  # validation error


@pytest.mark.anyio
async def test__users_update__smoke_with_another_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[
            PermissionTypeEnum.view,
            PermissionTypeEnum.create,
            PermissionTypeEnum.delete,
        ],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.put(f"/users/{user.id}")
    assert response.status_code == 403


@pytest.mark.anyio
async def test__users_update__smoke_not_auth(async_client):
    async with async_client as ac:
        response = await ac.put("/users/200")
    assert response.status_code == 401


@pytest.mark.anyio
async def test__users_delete__smoke_with_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[PermissionTypeEnum.delete],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.delete(f"/users/{user.id}")
    assert response.status_code == 204


@pytest.mark.anyio
async def test__users_delete__smoke_with_another_permissions(
    user_with_permissions_factory, async_client_for_user
):
    user = await user_with_permissions_factory(
        permission_types=[
            PermissionTypeEnum.view,
            PermissionTypeEnum.create,
            PermissionTypeEnum.update,
        ],
        resource=ResourcesEnum.users,
    )
    async_client = await async_client_for_user(user)
    async with async_client as ac:
        response = await ac.delete(f"/users/{user.id}")
    assert response.status_code == 403


@pytest.mark.anyio
async def test__users_delete__smoke_not_auth(async_client):
    async with async_client as ac:
        response = await ac.delete("/users/150")
    assert response.status_code == 401
