"""Initial

Revision ID: 60ef1c11f350
Revises: 
Create Date: 2023-11-16 13:58:37.931364

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "60ef1c11f350"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("map_url", sa.String(length=1000), nullable=True),
        sa.Column("address", sa.String(length=300), nullable=True),
        sa.Column("phone", sa.String(length=15), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("facebook_url", sa.String(length=1000), nullable=True),
        sa.Column("youtube_url", sa.String(length=1000), nullable=True),
        sa.Column("admission_info_url", sa.String(), nullable=True),
        sa.Column("statute_url", sa.String(), nullable=True),
        sa.Column("legal_info_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("contacts")
    # ### end Alembic commands ###
