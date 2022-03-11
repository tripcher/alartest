"""Add role to users

Revision ID: e3a43f7e6f88
Revises: b43c9e8152f9
Create Date: 2022-03-11 15:14:13.833543

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e3a43f7e6f88"
down_revision = "b43c9e8152f9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("role_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "users", "roles", ["role_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_column("users", "role_id")
    # ### end Alembic commands ###