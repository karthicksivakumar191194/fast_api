"""create tenant table

Revision ID: 611145944922
Revises: 0075f407551e
Create Date: 2025-01-30 16:50:00.526200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '611145944922'
down_revision: Union[str, None] = '0075f407551e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tenants',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('DELETED', 'ACTIVE', 'IN_ACTIVE', name='tenantstatusenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tenants_name', 'tenants', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_tenants_name', table_name='tenants')
    op.drop_table('tenants')
    # ### end Alembic commands ###
