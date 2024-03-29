"""create departments

Revision ID: 55afa0522d33
Revises: 265f2be58494
Create Date: 2023-11-17 13:36:00.534176

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "55afa0522d33"
down_revision: Union[str, None] = "265f2be58494"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "choreographic_department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sub_department_name", sa.String(length=300), nullable=True),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("photo", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "fine_arts_department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sub_department_name", sa.String(length=300), nullable=True),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("photo", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "music_department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sub_department_name", sa.String(length=300), nullable=True),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("photo", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "theatrical_department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sub_department_name", sa.String(length=300), nullable=True),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("photo", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vocal_choir_department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sub_department_name", sa.String(length=300), nullable=True),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("photo", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vocal_choir_department")
    op.drop_table("theatrical_department")
    op.drop_table("music_department")
    op.drop_table("fine_arts_department")
    op.drop_table("choreographic_department")
    # ### end Alembic commands ###
