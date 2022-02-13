"""empty message

Revision ID: f94690e0b957
Revises: c8588d8786c0
Create Date: 2022-02-11 17:05:33.632735

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f94690e0b957"
down_revision = "c8588d8786c0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "newsfeed", sa.Column("title_filter", sa.Unicode(length=255), nullable=True)
    )
    op.add_column(
        "newsfeed",
        sa.Column("title_sub_pattern", sa.Unicode(length=255), nullable=True),
    )
    op.add_column(
        "newsfeed", sa.Column("title_sub_repl", sa.Unicode(length=255), nullable=True)
    )


def downgrade():
    op.drop_column("newsfeed", "title_sub_repl")
    op.drop_column("newsfeed", "title_sub_pattern")
    op.drop_column("newsfeed", "title_filter")
