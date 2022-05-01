"""empty message

Revision ID: 33453c1aaf10
Revises: 9db14947d300
Create Date: 2022-04-27 20:48:46.801510

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

from project import dbtypes

# revision identifiers, used by Alembic.
revision = "33453c1aaf10"
down_revision = "9db14947d300"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "recyclingstreets_users",
        sa.Column(
            "notifications_active", sa.Boolean(), server_default="0", nullable=False
        ),
    )


def downgrade():
    op.drop_column("recyclingstreets_users", "notifications_active")
