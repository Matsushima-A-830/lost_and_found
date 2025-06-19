"""create tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2024-06-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '0001_create_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(64), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(128), nullable=False),
        sa.Column('role', sa.String(16), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('management_number', sa.String(32), nullable=False, unique=True),
        sa.Column('found_datetime', sa.DateTime, nullable=False),
        sa.Column('found_place', sa.String(128), nullable=False),
        sa.Column('category_l', sa.String(32), nullable=False),
        sa.Column('category_m', sa.String(32)),
        sa.Column('category_s', sa.String(32)),
        sa.Column('color', sa.String(32)),
        sa.Column('features', sa.Text),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('image_path', sa.String(256)),
        sa.Column('registered_by_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index('idx_items_found_datetime', 'items', ['found_datetime'])
    op.create_index('idx_items_status_category', 'items', ['status', 'category_l'])
    # 他テーブルも同様に追加

def downgrade():
    op.drop_index('idx_items_status_category', table_name='items')
    op.drop_index('idx_items_found_datetime', table_name='items')
    op.drop_table('items')
    op.drop_table('users')
