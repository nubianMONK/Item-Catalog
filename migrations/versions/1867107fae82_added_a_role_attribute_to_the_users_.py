"""Added a role attribute to the users table

Revision ID: 1867107fae82
Revises: 5a44001ae062
Create Date: 2018-12-23 18:28:34.203261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1867107fae82'
down_revision = '5a44001ae062'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
