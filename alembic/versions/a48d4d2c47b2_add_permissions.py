"""Add permissions

Revision ID: a48d4d2c47b2
Revises: e3a43f7e6f88
Create Date: 2022-03-11 15:17:55.221912

"""
import sqlalchemy as sa

from alembic import op
from app.roles.enums import PermissionTypeEnum, ResourcesEnum

# revision identifiers, used by Alembic.
revision = "a48d4d2c47b2"
down_revision = "e3a43f7e6f88"
branch_labels = None
depends_on = None

# перечисляем типы, что бы не зависеть от изменения PermissionTypeEnum (не учитывать новые добавленные)
types = [
    PermissionTypeEnum.update,
    PermissionTypeEnum.delete,
    PermissionTypeEnum.create,
    PermissionTypeEnum.view,
]


def generate_permission_values(resource: ResourcesEnum) -> str:
    values = []
    for permission_type in types:
        values.append(f"('{permission_type.value}', '{resource.value}')")

    return ", ".join(values)


def upgrade():
    values = ", ".join(
        [
            generate_permission_values(ResourcesEnum.roles),
            generate_permission_values(ResourcesEnum.users),
            generate_permission_values(ResourcesEnum.checks),
            generate_permission_values(ResourcesEnum.permissions),
        ]
    )
    query = f"INSERT INTO permissions (type, resource) VALUES {values}"
    op.execute(query)


def downgrade():
    str_types = ", ".join([f"'{type.value}'" for type in types])
    resources = [
        ResourcesEnum.roles,
        ResourcesEnum.users,
        ResourcesEnum.checks,
        ResourcesEnum.permissions,
    ]
    str_resources = ", ".join([f"'{resource.value}'" for resource in resources])

    query = f"DELETE FROM permissions WHERE type IN ({str_types}) and resource in ({str_resources})"
    op.execute(query)
