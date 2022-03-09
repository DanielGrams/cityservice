"""empty message

Revision ID: 04bce5aeff98
Revises: e5b60c3dee73
Create Date: 2022-03-08 16:52:23.082825

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

from project import dbtypes

# revision identifiers, used by Alembic.
revision = "04bce5aeff98"
down_revision = "e5b60c3dee73"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user", sa.Column("anonymous", sa.Boolean(), server_default="0", nullable=False)
    )


def downgrade():
    op.drop_column("user", "anonymous")
