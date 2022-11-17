"""Create posts table

Revision ID: 30b2758068f4
Revises: 191468c138e6
Create Date: 2022-11-17 16:15:26.251833
"""

from alembic import op
import sqlalchemy as sa


revision = '30b2758068f4'
down_revision = '191468c138e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('author', sa.Text(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('archived', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['author'], ['users.username'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index(op.f('ix_posts_author'), 'posts', ['author'], unique=False)
    op.create_index(op.f('ix_posts_created_at'), 'posts', ['created_at'], unique=False)
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_index(op.f('ix_posts_created_at'), table_name='posts')
    op.drop_index(op.f('ix_posts_author'), table_name='posts')

    op.drop_table('posts')
