from __future__ import annotations

import enum


class PermissionTypeEnum(enum.Enum):
    view = "view"
    create = "create"
    update = "update"
    delete = "delete"


class ResourcesEnum(enum.Enum):
    users = "users"
    roles = "roles"
    checks = "checks"
    permissions = "permissions"
