"""Create productos table

Revision ID: 91eae425aeff
Revises: d666807524b8
Create Date: 2023-09-04 15:29:05.065709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91eae425aeff'
down_revision: Union[str, None] = 'd666807524b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('productos',sa.Column('id_producto',sa.Integer(),nullable=False,autoincrement=True,primary_key=True),
                    sa.Column('producto',sa.String()),
                    sa.Column('marca',sa.String()),
                    sa.Column('cantidad',sa.String()),
                    sa.Column('caloria_kcal',sa.Integer()),
                    sa.Column('grasa_g',sa.Float()),
                    sa.Column('carbohidratos_g',sa.Float()),
                    sa.Column('proteina_g',sa.Float()))
    pass


def downgrade() -> None:
    op.drop_table('productos')
    pass
