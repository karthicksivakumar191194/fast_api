"""create location table

Revision ID: 67e275ae6964
Revises: 8008d57e462d
Create Date: 2025-02-09 12:14:57.613543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67e275ae6964'
down_revision: Union[str, None] = '8008d57e462d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tenant_id', sa.UUID(), nullable=False),
    sa.Column('workspace_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Enum('DELETED', 'ACTIVE', name='locationstatusenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_location_name', 'locations', ['name'], unique=False)
    op.create_index('idx_location_tenant_id', 'locations', ['tenant_id'], unique=False)
    op.create_index('idx_location_workspace_id', 'locations', ['workspace_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_location_workspace_id', table_name='locations')
    op.drop_index('idx_location_tenant_id', table_name='locations')
    op.drop_index('idx_location_name', table_name='locations')
    op.drop_table('locations')
    # ### end Alembic commands ###
