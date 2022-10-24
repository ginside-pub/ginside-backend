"""Create sample table

Revision ID: 8226cb914395
Revises:
Create Date: 2022-10-24 21:30:16.806169
"""

from alembic import op
import sqlalchemy as sa


revision = '8226cb914395'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
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


def downgrade():
    op.drop_index(op.f('ix_sample_name'), table_name='sample')
    op.drop_table('sample')
