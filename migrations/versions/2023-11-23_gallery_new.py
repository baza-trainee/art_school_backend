"""gallery_new

Revision ID: 4d29171bec91
Revises: 4cd1c281d770
Create Date: 2023-11-23 15:19:35.971761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d29171bec91'
down_revision: Union[str, None] = '4cd1c281d770'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gallery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_video', sa.Boolean(), nullable=False),
    sa.Column('is_achivement', sa.Boolean(), nullable=False),
    sa.Column('media', sa.String(), nullable=False),
    sa.Column('pinned_position', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('sub_department', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sub_department'], ['sub_departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('choreographic_department')
    op.drop_table('vocal_choir_department')
    op.drop_table('theatrical_department')
    op.drop_table('music_department')
    op.drop_table('fine_arts_department')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fine_arts_department',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sub_department_name', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='fine_arts_department_pkey')
    )
    op.create_table('music_department',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sub_department_name', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='music_department_pkey')
    )
    op.create_table('theatrical_department',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sub_department_name', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='theatrical_department_pkey')
    )
    op.create_table('vocal_choir_department',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sub_department_name', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='vocal_choir_department_pkey')
    )
    op.create_table('choreographic_department',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sub_department_name', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='choreographic_department_pkey')
    )
    op.drop_table('gallery')
    # ### end Alembic commands ###