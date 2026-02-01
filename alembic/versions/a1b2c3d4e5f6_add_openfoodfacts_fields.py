"""add openfoodfacts fields

Revision ID: a1b2c3d4e5f6
Revises: 6087532fccb7
Create Date: 2026-02-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '6087532fccb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('productos', sa.Column('barcode', sa.String(), nullable=True))
    op.add_column('productos', sa.Column('nutriscore_grade', sa.String(), nullable=True))
    op.add_column('productos', sa.Column('nova_group', sa.Integer(), nullable=True))
    op.add_column('productos', sa.Column('ingredients_text', sa.Text(), nullable=True))
    op.add_column('productos', sa.Column('allergens', sa.String(), nullable=True))
    op.add_column('productos', sa.Column('image_url', sa.String(), nullable=True))
    op.create_index('ix_productos_barcode', 'productos', ['barcode'], unique=True)
    op.alter_column('productos', 'caloria_kcal', type_=sa.Float(), existing_type=sa.Integer())


def downgrade() -> None:
    op.alter_column('productos', 'caloria_kcal', type_=sa.Integer(), existing_type=sa.Float())
    op.drop_index('ix_productos_barcode', table_name='productos')
    op.drop_column('productos', 'image_url')
    op.drop_column('productos', 'allergens')
    op.drop_column('productos', 'ingredients_text')
    op.drop_column('productos', 'nova_group')
    op.drop_column('productos', 'nutriscore_grade')
    op.drop_column('productos', 'barcode')
