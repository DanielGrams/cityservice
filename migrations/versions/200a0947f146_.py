"""empty message

Revision ID: 200a0947f146
Revises: 04bce5aeff98
Create Date: 2022-03-10 14:15:59.621426

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

from project import dbtypes

# revision identifiers, used by Alembic.
revision = "200a0947f146"
down_revision = "04bce5aeff98"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "place",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.Column("recycling_ids", sa.Unicode(length=255), nullable=True),
        sa.Column("weather_warning_name", sa.Unicode(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"], ["user.id"], name=op.f("fk_place_created_by_id_user")
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"], ["user.id"], name=op.f("fk_place_updated_by_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_place")),
        sa.UniqueConstraint("name", name=op.f("uq_place_name")),
    )
    op.create_table(
        "places_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("place_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["place_id"], ["place.id"], name=op.f("fk_places_users_place_id_place")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_places_users_user_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_places_users")),
    )
    op.create_table(
        "recyclingstreets_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("recyclingstreet_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["recyclingstreet_id"],
            ["recyclingstreets.id"],
            name=op.f("fk_recyclingstreets_users_recyclingstreet_id_recyclingstreets"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_recyclingstreets_users_user_id_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_recyclingstreets_users")),
    )
    op.add_column("newsfeed", sa.Column("place_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_newsfeed_place_id_place"), "newsfeed", "place", ["place_id"], ["id"]
    )
    op.add_column(
        "recyclingstreets", sa.Column("place_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        op.f("fk_recyclingstreets_place_id_place"),
        "recyclingstreets",
        "place",
        ["place_id"],
        ["id"],
    )
    op.add_column("weatherwarning", sa.Column("place_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_weatherwarning_place_id_place"),
        "weatherwarning",
        "place",
        ["place_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint(
        op.f("fk_weatherwarning_place_id_place"), "weatherwarning", type_="foreignkey"
    )
    op.drop_column("weatherwarning", "place_id")
    op.drop_constraint(
        op.f("fk_recyclingstreets_place_id_place"),
        "recyclingstreets",
        type_="foreignkey",
    )
    op.drop_column("recyclingstreets", "place_id")
    op.drop_constraint(
        op.f("fk_newsfeed_place_id_place"), "newsfeed", type_="foreignkey"
    )
    op.drop_column("newsfeed", "place_id")
    op.drop_table("recyclingstreets_users")
    op.drop_table("places_users")
    op.drop_table("place")
