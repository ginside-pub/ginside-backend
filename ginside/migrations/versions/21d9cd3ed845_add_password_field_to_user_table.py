"""Add password field to user table

Revision ID: 21d9cd3ed845
Revises: 4dfab64820a8
Create Date: 2022-10-29 17:05:32.027733
"""

from alembic import op
import sqlalchemy as sa


revision = '21d9cd3ed845'
down_revision = '4dfab64820a8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('password', sa.Text(), nullable=False))


def downgrade():
    op.drop_column('user', 'password')
