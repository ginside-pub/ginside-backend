"""Create users table

Revision ID: 191468c138e6
Revises:
Create Date: 2022-11-17 15:43:45.832599
"""

from alembic import op
import sqlalchemy as sa


revision = '191468c138e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('username', sa.Text(), nullable=False),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('display_name', sa.Text(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('username'),
    )

    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_display_name'), 'users', ['display_name'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_display_name'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')

    op.drop_table('users')
