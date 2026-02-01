"""add serving nutritional data

Revision ID: e4f5a6b7c8d9
Revises: c3d4e5f6a7b8
Create Date: 2026-02-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e4f5a6b7c8d9'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('productos', 'caloria_kcal', new_column_name='caloria_kcal_100g')
    op.alter_column('productos', 'grasa_g', new_column_name='grasa_g_100g')
    op.alter_column('productos', 'carbohidrato_g', new_column_name='carbohidrato_g_100g')
    op.alter_column('productos', 'proteina_g', new_column_name='proteina_g_100g')
    op.alter_column('productos', 'cantidad', new_column_name='serving_size')
    
    op.add_column('productos', sa.Column('serving_quantity_g', sa.Float(), nullable=True))
    op.add_column('productos', sa.Column('caloria_kcal_serving', sa.Float(), nullable=True))
    op.add_column('productos', sa.Column('grasa_g_serving', sa.Float(), nullable=True))
    op.add_column('productos', sa.Column('carbohidrato_g_serving', sa.Float(), nullable=True))
    op.add_column('productos', sa.Column('proteina_g_serving', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('productos', 'proteina_g_serving')
    op.drop_column('productos', 'carbohidrato_g_serving')
    op.drop_column('productos', 'grasa_g_serving')
    op.drop_column('productos', 'caloria_kcal_serving')
    op.drop_column('productos', 'serving_quantity_g')
    
    op.alter_column('productos', 'serving_size', new_column_name='cantidad')
    op.alter_column('productos', 'proteina_g_100g', new_column_name='proteina_g')
    op.alter_column('productos', 'carbohidrato_g_100g', new_column_name='carbohidrato_g')
    op.alter_column('productos', 'grasa_g_100g', new_column_name='grasa_g')
    op.alter_column('productos', 'caloria_kcal_100g', new_column_name='caloria_kcal')
