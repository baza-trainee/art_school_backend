"""validation change

Revision ID: c2be75aaa046
Revises: 1ffecc031881
Create Date: 2024-01-15 22:29:39.245507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2be75aaa046'
down_revision: Union[str, None] = '1ffecc031881'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('school_administrations', 'full_name',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=60),
               existing_nullable=True)
    op.alter_column('school_administrations', 'position',
               existing_type=sa.VARCHAR(length=2000),
               type_=sa.String(length=120),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('school_administrations', 'position',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=2000),
               existing_nullable=True)
    op.alter_column('school_administrations', 'full_name',
               existing_type=sa.String(length=60),
               type_=sa.VARCHAR(length=150),
               existing_nullable=True)
    # ### end Alembic commands ###