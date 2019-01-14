"""Added custom MetaData Object

Revision ID: 4d9889c4fb5c
Revises: c79e8f9b9b39
Create Date: 2019-01-04 07:12:43.783084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d9889c4fb5c'
down_revision = 'c79e8f9b9b39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_users_token'), 'users', ['token'])
    op.drop_constraint('users_token_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_token_key', 'users', ['token'])
    op.drop_constraint(op.f('uq_users_token'), 'users', type_='unique')
    # ### end Alembic commands ###
