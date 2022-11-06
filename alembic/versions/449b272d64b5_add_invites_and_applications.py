"""Add invites and applications

Revision ID: 449b272d64b5
Revises: 2f8e39eb08ce
Create Date: 2022-11-04 11:21:15.298733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '449b272d64b5'
down_revision = '2f8e39eb08ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('invites',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.drop_column('companies_users', 'is_active_user')
    op.drop_column('companies_users', 'is_active_owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies_users', sa.Column('is_active_owner', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('companies_users', sa.Column('is_active_user', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_table('invites')
    op.drop_table('applications')
    # ### end Alembic commands ###