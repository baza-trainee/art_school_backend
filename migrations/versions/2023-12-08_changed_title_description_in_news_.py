"""changed title | description in news,posters/slider-main

Revision ID: 8478f2530afc
Revises: 802f1d4a46ca
Create Date: 2023-12-08 11:06:50.769843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8478f2530afc"
down_revision: Union[str, None] = "802f1d4a46ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posters", "text")
    op.alter_column(
        "slider_main",
        "title",
        existing_type=sa.VARCHAR(length=150),
        type_=sa.String(length=120),
        existing_nullable=True,
    )
    op.alter_column(
        "slider_main",
        "description",
        existing_type=sa.VARCHAR(length=150),
        type_=sa.String(length=200),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "slider_main",
        "description",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=150),
        existing_nullable=True,
    )
    op.alter_column(
        "slider_main",
        "title",
        existing_type=sa.String(length=120),
        type_=sa.VARCHAR(length=150),
        existing_nullable=True,
    )
    op.add_column(
        "posters", sa.Column("text", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###