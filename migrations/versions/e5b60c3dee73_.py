"""empty message

Revision ID: e5b60c3dee73
Revises: f94690e0b957
Create Date: 2022-03-04 08:14:33.562349

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

from project import dbtypes
from project.models import NewsFeedType

# revision identifiers, used by Alembic.
revision = "e5b60c3dee73"
down_revision = "f94690e0b957"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("TRUNCATE newsitems;")
    op.create_table(
        "weatherwarning",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("headline", sa.String(), nullable=True),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("published", sa.DateTime(timezone=True), nullable=True),
        sa.Column("start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_weatherwarning")),
    )
    op.add_column(
        "newsfeed",
        sa.Column(
            "feed_type",
            dbtypes.IntegerEnum(NewsFeedType),
            server_default=str(NewsFeedType.unknown.value),
            nullable=False,
        ),
    )
    op.add_column("newsitems", sa.Column("news_feed_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f("fk_newsitems_news_feed_id_newsfeed"),
        "newsitems",
        "newsfeed",
        ["news_feed_id"],
        ["id"],
    )
    op.drop_column("newsitems", "publisher_icon_url")
    op.drop_column("newsitems", "publisher_name")


def downgrade():
    op.add_column(
        "newsitems",
        sa.Column("publisher_name", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "newsitems",
        sa.Column(
            "publisher_icon_url", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.drop_constraint(
        op.f("fk_newsitems_news_feed_id_newsfeed"), "newsitems", type_="foreignkey"
    )
    op.drop_column("newsitems", "news_feed_id")
    op.drop_column("newsfeed", "feed_type")
    op.drop_table("weatherwarning")
