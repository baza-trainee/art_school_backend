"""change contact field to fileupload

Revision ID: ae60bf321c97
Revises: c4df2ade5fd4
Create Date: 2024-01-10 20:21:29.239240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ae60bf321c97"
down_revision: Union[str, None] = "c4df2ade5fd4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contacts", sa.Column("statement_for_admission", sa.String(), nullable=True)
    )
    op.add_column("contacts", sa.Column("official_info", sa.String(), nullable=True))
    op.drop_column("contacts", "admission_info_url")
    op.drop_column("contacts", "statute_url")
    op.drop_column("contacts", "legal_info_url")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contacts",
        sa.Column("legal_info_url", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "contacts",
        sa.Column("statute_url", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "contacts",
        sa.Column(
            "admission_info_url", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("contacts", "official_info")
    op.drop_column("contacts", "statement_for_admission")
    # ### end Alembic commands ###
