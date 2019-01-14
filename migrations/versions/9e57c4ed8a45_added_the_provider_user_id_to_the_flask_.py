"""Added the provider_user_id to the flask_dance_oauth table

Revision ID: 9e57c4ed8a45
Revises: 1ab080a61204
Create Date: 2019-01-05 00:38:30.274975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e57c4ed8a45'
down_revision = '1ab080a61204'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flask_dance_oauth', sa.Column('provider_user_id', sa.String(length=256), nullable=True))
    op.create_unique_constraint(op.f('uq_flask_dance_oauth_provider_user_id'), 'flask_dance_oauth', ['provider_user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_flask_dance_oauth_provider_user_id'), 'flask_dance_oauth', type_='unique')
    op.drop_column('flask_dance_oauth', 'provider_user_id')
    # ### end Alembic commands ###
