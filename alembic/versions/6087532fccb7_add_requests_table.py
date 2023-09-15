"""add requests table

Revision ID: 6087532fccb7
Revises: 91eae425aeff
Create Date: 2023-09-15 14:30:08.011417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6087532fccb7'
down_revision: Union[str, None] = '91eae425aeff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('requests',
                    sa.Column('id_request',sa.Integer(),nullable=False),
                    sa.Column('requested_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                    sa.Column('id_producto',sa.Integer(),sa.ForeignKey('productos.id_producto'),nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('requests')
