"""Add time to results

Revision ID: bc6738c06822
Revises: 27d8af56bf86
Create Date: 2022-11-09 10:07:23.824396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc6738c06822'
down_revision = '27d8af56bf86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('results', 'time')
    # ### end Alembic commands ###
