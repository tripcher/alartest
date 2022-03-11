"""Add superuser

Revision ID: 677ac76bc494
Revises: ac5b584cb23c
Create Date: 2022-03-11 19:59:22.332076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import orm

from app.roles.tables import roles
from app.users.tables import users
from app.auth.services import fake_hash_password

revision = '677ac76bc494'
down_revision = 'ac5b584cb23c'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    super_role = session.execute(
        roles.select().filter_by(title="Супер права для users")
    ).fetchone()

    password = fake_hash_password(password='superuser')
    session.execute(
        users.insert().values(username='superuser', password=password, role_id=super_role['id'])
    )
    session.flush()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    user = session.execute(
        users.select().filter_by(username="superuser")
    ).fetchone()
    session.execute(users.delete().filter_by(id=user['id']))
