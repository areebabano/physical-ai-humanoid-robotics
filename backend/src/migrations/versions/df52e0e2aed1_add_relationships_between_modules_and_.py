"""Add relationships between modules and chapters

Revision ID: df52e0e2aed1
Revises: 91f30a3c4371
Create Date: 2025-12-07 06:05:21.183406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'df52e0e2aed1'
down_revision: Union[str, None] = '91f30a3c4371'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass