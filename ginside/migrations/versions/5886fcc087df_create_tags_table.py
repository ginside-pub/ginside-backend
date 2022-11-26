"""Create tags table

Revision ID: 5886fcc087df
Revises: 30b2758068f4
Create Date: 2022-11-26 23:17:20.352061
"""

from alembic import op
import sqlalchemy as sa


revision = '5886fcc087df'
down_revision = '30b2758068f4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tags',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('tag', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('post_id', 'tag', name='tags_pk'),
    )

    op.create_index(op.f('ix_tags_post_id'), 'tags', ['post_id'], unique=False)
    op.create_index(op.f('ix_tags_tag'), 'tags', ['tag'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_tags_tag'), table_name='tags')
    op.drop_index(op.f('ix_tags_post_id'), table_name='tags')

    op.drop_table('tags')
