"""add retailer_products table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-02-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'retailer_products',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('retailer', sa.String(), nullable=False),
        sa.Column('ean', sa.String(), nullable=True),
        sa.Column('sku', sa.String(), nullable=True),
        sa.Column('product_name', sa.String(), nullable=False),
        sa.Column('brand', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('list_price', sa.Float(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('product_url', sa.String(), nullable=True),
        sa.Column('last_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_retailer_products_retailer', 'retailer_products', ['retailer'])
    op.create_index('ix_retailer_products_ean', 'retailer_products', ['ean'])


def downgrade() -> None:
    op.drop_index('ix_retailer_products_ean', table_name='retailer_products')
    op.drop_index('ix_retailer_products_retailer', table_name='retailer_products')
    op.drop_table('retailer_products')
