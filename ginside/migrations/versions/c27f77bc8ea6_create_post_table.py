"""Create post table

Revision ID: c27f77bc8ea6
Revises: 8226cb914395
Create Date: 2022-10-26 16:18:56.221965
"""

from alembic import op
import sqlalchemy as sa


revision = 'c27f77bc8ea6'
down_revision = '8226cb914395'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'post',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('archived', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index(op.f('ix_post_created_at'), 'post', ['created_at'], unique=False)
    op.create_index(op.f('ix_post_title'), 'post', ['title'], unique=False)
    op.create_index(op.f('ix_post_updated_at'), 'post', ['updated_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_post_updated_at'), table_name='post')
    op.drop_index(op.f('ix_post_title'), table_name='post')
    op.drop_index(op.f('ix_post_created_at'), table_name='post')

    op.drop_table('post')
