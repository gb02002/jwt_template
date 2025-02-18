"""Fixed mapping and 'ordered_by'

Revision ID: 14c5b9175445
Revises: 15a48ced90d5
Create Date: 2024-07-30 16:24:28.411443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14c5b9175445'
down_revision: Union[str, None] = '15a48ced90d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('ordered_by', sa.Integer(), nullable=False))
    op.drop_constraint('items_order_fkey', 'items', type_='foreignkey')
    op.create_foreign_key(None, 'items', 'users', ['ordered_by'], ['id'], ondelete='CASCADE')
    op.drop_column('items', 'order')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'items', type_='foreignkey')
    op.create_foreign_key('items_order_fkey', 'items', 'users', ['order'], ['id'], ondelete='CASCADE')
    op.drop_column('items', 'ordered_by')
    # ### end Alembic commands ###
