"""Add roles

Revision ID: ac5b584cb23c
Revises: a48d4d2c47b2
Create Date: 2022-03-11 15:37:02.145721

"""
import sqlalchemy as sa
# revision identifiers, used by Alembic.
from sqlalchemy import orm

from alembic import op
from app.roles.enums import PermissionTypeEnum, ResourcesEnum
from app.roles.tables import permissions_in_roles, roles

revision = "ac5b584cb23c"
down_revision = "a48d4d2c47b2"
branch_labels = None
depends_on = None

types = [
    PermissionTypeEnum.update,
    PermissionTypeEnum.delete,
    PermissionTypeEnum.create,
    PermissionTypeEnum.view,
]


def generate_all_permission_values(resource: ResourcesEnum) -> str:
    query = f"select permissions.id from permissions where permissions.resource = '{resource.value}'"
    conn = op.get_bind()
    permission_ids = conn.execute(query).fetchall()
    role = conn.execute(
        roles.select().filter_by(title="Супер права для users")
    ).fetchone()
    role_id = role["id"]

    values = []
    for permission_id in permission_ids:
        values.append(f"('{role_id}', '{permission_id[0]}')")

    return ", ".join(values)


def generate_read_permission_values(resource: ResourcesEnum) -> str:
    query = f"select permissions.id from permissions where permissions.resource = '{resource.value}' and permissions.type = '{PermissionTypeEnum.view.value}'"
    conn = op.get_bind()
    permission_ids = conn.execute(query).fetchall()
    role = conn.execute(
        roles.select().filter_by(title="Только чтение users")
    ).fetchone()
    role_id = role["id"]

    values = []
    for permission_id in permission_ids:
        values.append(f"('{role_id}', '{permission_id[0]}')")

    return ", ".join(values)


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.execute(roles.insert().values({"title": "Супер права для users"}))
    values = generate_all_permission_values(ResourcesEnum.users)
    query_permissions = (
        f"INSERT INTO permissions_in_roles (role_id, permission_id) VALUES {values}"
    )
    bind.execute(query_permissions)

    session.execute(roles.insert().values({"title": "Только чтение users"}))
    values = generate_read_permission_values(ResourcesEnum.users)
    query_permissions = (
        f"INSERT INTO permissions_in_roles (role_id, permission_id) VALUES {values}"
    )
    bind.execute(query_permissions)
    session.flush()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    read_role = session.execute(
        roles.select().filter_by(title="Только чтение users")
    ).fetchone()
    read_role_id = read_role["id"]
    session.execute(permissions_in_roles.delete().filter_by(role_id=read_role_id))
    session.execute(roles.delete().filter_by(id=read_role_id))

    super_role = session.execute(
        roles.select().filter_by(title="Супер права для users")
    ).fetchone()
    super_role_id = super_role["id"]
    session.execute(permissions_in_roles.delete().filter_by(role_id=super_role_id))
    session.execute(roles.delete().filter_by(id=super_role_id))
    session.flush()
