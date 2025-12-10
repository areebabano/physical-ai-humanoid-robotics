"""Initial database schema

Revision ID: 91f30a3c4371
Revises: 
Create Date: 2025-12-07 05:51:39.164708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '91f30a3c4371'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass