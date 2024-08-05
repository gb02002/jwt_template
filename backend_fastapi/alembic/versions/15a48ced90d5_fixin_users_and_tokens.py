"""Fixin users and tokens

Revision ID: 15a48ced90d5
Revises: 8e2a5ef6b98b
Create Date: 2024-07-30 16:01:03.961985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15a48ced90d5'
down_revision: Union[str, None] = '8e2a5ef6b98b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('order', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'items', 'users', ['order'], ['id'], ondelete='CASCADE')
    op.add_column('refresh_token', sa.Column('users_id', sa.Integer(), nullable=False))
    op.drop_constraint('refresh_token_user_id_fkey', 'refresh_token', type_='foreignkey')
    op.create_foreign_key(None, 'refresh_token', 'users', ['users_id'], ['id'])
    op.drop_column('refresh_token', 'user_id')
    op.add_column('users', sa.Column('password_hash', sa.String(), nullable=False))
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.drop_constraint('users_order_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'order')
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_order_fkey', 'users', 'items', ['order'], ['id'], ondelete='CASCADE')
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.drop_column('users', 'password_hash')
    op.add_column('refresh_token', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'refresh_token', type_='foreignkey')
    op.create_foreign_key('refresh_token_user_id_fkey', 'refresh_token', 'users', ['user_id'], ['id'])
    op.drop_column('refresh_token', 'users_id')
    op.drop_constraint(None, 'items', type_='foreignkey')
    op.drop_column('items', 'order')
    # ### end Alembic commands ###
