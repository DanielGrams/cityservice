"""empty message

Revision ID: 9db14947d300
Revises: 200a0947f146
Create Date: 2022-04-04 19:25:01.034091

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

from project import dbtypes
from project.models import PushPlatform

# revision identifiers, used by Alembic.
revision = "9db14947d300"
down_revision = "200a0947f146"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pushregistration",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.UnicodeText(), nullable=True),
        sa.Column("device", sa.Unicode(length=255), nullable=False),
        sa.Column("platform", dbtypes.IntegerEnum(PushPlatform), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name=op.f("fk_pushregistration_created_by_id_user"),
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name=op.f("fk_pushregistration_updated_by_id_user"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_pushregistration_user_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pushregistration")),
    )


def downgrade():
    op.drop_table("pushregistration")
