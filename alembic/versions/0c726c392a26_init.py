"""init

Revision ID: 0c726c392a26
Revises: dffc50e2284f
Create Date: 2024-06-25 12:36:19.033908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c726c392a26'
down_revision: Union[str, None] = 'dffc50e2284f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
