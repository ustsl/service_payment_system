"""comment

Revision ID: 4da0918dd83b
Revises: cc0498fe90a6
Create Date: 2024-05-14 15:20:10.697969

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4da0918dd83b'
down_revision: Union[str, None] = 'cc0498fe90a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'invoice', ['invoice_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invoice', type_='unique')
    # ### end Alembic commands ###
