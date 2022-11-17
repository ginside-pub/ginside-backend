"""Create posts table

Revision ID: c836435ec14a
Revises: 191468c138e6
Create Date: 2022-11-17 15:44:45.744694
"""

from alembic import op
import sqlalchemy as sa


revision = 'c836435ec14a'
down_revision = '191468c138e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('archived', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index(op.f('ix_posts_created_at'), 'posts', ['created_at'], unique=False)
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_index(op.f('ix_posts_created_at'), table_name='posts')

    op.drop_table('posts')
