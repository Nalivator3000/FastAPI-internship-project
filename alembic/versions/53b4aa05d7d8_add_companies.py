"""Add companies

Revision ID: 53b4aa05d7d8
Revises: 6c5db1ebff5b
Create Date: 2022-11-01 16:30:22.432017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53b4aa05d7d8'
down_revision = '6c5db1ebff5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('description', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('companies', 'description')
    # ### end Alembic commands ###
