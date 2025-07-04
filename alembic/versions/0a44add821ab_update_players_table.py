"""update players table

Revision ID: 0a44add821ab
Revises: a88cff0ee33b
Create Date: 2025-05-16 16:28:25.119828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a44add821ab'
down_revision: Union[str, None] = 'a88cff0ee33b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('username', sa.String(length=100), nullable=False))
    op.add_column('players', sa.Column('password', sa.String(length=60), nullable=False))
    op.add_column('players', sa.Column('email', sa.String(length=320), nullable=False))
    op.add_column('players', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    op.create_unique_constraint(None, 'players', ['username'])
    op.create_unique_constraint(None, 'players', ['email'])
    op.drop_column('players', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'players', type_='unique')
    op.drop_constraint(None, 'players', type_='unique')
    op.drop_column('players', 'is_superuser')
    op.drop_column('players', 'email')
    op.drop_column('players', 'password')
    op.drop_column('players', 'username')
    # ### end Alembic commands ###
