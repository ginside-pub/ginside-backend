"""Remove sample table

Revision ID: 20ba63e6655c
Revises: c27f77bc8ea6
Create Date: 2022-10-26 16:36:29.321883
"""

from alembic import op
import sqlalchemy as sa


revision = '20ba63e6655c'
down_revision = 'c27f77bc8ea6'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index(op.f('ix_sample_name'), table_name='sample')
    op.drop_table('sample')


def downgrade():
    op.create_table(
        'sample',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index(op.f('ix_sample_name'), 'sample', ['name'], unique=True)
