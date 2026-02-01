"""fix carbohidrato column name

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-02-01

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('productos', 'carbohidratos_g', new_column_name='carbohidrato_g')


def downgrade() -> None:
    op.alter_column('productos', 'carbohidrato_g', new_column_name='carbohidratos_g')
