"""Create user table

Revision ID: 4dfab64820a8
Revises: 20ba63e6655c
Create Date: 2022-10-29 13:50:38.575807
"""

from alembic import op
import sqlalchemy as sa


revision = '4dfab64820a8'
down_revision = '20ba63e6655c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('username', sa.Text(), nullable=False),
        sa.Column('display_name', sa.Text(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('username'),
    )

    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)
    op.create_index(op.f('ix_user_display_name'), 'user', ['display_name'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_user_display_name'), table_name='user')
    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_table('user')
