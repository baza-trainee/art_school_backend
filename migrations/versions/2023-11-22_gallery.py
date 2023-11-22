"""gallery

Revision ID: a0f006470948
Revises: 524df6d32c29
Create Date: 2023-11-22 15:49:29.714092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a0f006470948"
down_revision: Union[str, None] = "524df6d32c29"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "gallery",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_video", sa.Boolean(), nullable=True),
        sa.Column("pinned_position", sa.Integer(), nullable=True),
        sa.Column("media", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("gallery")
    # ### end Alembic commands ###