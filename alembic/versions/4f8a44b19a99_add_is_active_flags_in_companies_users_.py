"""Add is active flags in companies_users and companies_administrators

Revision ID: 4f8a44b19a99
Revises: ae78e9e30b10
Create Date: 2022-11-03 08:13:59.605254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f8a44b19a99'
down_revision = 'ae78e9e30b10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies_administrators', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('companies_users', sa.Column('is_active_owner', sa.Boolean(), nullable=True))
    op.add_column('companies_users', sa.Column('is_active_user', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('companies_users', 'is_active_user')
    op.drop_column('companies_users', 'is_active_owner')
    op.drop_column('companies_administrators', 'is_active')
    # ### end Alembic commands ###
