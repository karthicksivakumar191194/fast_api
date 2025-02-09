"""create role table

Revision ID: d12c0b8b0663
Revises: 67e275ae6964
Create Date: 2025-02-09 12:17:53.781299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd12c0b8b0663'
down_revision: Union[str, None] = '67e275ae6964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tenant_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('DELETED', 'ACTIVE', name='rolestatusenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_role_name', 'roles', ['name'], unique=False)
    op.create_index('idx_role_tenant_id', 'roles', ['tenant_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_role_tenant_id', table_name='roles')
    op.drop_index('idx_role_name', table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
