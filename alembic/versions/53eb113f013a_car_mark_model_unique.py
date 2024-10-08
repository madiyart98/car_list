"""Car mark model unique

Revision ID: 53eb113f013a
Revises: f6e124e4392e
Create Date: 2024-08-14 08:50:48.463210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53eb113f013a'
down_revision: Union[str, None] = 'f6e124e4392e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uix_mark_model', 'cars', ['mark', 'model', 'year'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uix_mark_model', 'cars', type_='unique')
    # ### end Alembic commands ###
