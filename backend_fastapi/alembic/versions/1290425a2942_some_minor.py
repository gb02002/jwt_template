"""Some minor

Revision ID: 1290425a2942
Revises: 6a02f2250b87
Create Date: 2024-07-30 16:51:34.255242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1290425a2942'
down_revision: Union[str, None] = '6a02f2250b87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refresh_tokens', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('refresh_tokens_users_id_fkey', 'refresh_tokens', type_='foreignkey')
    op.create_foreign_key(None, 'refresh_tokens', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('refresh_tokens', 'users_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refresh_tokens', sa.Column('users_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'refresh_tokens', type_='foreignkey')
    op.create_foreign_key('refresh_tokens_users_id_fkey', 'refresh_tokens', 'users', ['users_id'], ['id'], ondelete='CASCADE')
    op.drop_column('refresh_tokens', 'user_id')
    # ### end Alembic commands ###
