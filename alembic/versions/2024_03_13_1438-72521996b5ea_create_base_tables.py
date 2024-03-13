"""create base tables

Revision ID: 72521996b5ea
Revises: 
Create Date: 2024-03-13 14:38:18.654267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "72521996b5ea"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "scale_model",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("keywords", sa.String(length=255), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("scale", sa.String(length=20), nullable=False),
        sa.Column("brand", sa.String(length=25), nullable=False),
        sa.Column("search_url_created_by_user", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("about", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "collection",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cookie_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sold_ad",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_ebay", sa.String(), nullable=False),
        sa.Column("raw_sold_date", sa.String(length=100), nullable=False),
        sa.Column("sold_date", sa.DateTime(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("ebay_link", sa.Text(), nullable=False),
        sa.Column(
            "include_in_calculation",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column("scale_model_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["scale_model_id"],
            ["scale_model.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "collection_and_scale_model",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("collection_id", sa.Integer(), nullable=False),
        sa.Column("scale_model_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["collection_id"],
            ["collection.id"],
        ),
        sa.ForeignKeyConstraint(
            ["scale_model_id"],
            ["scale_model.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "collection_price",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_collection", sa.Integer(), nullable=False),
        sa.Column("min_price", sa.Integer(), nullable=False),
        sa.Column("max_price", sa.Integer(), nullable=False),
        sa.Column(
            "update_date",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_collection"],
            ["collection.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "scale_model_and_ad_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scale_model_id", sa.Integer(), nullable=False),
        sa.Column("sold_ad_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["scale_model_id"],
            ["scale_model.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sold_ad_id"],
            ["sold_ad.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("scale_model_and_ad_association")
    op.drop_table("collection_price")
    op.drop_table("collection_and_scale_model")
    op.drop_table("sold_ad")
    op.drop_table("cookie_table")
    op.drop_table("collection")
    op.drop_table("user")
    op.drop_table("scale_model")
    # ### end Alembic commands ###